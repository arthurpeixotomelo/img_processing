import marimo

__generated_with = "0.23.15"
app = marimo.App()


@app.cell
def _():
    from pathlib import Path
    from collections import Counter

    import cv2
    import numpy as np
    import polars as pl
    from sklearn.cluster import KMeans

    return Counter, KMeans, Path, cv2, np, pl


@app.cell
def _(Counter, KMeans, cv2, np):
    def decode_image_bytes(img_bytes):
        """Decode image bytes into an OpenCV BGR image."""
        if img_bytes is None:
            raise ValueError("img_bytes is None")
        buffer = (
            img_bytes if isinstance(img_bytes, (bytes, bytearray)) else bytes(img_bytes)
        )
        array = np.frombuffer(buffer, dtype=np.uint8)
        image = cv2.imdecode(array, cv2.IMREAD_COLOR)
        if image is None:
            raise ValueError("Failed to decode image bytes")
        return image

    def calculate_luminosity(image):
        gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        return {
            "mean_luminosity": float(np.mean(gray)),
            "median_luminosity": float(np.median(gray)),
            "std_luminosity": float(np.std(gray)),
            "min_luminosity": int(np.min(gray)),
            "max_luminosity": int(np.max(gray)),
        }

    def calculate_saturation(image):
        hsv = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)
        saturation = hsv[:, :, 1]
        return {
            "median_saturation": float(np.median(saturation)),
            "mean_saturation": float(np.mean(saturation)),
            "std_saturation": float(np.std(saturation)),
            "min_saturation": int(np.min(saturation)),
            "max_saturation": int(np.max(saturation)),
        }

    def get_predominant_colors(image, n_colors=5, max_pixels=20_000):
        rgb_image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
        pixels = rgb_image.reshape(-1, 3)

        if len(pixels) > max_pixels:
            rng = np.random.default_rng(42)
            indices = rng.choice(len(pixels), size=max_pixels, replace=False)
            pixels_fit = pixels[indices]
        else:
            pixels_fit = pixels

        kmeans = KMeans(n_clusters=n_colors, random_state=42, n_init=10)
        kmeans.fit(pixels_fit)

        colors = kmeans.cluster_centers_.astype(int)
        labels = kmeans.labels_
        label_counts = Counter(labels)
        total_pixels = len(pixels_fit)

        color_info = []
        for index in range(n_colors):
            percentage = (label_counts.get(index, 0) / total_pixels) * 100
            color_info.append({
                "color_rgb": tuple(colors[index]),
                "percentage": float(percentage),
            })

        color_info.sort(key=lambda value: value["percentage"], reverse=True)
        return {
            "predominant_color": color_info[0]["color_rgb"],
            "predominant_color_percentage": color_info[0]["percentage"],
            "all_colors": color_info,
        }

    def get_color_category(rgb_color):
        r, g, b = rgb_color
        r_norm, g_norm, b_norm = r / 255.0, g / 255.0, b / 255.0
        max_val = max(r_norm, g_norm, b_norm)
        min_val = min(r_norm, g_norm, b_norm)
        diff = max_val - min_val
        saturation = 0 if max_val == 0 else diff / max_val
        value = max_val

        if diff == 0:
            hue = 0
        elif max_val == r_norm:
            hue = 60 * (((g_norm - b_norm) / diff) % 6)
        elif max_val == g_norm:
            hue = 60 * (((b_norm - r_norm) / diff) + 2)
        else:
            hue = 60 * (((r_norm - g_norm) / diff) + 4)

        if saturation < 0.15:
            if value < 0.2:
                return "Black"
            if value > 0.8:
                return "White"
            return "Gray"

        if hue < 15 or hue >= 345:
            return "Red"
        if 15 <= hue < 45:
            return "Orange"
        if 45 <= hue < 75:
            return "Yellow"
        if 75 <= hue < 165:
            return "Green"
        if 165 <= hue < 195:
            return "Cyan"
        if 195 <= hue < 255:
            return "Blue"
        if 255 <= hue < 285:
            return "Purple"
        if 285 <= hue < 315:
            return "Magenta"
        return "Pink"

    def get_color_temperature(rgb_color):
        r, g, b = rgb_color
        warm_score = (r * 1.0 + g * 0.5) / 2
        cool_score = (b * 1.0 + g * 0.3) / 2
        return "warm" if warm_score > cool_score else "cool"

    # Luminosity and saturation are 0-255 byte ranges (grayscale / HSV S channel).
    # Bands split at the 1st and 3rd quartiles of that range so labels are stable,
    # interpretable for non-technical readers, and independent of dataset skew.
    _LUMINOSITY_LOW_THRESHOLD = 85
    _LUMINOSITY_HIGH_THRESHOLD = 170
    _SATURATION_LOW_THRESHOLD = 85
    _SATURATION_HIGH_THRESHOLD = 170

    def get_luminosity_category(mean_luminosity):
        """Categorize mean luminosity into low/neutral/high bands (0-255 grayscale)."""
        if mean_luminosity < _LUMINOSITY_LOW_THRESHOLD:
            return "low"
        if mean_luminosity > _LUMINOSITY_HIGH_THRESHOLD:
            return "high"
        return "neutral"

    def get_saturation_category(mean_saturation):
        """Categorize mean saturation into low/neutral/high bands (0-255 HSV S channel)."""
        if mean_saturation < _SATURATION_LOW_THRESHOLD:
            return "low"
        if mean_saturation > _SATURATION_HIGH_THRESHOLD:
            return "high"
        return "neutral"

    def analyze_post_row(row, n_colors=5, max_pixels=20_000):
        try:
            image_bgr = decode_image_bytes(row.get("post_img_data"))
            height, width, channels = image_bgr.shape
            luminosity = calculate_luminosity(image_bgr)
            saturation = calculate_saturation(image_bgr)
            colors = get_predominant_colors(
                image_bgr, n_colors=n_colors, max_pixels=max_pixels
            )
            predominant_rgb = colors["predominant_color"]

            post_id = row.get("post_id")
            username = row.get("username")
            filename = (
                str(post_id)
                if post_id is not None
                else str(row.get("post_img_url", "unknown"))
            )
            if username:
                filename = f"{username}_{filename}"

            return {
                "filename": filename,
                "type": row.get("type"),
                "post_id": post_id,
                "username": username,
                "post_url": row.get("post_url"),
                "post_img_url": row.get("post_img_url"),
                "post_created_at": row.get("post_created_at"),
                "likes": row.get("likes"),
                "comments": row.get("comments"),
                "width": int(width),
                "height": int(height),
                "channels": int(channels),
                **luminosity,
                **saturation,
                **colors,
                "color_category": get_color_category(predominant_rgb),
                "color_temperature": get_color_temperature(predominant_rgb),
                "luminosity_category": get_luminosity_category(
                    luminosity["mean_luminosity"]
                ),
                "saturation_category": get_saturation_category(
                    saturation["mean_saturation"]
                ),
            }
        except Exception as exc:
            print(f"Error analyzing post_id={row.get('post_id')}: {exc}")
            return None

    print("Helper functions defined successfully!")
    return (analyze_post_row,)


@app.cell
def _(Path, analyze_post_row, pl):
    def load_structured_parquets(parquet_pattern="structured_scrapper_data.parquet"):
        parquet_files = sorted(Path(".").glob(parquet_pattern))
        if not parquet_files:
            raise FileNotFoundError(
                f"No parquet files found for pattern: {parquet_pattern}"
            )

        frames = []
        for path in parquet_files:
            frame = pl.read_parquet(path)
            brand_type = (
                "fast"
                if "fast" in path.stem
                else ("luxury" if "luxury" in path.stem else None)
            )
            if brand_type is not None and "type" not in frame.columns:
                frame = frame.with_columns(pl.lit(brand_type).alias("type"))
            frames.append(frame)

        # combined = frames[0]
        # for frame in frames[1:]:
        #     combined = combined.vstack(frame)
        combined = pl.concat(frames, how="vertical")

        return combined, parquet_files

    def normalize_scrape_frame(frame: pl.DataFrame) -> pl.DataFrame:
        cols = set(frame.columns)

        def pick(name, candidates):
            for candidate in candidates:
                if candidate in cols:
                    return candidate
            raise ValueError(
                f"Missing '{name}'. Tried {candidates}. Found: {sorted(cols)}"
            )

        post_id_col = pick("post_id", ["post_id", "id"])
        username_col = pick("username", ["username", "ownerUsername"])
        likes_col = pick("likes", ["post_likes", "likesCount", "post_likesCount"])
        comments_col = pick(
            "comments", ["post_comments", "commentsCount", "post_commentsCount"]
        )
        img_col = pick("post_img_data", ["post_img_data"])
        img_url_col = pick("post_img_url", ["post_img_url", "displayUrl"])
        type_col = "type" if "type" in cols else None
        post_url_col = (
            "post_url" if "post_url" in cols else ("url" if "url" in cols else None)
        )
        created_col = (
            "post_created_at"
            if "post_created_at" in cols
            else ("timestamp" if "timestamp" in cols else None)
        )

        select_cols = [
            post_id_col,
            username_col,
            likes_col,
            comments_col,
            img_col,
            img_url_col,
        ]
        if type_col:
            select_cols.append(type_col)
        if post_url_col:
            select_cols.append(post_url_col)
        if created_col:
            select_cols.append(created_col)

        rename_map = {
            post_id_col: "post_id",
            username_col: "username",
            likes_col: "likes",
            comments_col: "comments",
            img_col: "post_img_data",
            img_url_col: "post_img_url",
        }
        if type_col:
            rename_map[type_col] = "type"
        if post_url_col:
            rename_map[post_url_col] = "post_url"
        if created_col:
            rename_map[created_col] = "post_created_at"

        normalized = (
            frame
            .select(select_cols)
            .rename(rename_map)
            .with_columns([
                pl.col("likes").cast(pl.Int64),
                pl.col("comments").cast(pl.Int64),
            ])
            .filter(pl.col("post_img_data").is_not_null())
        )

        return normalized

    def analyze_dataset(frame: pl.DataFrame, n_colors=5, max_pixels=20_000):
        results = []
        failed = 0
        total = frame.height

        for index, row in enumerate(frame.iter_rows(named=True), 1):
            if index % 25 == 0 or index == 1 or index == total:
                print(f"Analyzing {index}/{total}...")

            result = analyze_post_row(row, n_colors=n_colors, max_pixels=max_pixels)
            if result is None:
                failed += 1
                continue
            results.append(result)

        print(f"Successfully analyzed {len(results)} images.")
        print(f"Failed: {failed}")
        return pl.DataFrame(results)

    print("Dataset helpers defined successfully!")
    return analyze_dataset, load_structured_parquets, normalize_scrape_frame


@app.cell
def _(load_structured_parquets, normalize_scrape_frame):
    # Load every structured parquet produced by step 1 and concatenate them.
    scrape_df, parquet_files = load_structured_parquets()
    print("Parquet inputs:")
    for path in parquet_files:
        print(f"- {path}")

    print("\nColumns in concatenated parquet:")
    print(scrape_df.columns)

    scrape_df = normalize_scrape_frame(scrape_df)
    print(f"\nRows with image bytes: {scrape_df.height}")
    print(f"Columns after normalization: {scrape_df.columns}")
    return (scrape_df,)


@app.cell
def _(analyze_dataset, scrape_df):
    analysis_df = analyze_dataset(
        scrape_df,
        n_colors=5,
        max_pixels=20_000,
    )

    # Keep the dataframe available for downstream analysis and export.
    print(f"\nAnalysis dataframe shape: {analysis_df.shape}")
    analysis_df.head()
    return (analysis_df,)


@app.cell
def _(analysis_df):
    # Add engagement total metric for downstream notebooks.
    if {"likes", "comments"}.issubset(analysis_df.columns):
        analysis_df["engagement_total"] = analysis_df["likes"] + analysis_df["comments"]

    # Convert predominant_color tuple to string for CSV export and downstream reads.
    if "predominant_color" in analysis_df.columns:
        analysis_df["predominant_color"] = analysis_df["predominant_color"].apply(str)

    analysis_df.to_csv("image_analysis_full.csv", index=False)
    return


if __name__ == "__main__":
    app.run()
