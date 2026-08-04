import marimo

__generated_with = "0.23.15"
app = marimo.App()


@app.cell
def _():
    import re
    import ast
    from pathlib import Path
    from collections.abc import Iterable, Sequence

    import numpy as np
    import pandas as pd
    import seaborn as sns
    import matplotlib.pyplot as plt
    import plotly.graph_objects as go

    return Iterable, Path, Sequence, ast, go, np, pd, plt, re, sns


@app.cell
def _(Iterable, Path, Sequence, ast, pd, plt, re, sns):
    REQUIRED_COLUMNS = {
        "likes",
        "comments",
        "predominant_color",
        "color_category",
        "color_temperature",
        "mean_luminosity",
        "mean_saturation",
        "luminosity_category",
        "saturation_category",
    }

    def semantic_palette(values: Iterable[object]) -> dict[object, str]:
        color_lookup = {
            "achromatic": "#7f7f7f",
            "balanced": "#8a60b0",
            "black": "#1f1f1f",
            "blue": "#1f77b4",
            "chromatic": "#f28e2b",
            "cool": "#4c78a8",
            "cyan": "#17becf",
            "gray": "#7f7f7f",
            "grey": "#7f7f7f",
            "green": "#2ca02c",
            "magenta": "#e377c2",
            "mixed": "#8a60b0",
            "neutral": "#8c8c8c",
            "orange": "#ff7f0e",
            "pink": "#ff69b4",
            "purple": "#9467bd",
            "red": "#d62728",
            "white": "#f2f2f2",
            "warm": "#ff8c42",
            "yellow": "#f2c744",
        }
        unique_values = list(dict.fromkeys(values))
        fallback_colors = sns.color_palette("deep", max(len(unique_values), 1))
        palette: dict[object, str] = {}
        for value, fallback_color in zip(unique_values, fallback_colors):
            normalized = str(value).strip().lower()
            palette[value] = color_lookup.get(normalized, fallback_color)
        return palette

    def set_visual_theme() -> None:
        sns.set_theme(style="whitegrid", context="talk")
        plt.rcParams.update({
            "font.family": "DejaVu Sans",
            "font.sans-serif": ["DejaVu Sans"],
            "text.usetex": False,
        })
        plt.rcParams["figure.figsize"] = (12, 6)

    def _filter_columns(frame: pd.DataFrame, columns: Sequence[str]) -> list[str]:
        return [column for column in columns if column in frame.columns]

    def save_figure(
        fig: plt.Figure, output_path: Path | None = None, *, dpi: int = 160
    ):
        if output_path is not None:
            fig.savefig(output_path, dpi=dpi, bbox_inches="tight")
        return fig

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

    return (
        REQUIRED_COLUMNS,
        parse_rgb_tuple,
        save_figure,
        semantic_palette,
        set_visual_theme,
    )


@app.cell
def _(Path, REQUIRED_COLUMNS, parse_rgb_tuple, pd):
    def load_and_clean_data(csv_path: Path) -> pd.DataFrame:
        df = pd.read_csv(csv_path)

        missing_columns = REQUIRED_COLUMNS - set(df.columns)
        if missing_columns:
            raise ValueError(
                f"Missing required columns in {csv_path}: {sorted(missing_columns)}"
            )

        df = df.copy()
        df["likes"] = pd.to_numeric(df["likes"], errors="coerce")
        df["comments"] = pd.to_numeric(df["comments"], errors="coerce")
        df["mean_luminosity"] = pd.to_numeric(df["mean_luminosity"], errors="coerce")
        df["mean_saturation"] = pd.to_numeric(df["mean_saturation"], errors="coerce")

        if "engagement_total" in df.columns:
            df["engagement_total"] = pd.to_numeric(
                df["engagement_total"], errors="coerce"
            )
        else:
            df["engagement_total"] = df["likes"] + df["comments"]

        df.dropna(subset=["likes", "comments", "engagement_total"], inplace=True)

        rgb_values = df["predominant_color"].apply(parse_rgb_tuple)
        df["predominant_r"] = rgb_values.apply(lambda rgb: rgb[0] if rgb else None)
        df["predominant_g"] = rgb_values.apply(lambda rgb: rgb[1] if rgb else None)
        df["predominant_b"] = rgb_values.apply(lambda rgb: rgb[2] if rgb else None)

        return df

    return (load_and_clean_data,)


@app.cell
def _(Path, Sequence, go, np, pd, plt, save_figure, semantic_palette, sns):
    def plot_metric_distributions(
        frame: pd.DataFrame,
        columns: Sequence[str],
        *,
        bins: int = 30,
        ncols: int = 3,
        output_path: Path | None = None,
    ):
        available = _filter_columns(frame, columns)
        if not available:
            raise ValueError("No matching columns were found for plotting")

        nrows = int(np.ceil(len(available) / ncols))
        fig, axes = plt.subplots(nrows, ncols, figsize=(6 * ncols, 4.5 * nrows))
        axes = np.array(axes).reshape(-1)

        palette = sns.color_palette("Blues", len(available))
        for index, column in enumerate(available):
            axes[index].hist(
                frame[column].dropna(),
                bins=bins,
                edgecolor="black",
                alpha=0.8,
                color=palette[index],
            )
            axes[index].set_title(f"{column} distribution")
            axes[index].set_xlabel(column)
            axes[index].set_ylabel("Count")

        for axis in axes[len(available) :]:
            axis.set_visible(False)

        fig.tight_layout()
        return save_figure(fig, output_path)

    def plot_rgb_channels(
        frame: pd.DataFrame,
        *,
        channels: Sequence[str] = ("red", "green", "blue"),
        output_path: Path | None = None,
    ):
        return plot_metric_distributions(
            frame,
            channels,
            ncols=len(channels),
            output_path=output_path,
        )

    def plot_group_boxplots(
        frame: pd.DataFrame,
        group_col: str,
        target_cols: Sequence[str] = ("likes", "engagement_total"),
        *,
        output_path: Path | None = None,
    ):
        available_targets = _filter_columns(frame, target_cols)
        if group_col not in frame.columns or not available_targets:
            raise ValueError("The requested group or target columns are not available")

        fig, axes = plt.subplots(
            1, len(available_targets), figsize=(8 * len(available_targets), 6)
        )
        if len(available_targets) == 1:
            axes = [axes]

        for axis, column in zip(axes, available_targets):
            frame.boxplot(column=column, by=group_col, ax=axis)
            axis.set_title(f"{column} by {group_col}")
            axis.set_xlabel(group_col)
            axis.set_ylabel(column)
            axis.tick_params(axis="x", rotation=45)

        fig.suptitle("")
        fig.tight_layout()
        return save_figure(fig, output_path)

    def plot_scatter_grid(
        frame: pd.DataFrame,
        x_cols: Sequence[str],
        y_col: str,
        *,
        ncols: int = 3,
        trendline: bool = True,
        output_path: Path | None = None,
    ):
        available_x = _filter_columns(frame, x_cols)
        if y_col not in frame.columns or not available_x:
            raise ValueError("The requested scatter plot columns are not available")

        nrows = int(np.ceil(len(available_x) / ncols))
        fig, axes = plt.subplots(nrows, ncols, figsize=(6 * ncols, 4.5 * nrows))
        axes = np.array(axes).reshape(-1)

        for index, x_col in enumerate(available_x):
            axis = axes[index]
            subset = frame[[x_col, y_col]].dropna()
            axis.scatter(subset[x_col], subset[y_col], alpha=0.55, s=18)
            axis.set_xlabel(x_col)
            axis.set_ylabel(y_col)
            axis.set_title(f"{x_col} vs {y_col}")

            if trendline and len(subset) > 1:
                slope, intercept = np.polyfit(subset[x_col], subset[y_col], 1)
                x_values = np.linspace(subset[x_col].min(), subset[x_col].max(), 100)
                axis.plot(
                    x_values,
                    slope * x_values + intercept,
                    color="red",
                    linewidth=2,
                    alpha=0.8,
                )

        for axis in axes[len(available_x) :]:
            axis.set_visible(False)

        fig.tight_layout()
        return save_figure(fig, output_path)

    def plot_group_means(
        frame: pd.DataFrame,
        group_col: str,
        target_col: str = "likes",
        *,
        sort_desc: bool = True,
        output_path: Path | None = None,
    ):
        if group_col not in frame.columns or target_col not in frame.columns:
            raise ValueError("The requested group or target column is not available")

        means = (
            frame
            .groupby(group_col)[target_col]
            .mean()
            .sort_values(ascending=not sort_desc)
        )
        fig, ax = plt.subplots(figsize=(12, max(5, 0.4 * len(means))))
        palette = semantic_palette(means.index.tolist())
        ax.barh(
            range(len(means)),
            means.values,
            color=[palette[value] for value in means.index],
        )
        ax.set_yticks(range(len(means)))
        ax.set_yticklabels(means.index)
        ax.set_xlabel(f"Average {target_col}")
        ax.set_title(f"Average {target_col} by {group_col}")
        ax.grid(axis="x", alpha=0.3)
        fig.subplots_adjust(left=0.24, right=0.98, top=0.90, bottom=0.16)
        return save_figure(fig, output_path)

    ACHROMATIC_HUES = {"Black", "White", "Gray"}

    def chromaticity_category(color_category: object) -> str:
        """Collapse hue-like color categories into achromatic/chromatic."""
        return "achromatic" if color_category in ACHROMATIC_HUES else "chromatic"

    def _tercile_label(value: float, low: float, high: float) -> str:
        if pd.isna(value):
            return "neutral"
        if value <= low:
            return "low"
        if value >= high:
            return "high"
        return "neutral"

    def add_visual_cohort_columns(frame: pd.DataFrame) -> pd.DataFrame:
        """Attach the columns used by the engagement Sankey diagram."""
        required = {
            "type",
            "username",
            "color_category",
            "color_temperature",
            "saturation_category",
            "luminosity_category",
        }
        missing = required - set(frame.columns)
        if missing:
            raise ValueError(f"Missing Sankey columns: {sorted(missing)}")

        enriched = frame.copy()
        enriched["chromaticity"] = enriched["color_category"].apply(
            chromaticity_category
        )
        return enriched

    def _spread_positions(count: int, start: float, stop: float) -> list[float]:
        if count <= 1:
            return [(start + stop) / 2]
        return np.linspace(start, stop, count).tolist()

    def build_engagement_sankey(
        frame: pd.DataFrame,
        *,
        engagement_col: str = "engagement_total",
        output_path: Path | None = None,
    ) -> go.Figure:
        """Build a Sankey with color -> chromaticity -> temperature and parallel bands."""
        enriched = add_visual_cohort_columns(frame)
        required = {
            "type",
            "username",
            "chromaticity",
            "color_temperature",
            "saturation_category",
            "luminosity_category",
            engagement_col,
        }
        missing = required - set(enriched.columns)
        if missing:
            raise ValueError(f"Missing Sankey columns: {sorted(missing)}")

        def order_values(column: str, values: list[str]) -> list[str]:
            if column == "chromaticity":
                preferred = ["achromatic", "chromatic"]
            elif column in {"saturation_category", "luminosity_category"}:
                preferred = ["low", "neutral", "high"]
            elif column == "color_temperature":
                preferred = ["warm", "cool"]
            else:
                preferred = []

            ordered = [value for value in preferred if value in values]
            ordered.extend([value for value in values if value not in preferred])
            return ordered

        node_labels: list[str] = []
        node_x: list[float] = []
        node_y: list[float] = []
        stage_to_index: dict[str, int] = {}

        def add_node(key: str, label: str, x: float, y: float) -> int:
            if key in stage_to_index:
                return stage_to_index[key]
            index = len(node_labels)
            stage_to_index[key] = index
            node_labels.append(label)
            node_x.append(x)
            node_y.append(y)
            return index

        type_values = order_values(
            "type",
            [str(value) for value in enriched["type"].dropna().unique().tolist()],
        )
        brand_values = order_values(
            "username",
            [str(value) for value in enriched["username"].dropna().unique().tolist()],
        )

        for value, y_position in zip(
            type_values, _spread_positions(len(type_values), 0.35, 0.65)
        ):
            add_node(f"type::{value}", value, 0.02, y_position)

        for value, y_position in zip(
            brand_values, _spread_positions(len(brand_values), 0.10, 0.90)
        ):
            add_node(f"username::{value}", value, 0.22, y_position)

        branch_values = order_values("branch", ["color", "saturation", "luminosity"])
        for value, y_position in zip(
            branch_values, _spread_positions(len(branch_values), 0.18, 0.82)
        ):
            add_node(f"branch::{value}", value, 0.46, y_position)

        color_nodes = order_values(
            "chromaticity",
            [
                str(value)
                for value in enriched["chromaticity"].dropna().unique().tolist()
            ],
        )
        saturation_nodes = order_values(
            "saturation_category",
            [
                str(value)
                for value in enriched["saturation_category"].dropna().unique().tolist()
            ],
        )
        luminosity_nodes = order_values(
            "luminosity_category",
            [
                str(value)
                for value in enriched["luminosity_category"].dropna().unique().tolist()
            ],
        )
        temperature_nodes = order_values(
            "color_temperature",
            [
                str(value)
                for value in enriched["color_temperature"].dropna().unique().tolist()
            ],
        )

        for value, y_position in zip(
            color_nodes, _spread_positions(len(color_nodes), 0.28, 0.72)
        ):
            add_node(f"chromaticity::{value}", value, 0.70, y_position)

        for value, y_position in zip(
            saturation_nodes, _spread_positions(len(saturation_nodes), 0.12, 0.88)
        ):
            add_node(f"saturation_category::{value}", value, 0.70, y_position)

        for value, y_position in zip(
            luminosity_nodes, _spread_positions(len(luminosity_nodes), 0.12, 0.88)
        ):
            add_node(f"luminosity_category::{value}", value, 0.70, y_position)

        for value, y_position in zip(
            temperature_nodes, _spread_positions(len(temperature_nodes), 0.28, 0.72)
        ):
            add_node(f"color_temperature::{value}", value, 0.94, y_position)

        source_nodes: list[int] = []
        target_nodes: list[int] = []
        link_values: list[float] = []

        def add_link(source_key: str, target_key: str, value: float) -> None:
            source_nodes.append(stage_to_index[source_key])
            target_nodes.append(stage_to_index[target_key])
            link_values.append(float(max(value, 0.0)))

        type_brand = (
            enriched
            .groupby(["type", "username"], dropna=False)[engagement_col]
            .mean()
            .reset_index()
        )
        for _, row in type_brand.iterrows():
            if pd.isna(row["type"]) or pd.isna(row["username"]):
                continue
            add_link(
                f"type::{row['type']}",
                f"username::{row['username']}",
                row[engagement_col],
            )

        branch_factor = 3.0
        brand_means = (
            enriched
            .groupby("username", dropna=False)[engagement_col]
            .mean()
            .reset_index()
        )
        for _, row in brand_means.iterrows():
            if pd.isna(row["username"]):
                continue
            brand_key = f"username::{row['username']}"
            for branch in ("color", "saturation", "luminosity"):
                add_link(
                    brand_key, f"branch::{branch}", row[engagement_col] / branch_factor
                )

        chromaticity_means = (
            enriched
            .groupby("chromaticity", dropna=False)[engagement_col]
            .mean()
            .reset_index()
        )
        for _, row in chromaticity_means.iterrows():
            if pd.isna(row["chromaticity"]):
                continue
            add_link(
                "branch::color",
                f"chromaticity::{row['chromaticity']}",
                row[engagement_col],
            )

        temperature_means = (
            enriched
            .groupby(["chromaticity", "color_temperature"], dropna=False)[
                engagement_col
            ]
            .mean()
            .reset_index()
        )
        for _, row in temperature_means.iterrows():
            if pd.isna(row["chromaticity"]) or pd.isna(row["color_temperature"]):
                continue
            add_link(
                f"chromaticity::{row['chromaticity']}",
                f"color_temperature::{row['color_temperature']}",
                row[engagement_col],
            )

        for branch, category_column in (
            ("saturation", "saturation_category"),
            ("luminosity", "luminosity_category"),
        ):
            grouped = (
                enriched
                .groupby(category_column, dropna=False)[engagement_col]
                .mean()
                .reset_index()
            )
            for _, row in grouped.iterrows():
                if pd.isna(row[category_column]):
                    continue
                add_link(
                    f"branch::{branch}",
                    f"{category_column}::{row[category_column]}",
                    row[engagement_col],
                )

        figure = go.Figure(
            data=[
                go.Sankey(
                    arrangement="snap",
                    node={
                        "label": node_labels,
                        "x": node_x,
                        "y": node_y,
                        "pad": 18,
                        "thickness": 16,
                        "line": {"color": "#2a2a2a", "width": 0.5},
                    },
                    link={
                        "source": source_nodes,
                        "target": target_nodes,
                        "value": link_values,
                        "color": "rgba(120, 144, 184, 0.35)",
                    },
                )
            ]
        )
        figure.update_layout(
            title="Average engagement flow: brand type → brand → color → chromaticity → temperature",
            font_size=12,
            height=620,
            margin={"l": 16, "r": 16, "t": 60, "b": 16},
        )

        if output_path is not None:
            figure.write_html(str(output_path))
        return figure

    def build_visual_report(
        frame: pd.DataFrame,
        *,
        numeric_columns: Sequence[str],
        group_col: str = "color_category",
        target_col: str = "likes",
        output_dir: Path | None = None,
    ):
        output_path = Path(output_dir) if output_dir is not None else None
        figures = {
            "distributions": plot_metric_distributions(
                frame,
                numeric_columns,
                output_path=output_path / "metric_distributions.png"
                if output_path is not None
                else None,
            ),
            "rgb_channels": plot_rgb_channels(
                frame,
                output_path=output_path / "rgb_channels.png"
                if output_path is not None
                else None,
            )
            if {"red", "green", "blue"}.issubset(frame.columns)
            else None,
            "boxplots": plot_group_boxplots(
                frame,
                group_col,
                (target_col, "engagement_total")
                if "engagement_total" in frame.columns
                else (target_col,),
                output_path=output_path / f"{group_col}_boxplots.png"
                if output_path is not None
                else None,
            )
            if group_col in frame.columns
            else None,
            "scatter_grid": plot_scatter_grid(
                frame,
                [column for column in numeric_columns if column != target_col],
                target_col,
                output_path=output_path / f"{target_col}_scatter_grid.png"
                if output_path is not None
                else None,
            ),
            "group_means": plot_group_means(
                frame,
                group_col,
                target_col,
                output_path=output_path / f"{group_col}_means.png"
                if output_path is not None
                else None,
            )
            if group_col in frame.columns
            else None,
        }
        return figures

    def generate_visualizations(df: pd.DataFrame, output_dir: Path, prefix: str):
        output_dir.mkdir(parents=True, exist_ok=True)

        fig = plot_group_means(
            df,
            "color_category",
            "engagement_total",
            output_path=output_dir / f"{prefix}_bar_color_category_engagement.png",
        )
        plt.close(fig)

        fig = plot_group_means(
            df,
            "color_temperature",
            "engagement_total",
            output_path=output_dir / f"{prefix}_bar_color_temperature_engagement.png",
        )
        plt.close(fig)

        build_engagement_sankey(
            df,
            output_path=output_dir / f"{prefix}_sankey_engagement_cohorts.html",
        )

    return (generate_visualizations,)


@app.cell
def _(Path, generate_visualizations, load_and_clean_data, set_visual_theme):
    def run_analysis(csv_path: Path, output_dir: Path, sample_size: int | None = None):
        df = load_and_clean_data(csv_path)
        if sample_size is not None:
            df = df.head(sample_size)

        set_visual_theme()

        generate_visualizations(df, output_dir, "full_dataset")

        for segment in ["fast", "luxury"]:
            segment_df = (
                df[df["type"].str.lower() == segment].copy()
                if "type" in df.columns
                else df.iloc[0:0]
            )
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

    return (run_analysis,)


@app.cell
def _(Path, run_analysis):
    run_analysis(Path("image_analysis_full.csv"), Path("visualization_outputs"))
    return


if __name__ == "__main__":
    app.run()
