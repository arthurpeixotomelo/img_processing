import marimo

__generated_with = "0.23.16"
app = marimo.App()


@app.cell
def _():
    from time import monotonic
    from dataclasses import dataclass

    import polars as pl
    from httpx import HTTPError, AsyncClient
    from playwright.async_api import async_playwright
    from asyncio import Semaphore, gather, sleep, Lock

    FALLBACK_IMAGE_INDEX = 1
    DEFAULT_TARGET_CSV = 'scrapper_data.csv'
    PARQUET_OUT = 'structured_scrapper_data_new.parquet'
    return (
        AsyncClient,
        DEFAULT_TARGET_CSV,
        FALLBACK_IMAGE_INDEX,
        HTTPError,
        Lock,
        PARQUET_OUT,
        Semaphore,
        async_playwright,
        dataclass,
        gather,
        monotonic,
        pl,
        sleep,
    )


@app.cell
def _(Lock, Semaphore, dataclass, monotonic, sleep):
    class AsyncRateLimiter:
        """Async throttle: caps requests per second across coroutines."""

        def __init__(self, requests_per_second: float) -> None:
            self._min_interval_s = 1.0 / float(requests_per_second)
            self._lock = Lock()
            self._next_allowed = 0.0

        async def acquire(self) -> None:
            async with self._lock:
                now = monotonic()
                scheduled = max(now, self._next_allowed)
                self._next_allowed = scheduled + self._min_interval_s
            delay = scheduled - now
            if delay > 0:
                await sleep(delay)

    @dataclass(frozen=True, slots=True)
    class FetchConfig:
        requests_per_second: float = 5
        timeout_seconds: float = 5
        max_retries: int = 2
        backoff_seconds: float = 0.5
        max_concurrency: int = 16

        def __post_init__(self) -> None:
            if self.requests_per_second <= 0:
                raise ValueError('requests_per_second must be > 0')
            if self.max_concurrency <= 0:
                raise ValueError('max_concurrency must be > 0')

        def rate_limiter(self) -> AsyncRateLimiter:
            return AsyncRateLimiter(self.requests_per_second)

        def semaphore(self) -> Semaphore:
            return Semaphore(self.max_concurrency)

    return (FetchConfig,)


@app.cell
def _(AsyncClient, FetchConfig, HTTPError, sleep):
    async def fetch_bytes(
        client: AsyncClient,
        url: str,
        cfg: FetchConfig,
    ) -> bytes:
        limiter = cfg.rate_limiter()
        if not url:
            raise ValueError('Empty URL')

        last_error: Exception | None = None
        for attempt in range(cfg.max_retries + 1):
            await limiter.acquire()
            try:
                response = await client.get(url, timeout=cfg.timeout_seconds)
                response.raise_for_status()
                return response.content
            except HTTPError as exc:
                last_error = exc
                if attempt >= cfg.max_retries:
                    break
                await sleep(cfg.backoff_seconds * (2 ** attempt))

        raise last_error or RuntimeError('Failed to fetch image bytes')

    return (fetch_bytes,)


@app.cell
def _(AsyncClient, FALLBACK_IMAGE_INDEX, FetchConfig, fetch_bytes):
    async def fetch_direct(row: dict, client: AsyncClient, cfg: FetchConfig) -> bytes:
        return await fetch_bytes(client, row['displayUrl'], cfg)


    async def fetch_via_post(row: dict, client: AsyncClient, cfg: FetchConfig, browser) -> bytes:
        img_url = await extract_img_url(browser, row['url'])
        if not img_url:
            raise ValueError(f'No image src on {row["url"]}')
        return await fetch_bytes(client, img_url, cfg)


    async def extract_img_url(browser, post_url: str) -> str | None:
        page = await browser.new_page()
        try:
            await page.goto(post_url)
            imgs = await page.query_selector_all('img')
            if len(imgs) <= FALLBACK_IMAGE_INDEX:
                return None
            return await imgs[FALLBACK_IMAGE_INDEX].get_attribute('src')
        finally:
            await page.close()

    return fetch_direct, fetch_via_post


@app.cell
def _(
    AsyncClient,
    FetchConfig,
    async_playwright,
    fetch_direct,
    fetch_via_post,
    gather,
    pl,
):
    async def fetch_all(frame: pl.DataFrame, cfg: FetchConfig) -> list[bytes | None]:
        rows = frame.to_dicts()
        sem = cfg.semaphore()

        async def fetch_one(row: dict) -> bytes | None:
            async def run(fetch, *args):
                async with sem:
                    return await fetch(row, client, cfg, *args)

            try:
                return await run(fetch_direct)
            except Exception:
                pass

            try:
                return await run(fetch_via_post, browser)
            except Exception:
                return None

        async with AsyncClient() as client, async_playwright() as playwright:
            browser = await playwright.chromium.launch()
            try:
                return await gather(*(fetch_one(r) for r in rows))
            finally:
                await browser.close()

    return (fetch_all,)


@app.cell
def _(DEFAULT_TARGET_CSV, FetchConfig, fetch_all, pl):
    async def build_structured_scrapper_frame(
        source_csv: str = DEFAULT_TARGET_CSV,
        cfg: FetchConfig = FetchConfig(),
    ) -> pl.DataFrame:
        frame = (
            pl.read_csv(source_csv).filter(pl.col('type') != 'Video')
        )

        image_bytes = await fetch_all(frame, cfg)

        return frame.select(
            pl.col('ownerId').alias('id'),
            pl.col('ownerUsername').alias('username'),
            pl.col('id').alias('post_id'),
            pl.col('url').alias('post_url'),
            pl.col('caption').alias('post_caption'),
            pl.col('likesCount').alias('post_likes'),
            pl.col('commentsCount').alias('post_comments'),
            pl.col('displayUrl').alias('post_img_url'),
            pl.Series('post_img_data', image_bytes, dtype=pl.Binary),
            pl.col('type').alias('post_type'),
            pl.col('timestamp').alias('post_created_at'),
        )

    return (build_structured_scrapper_frame,)


@app.cell
async def _(DEFAULT_TARGET_CSV, FetchConfig, build_structured_scrapper_frame):
    df = await build_structured_scrapper_frame(
        DEFAULT_TARGET_CSV,
        FetchConfig(requests_per_second=60, max_concurrency=32)
    )
    return (df,)


@app.cell
def _(PARQUET_OUT, df):
    df.write_parquet(PARQUET_OUT)
    return


if __name__ == "__main__":
    app.run()
