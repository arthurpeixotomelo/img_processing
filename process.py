# /// script
# requires-python = ">=3.13"
# dependencies = [
#     "marimo>=0.23.3",
#     "polars>=1.43.0",
#     "requests>=2.34.2",
# ]
# ///

import marimo

__generated_with = "0.23.14"
app = marimo.App()


@app.cell
def _():
    from pathlib import Path
    from threading import Lock
    from time import monotonic, sleep
    from collections.abc import Iterable
    from concurrent.futures import ThreadPoolExecutor, as_completed

    import polars as pl
    from requests import get

    return (
        Iterable,
        Lock,
        Path,
        ThreadPoolExecutor,
        as_completed,
        get,
        monotonic,
        pl,
        sleep,
    )


@app.cell
def _(Iterable, Lock, ThreadPoolExecutor, as_completed, get, monotonic, sleep):
    class GlobalRateLimiter:
        """Thread-safe limiter that caps the number of requests per second."""

        def __init__(self, requests_per_second: float) -> None:
            if requests_per_second <= 0:
                raise ValueError("requests_per_second must be greater than zero")
            self._min_interval_s = 1.0 / float(requests_per_second)
            self._lock = Lock()
            self._next_allowed = 0.0

        def wait(self) -> None:
            with self._lock:
                now = monotonic()
                scheduled = max(now, self._next_allowed)
                self._next_allowed = scheduled + self._min_interval_s
            delay = scheduled - now
            if delay > 0:
                sleep(delay)


    def fetch_bytes(
        url: str,
        *,
        timeout_s: float,
        max_retries: int,
        backoff_s: float,
        limiter: GlobalRateLimiter,
    ) -> bytes:
        if not url:
            raise ValueError("Empty URL")

        last_error: Exception | None = None
        for attempt in range(max_retries + 1):
            limiter.wait()
            try:
                response = get(url, timeout=timeout_s)
                response.raise_for_status()
                return response.content
            except Exception as exc:
                last_error = exc
                if attempt >= max_retries:
                    break
                sleep(backoff_s * (2**attempt))

        raise last_error or RuntimeError("Failed to fetch image bytes")


    def fetch_image_contents(
        urls: Iterable[str],
        *,
        max_workers: int = 16,
        requests_per_second: float = 5,
        timeout_s: float = 20,
        max_retries: int = 2,
        backoff_s: float = 0.5,
        raise_on_error: bool = True,
    ) -> list[bytes | None]:
        url_list: list[str] = list(urls)
        results: list[bytes | None] = [None] * len(url_list)
        limiter = GlobalRateLimiter(requests_per_second)

        def task(index: int, url: str) -> tuple[int, bytes | None]:
            try:
                return (
                    index,
                    fetch_bytes(
                        url,
                        timeout_s=timeout_s,
                        max_retries=max_retries,
                        backoff_s=backoff_s,
                        limiter=limiter,
                    ),
                )
            except Exception:
                if raise_on_error:
                    raise
                return index, None

        with ThreadPoolExecutor(max_workers=max_workers) as executor:
            futures = {executor.submit(task, index, url): index for index, url in enumerate(url_list)}
            for future in as_completed(futures):
                index, payload = future.result()
                results[index] = payload

        return results

    return (fetch_image_contents,)


@app.cell
def _(Path, fetch_image_contents, pl):
    def infer_output_path(source_csv):
        source = Path(source_csv)
        return source.with_name(f"{source.stem.replace('scrapper_data', 'structured_scrapper_data')}.parquet")

    def load_scrapper_frame(source_csv):
        frame = pl.read_csv(source_csv).filter(pl.col("type") != "Video")
        return frame.with_row_index("_row")


    def build_structured_scrapper_frame(
        source_csv,
        *,
        output_parquet=None,
        fetch_images: bool = True,
        max_workers: int = 16,
        requests_per_second: float = 5,
        timeout_s: float = 20,
        max_retries: int = 2,
        backoff_s: float = 0.5,
    ) -> pl.DataFrame:
        frame = load_scrapper_frame(source_csv)

        if fetch_images:
            urls = frame.get_column("displayUrl").to_list()
            image_bytes = fetch_image_contents(
                urls,
                max_workers=max_workers,
                requests_per_second=requests_per_second,
                timeout_s=timeout_s,
                max_retries=max_retries,
                backoff_s=backoff_s,
                raise_on_error=False,
            )
            image_frame = pl.DataFrame({"_row": list(range(len(image_bytes))), "post_img_data": image_bytes}).with_columns(
                pl.col("post_img_data").cast(pl.Binary)
            )
            frame = frame.join(image_frame, on="_row", how="left")
        else:
            frame = frame.with_columns(pl.lit(None, dtype=pl.Binary).alias("post_img_data"))

        structured = frame.select(
            pl.col("ownerId").alias("id"),
            pl.col("ownerUsername").alias("username"),
            pl.col("id").alias("post_id"),
            pl.col("url").alias("post_url"),
            pl.col("caption").alias("post_caption"),
            pl.col("likesCount").alias("post_likes"),
            pl.col("commentsCount").alias("post_comments"),
            pl.col("displayUrl").alias("post_img_url"),
            pl.col("post_img_data").alias("post_img_data"),
            pl.col("type").alias("post_type"),
            pl.col("timestamp").alias("post_created_at"),
        )

        if output_parquet is not None:
            structured.write_parquet(output_parquet)

        return structured

    return build_structured_scrapper_frame, infer_output_path


@app.cell
def _(build_structured_scrapper_frame, infer_output_path):
    source_csv = "scrapper_data.csv"

    df = build_structured_scrapper_frame(
        source_csv,
        output_parquet=infer_output_path(source_csv),
        fetch_images=True,
        requests_per_second=5,
    )
    return


if __name__ == "__main__":
    app.run()
