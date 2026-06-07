from __future__ import annotations

import argparse
import ast
from pathlib import Path
import re
from typing import Iterable


REQUIRED_COLUMNS = {
    "likes",
    "comments",
    "engagement_total",
    "predominant_color",
    "color_category",
    "color_temperature",
    "mean_luminosity",
    "mean_saturation",
}


def _import_pandas():
    import pandas as pd

    return pd


def _import_plotting():
    import matplotlib.pyplot as plt
    import seaborn as sns

    return plt, sns


def parse_rgb_tuple(value: object) -> tuple[int, int, int] | None:
    if not isinstance(value, str) or not value.strip():
        return None

    if "np." in value:
        numbers = re.findall(r"np\.\w+\((-?\d+)\)", value)
        if len(numbers) != 3:
            return None
        r, g, b = (int(numbers[0]), int(numbers[1]), int(numbers[2]))
    else:
        cleaned = value.strip()

        try:
            parsed = ast.literal_eval(cleaned)
        except (ValueError, SyntaxError):
            return None

        if not isinstance(parsed, tuple) or len(parsed) != 3:
            return None

        try:
            r, g, b = (int(parsed[0]), int(parsed[1]), int(parsed[2]))
        except (TypeError, ValueError):
            return None

    if any(channel < 0 or channel > 255 for channel in (r, g, b)):
        return None

    return r, g, b


def load_and_clean_data(csv_path: Path):
    pd = _import_pandas()
    df = pd.read_csv(csv_path)

    missing_columns = REQUIRED_COLUMNS - set(df.columns)
    if missing_columns:
        raise ValueError(
            f"Missing required columns in {csv_path}: {sorted(missing_columns)}"
        )

    df = df.copy()
    df["engagement_total"] = pd.to_numeric(df["engagement_total"], errors="coerce")
    df["likes"] = pd.to_numeric(df["likes"], errors="coerce")
    df["comments"] = pd.to_numeric(df["comments"], errors="coerce")
    df["mean_luminosity"] = pd.to_numeric(df["mean_luminosity"], errors="coerce")
    df["mean_saturation"] = pd.to_numeric(df["mean_saturation"], errors="coerce")

    df.dropna(subset=["likes", "comments", "engagement_total"], inplace=True)

    rgb_values = df["predominant_color"].apply(parse_rgb_tuple)
    df["predominant_r"] = rgb_values.apply(lambda rgb: rgb[0] if rgb else None)
    df["predominant_g"] = rgb_values.apply(lambda rgb: rgb[1] if rgb else None)
    df["predominant_b"] = rgb_values.apply(lambda rgb: rgb[2] if rgb else None)

    return df


def _save_bar_plot(df, group_col: str, value_col: str, output_path: Path):
    plt, sns = _import_plotting()
    plt.figure(figsize=(12, 6))
    ordered = (
        df.groupby(group_col, dropna=False)[value_col]
        .mean()
        .sort_values(ascending=False)
        .reset_index()
    )
    sns.barplot(data=ordered, x=group_col, y=value_col, palette="viridis", hue=group_col)
    plt.xticks(rotation=45, ha="right")
    plt.tight_layout()
    plt.savefig(output_path, dpi=200)
    plt.close()


def _save_box_plot(df, group_col: str, value_col: str, output_path: Path):
    plt, sns = _import_plotting()
    plt.figure(figsize=(12, 6))
    sns.boxplot(data=df, x=group_col, y=value_col, palette="Set3", hue=group_col)
    plt.xticks(rotation=45, ha="right")
    plt.tight_layout()
    plt.savefig(output_path, dpi=200)
    plt.close()


def _save_scatter_plot(df, x_col: str, y_col: str, output_path: Path):
    plt, sns = _import_plotting()
    plt.figure(figsize=(10, 6))
    sns.scatterplot(data=df, x=x_col, y=y_col, hue="color_category", alpha=0.7)
    plt.tight_layout()
    plt.savefig(output_path, dpi=200)
    plt.close()


def _save_heatmap(df, columns: Iterable[str], output_path: Path):
    plt, sns = _import_plotting()
    plt.figure(figsize=(8, 6))
    corr = df[list(columns)].corr(numeric_only=True)
    sns.heatmap(corr, annot=True, cmap="coolwarm", fmt=".2f")
    plt.tight_layout()
    plt.savefig(output_path, dpi=200)
    plt.close()


def generate_visualizations(df, output_dir: Path, prefix: str):
    output_dir.mkdir(parents=True, exist_ok=True)

    _save_bar_plot(df, "color_category", "engagement_total", output_dir / f"{prefix}_bar_color_category_engagement.png")
    _save_bar_plot(df, "color_temperature", "engagement_total", output_dir / f"{prefix}_bar_color_temperature_engagement.png")

    temp = df.copy()
    temp["luminosity_bin"] = temp["mean_luminosity"].round(-1)
    temp["saturation_bin"] = temp["mean_saturation"].round(-1)

    _save_bar_plot(temp, "luminosity_bin", "engagement_total", output_dir / f"{prefix}_bar_luminosity_engagement.png")
    _save_bar_plot(temp, "saturation_bin", "engagement_total", output_dir / f"{prefix}_bar_saturation_engagement.png")

    _save_box_plot(df, "color_category", "engagement_total", output_dir / f"{prefix}_box_color_category_engagement.png")
    _save_scatter_plot(df, "mean_luminosity", "engagement_total", output_dir / f"{prefix}_scatter_luminosity_engagement.png")
    _save_scatter_plot(df, "mean_saturation", "engagement_total", output_dir / f"{prefix}_scatter_saturation_engagement.png")
    _save_heatmap(
        df,
        [
            "likes",
            "comments",
            "engagement_total",
            "mean_luminosity",
            "mean_saturation",
            "predominant_r",
            "predominant_g",
            "predominant_b",
        ],
        output_dir / f"{prefix}_heatmap_correlations.png",
    )


def run_analysis(csv_path: Path, output_dir: Path, sample_size: int | None = None):
    df = load_and_clean_data(csv_path)
    if sample_size:
        df = df.head(sample_size)

    generate_visualizations(df, output_dir, "full_dataset")

    for segment in ["fast", "luxury"]:
        segment_df = df[df["type"].str.lower() == segment].copy() if "type" in df.columns else df.iloc[0:0]
        if not segment_df.empty:
            generate_visualizations(segment_df, output_dir, f"{segment}_segment")

    if "username" in df.columns:
        for brand, brand_df in df.groupby("username"):
            if len(brand_df) >= 5:
                safe_brand = str(brand).strip().lower().replace(" ", "_")
                generate_visualizations(brand_df, output_dir, f"brand_{safe_brand}")

    cleaned_path = output_dir / "cleaned_dataset.csv"
    df.to_csv(cleaned_path, index=False)

    print(f"Dataset shape after cleaning: {df.shape}")
    print(f"Columns: {df.columns.tolist()}")
    print(f"Saved outputs to: {output_dir}")


def resolve_default_csv(repo_root: Path) -> Path:
    preferred = repo_root / "image_analysis_results_full_fast.csv"
    fallback = repo_root / "image_analysis_full.csv"
    if preferred.exists():
        return preferred
    if fallback.exists():
        return fallback
    raise FileNotFoundError(
        "Could not find image_analysis_results_full_fast.csv or image_analysis_full.csv"
    )


def main():
    parser = argparse.ArgumentParser(description="Start full fast dataset visualization implementation")
    parser.add_argument("--csv", type=Path, default=None, help="Path to CSV dataset")
    parser.add_argument(
        "--output-dir",
        type=Path,
        default=Path("visualization_outputs"),
        help="Directory for generated visualizations",
    )
    parser.add_argument(
        "--sample-size",
        type=int,
        default=None,
        help="Optional cap for quick/manual verification",
    )
    args = parser.parse_args()

    csv_path = args.csv if args.csv else resolve_default_csv(Path.cwd())
    run_analysis(csv_path=csv_path, output_dir=args.output_dir, sample_size=args.sample_size)


if __name__ == "__main__":
    main()
