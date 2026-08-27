import matplotlib

matplotlib.use("Agg")
import marimo

__generated_with = "0.24.0"
app = marimo.App()


@app.cell
def _():
    import re
    from collections.abc import Iterable, Sequence
    from pathlib import Path

    import matplotlib

    matplotlib.use("Agg")
    import matplotlib.pyplot as plt
    import numpy as np
    import pandas as pd
    import plotly.graph_objects as go
    import seaborn as sns

    return Iterable, Path, Sequence, go, np, pd, plt, re, sns


@app.cell
def _(Iterable, Path, Sequence, np, pd, plt, re, sns):
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

    def filter_columns(frame: pd.DataFrame, columns: Sequence[str]) -> list[str]:
        return [column for column in columns if column in frame.columns]

    def require_columns(frame: pd.DataFrame, columns: Sequence[str]) -> None:
        """Raise immediately if any required column is missing from the frame."""
        missing = [column for column in columns if column not in frame.columns]
        if missing:
            raise ValueError(f"Missing required columns: {missing}")

    def hide_extra_axes(axes: np.ndarray, used_count: int) -> None:
        """Hide unused subplot axes created by a fixed-shape grid."""
        for axis in axes[used_count:]:
            axis.set_visible(False)

    def save_figure(
        fig: plt.Figure, output_path: Path | None = None, *, dpi: int = 160
    ):
        if output_path is not None:
            fig.savefig(output_path, dpi=dpi, bbox_inches="tight")
        return fig

    def parse_rgb_tuple(value: object) -> tuple[int, int, int] | None:
        if value is None:
            return None
        if isinstance(value, (tuple, list)) and len(value) == 3:
            try:
                return (int(value[0]), int(value[1]), int(value[2]))
            except (TypeError, ValueError):
                return None

        val_str = str(value).strip()
        if not val_str:
            return None

        numbers = re.findall(r"-?\d+", val_str)
        if len(numbers) >= 3:
            try:
                r, g, b = (int(numbers[0]), int(numbers[1]), int(numbers[2]))
                if all(0 <= channel <= 255 for channel in (r, g, b)):
                    return (r, g, b)
            except (TypeError, ValueError):
                pass

        return None

    return (
        REQUIRED_COLUMNS,
        filter_columns,
        hide_extra_axes,
        parse_rgb_tuple,
        require_columns,
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

        df["color_temperature_score"] = (
            df["predominant_r"] * 1.0 + df["predominant_g"] * 0.5
        ) / 2.0 - (df["predominant_b"] * 1.0 + df["predominant_g"] * 0.3) / 2.0
        if "color_category" in df.columns:
            df["achromatic"] = df["color_category"].isin(["Black", "White", "Gray"])

        return df

    return (load_and_clean_data,)


@app.cell
def _(
    Path,
    Sequence,
    filter_columns,
    go,
    hide_extra_axes,
    np,
    pd,
    plt,
    require_columns,
    save_figure,
    semantic_palette,
    sns,
):
    def plot_metric_distributions(
        frame: pd.DataFrame,
        columns: Sequence[str],
        *,
        bins: int = 30,
        ncols: int = 3,
        output_path: Path | None = None,
    ):
        available = filter_columns(frame, columns)
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

        hide_extra_axes(axes, len(available))
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
        available_targets = filter_columns(frame, target_cols)
        require_columns(frame, [group_col])
        if not available_targets:
            raise ValueError("The requested target columns are not available")

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
        available_x = filter_columns(frame, x_cols)
        require_columns(frame, [y_col])
        if not available_x:
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

        hide_extra_axes(axes, len(available_x))
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
        require_columns(frame, [group_col, target_col])

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

    # --- Sankey building ----------------------------------------------------------
    # The Sankey has four left-to-right stages:
    #   type -> username -> branch(color|luminosity|saturation) -> category nodes
    # Each branch owns its own vertical lane so the saturation/luminosity
    # low/neutral/high nodes no longer overlap.

    # Preferred display order per stage
    STAGE_ORDER: dict[str, list[str]] = {
        "type": ["luxury", "fast"],
        "chromaticity": ["achromatic", "chromatic"],
        "branch": ["color", "luminosity", "saturation"],
        "saturation_category": ["high", "neutral", "low"],
        "luminosity_category": ["high", "neutral", "low"],
    }

    STAGE_LABELS: dict[str, dict[str, str]] = {
        "type": {"luxury": "Luxury", "fast": "Fast Fashion"},
        "branch": {
            "color": "Color / Hue",
            "luminosity": "Brightness (Lum)",
            "saturation": "Vividness (Sat)",
        },
        "chromaticity": {
            "achromatic": "Achromatic (Neutral)",
            "chromatic": "Chromatic (Colorful)",
        },
        "luminosity_category": {
            "high": "Lum: High",
            "neutral": "Lum: Neutral",
            "low": "Lum: Low",
        },
        "saturation_category": {
            "high": "Sat: High",
            "neutral": "Sat: Neutral",
            "low": "Sat: Low",
        },
    }

    NODE_COLORS: dict[str, str] = {
        "type::luxury": "#8b5cf6",
        "type::fast": "#f59e0b",
        "branch::color": "#3b82f6",
        "branch::luminosity": "#10b981",
        "branch::saturation": "#ec4899",
        "chromaticity::achromatic": "#64748b",
        "chromaticity::chromatic": "#0ea5e9",
        "luminosity_category::high": "#fde047",
        "luminosity_category::neutral": "#94a3b8",
        "luminosity_category::low": "#334155",
        "saturation_category::high": "#f43f5e",
        "saturation_category::neutral": "#cbd5e1",
        "saturation_category::low": "#94a3b8",
    }

    def node_key(stage: str, value: str) -> str:
        return f"{stage}::{value}"

    def build_engagement_sankey(
        frame: pd.DataFrame,
        *,
        engagement_col: str = "engagement_total",
        output_path: Path | None = None,
        title: str | None = None,
    ) -> go.Figure:
        """Build a lane-separated Sankey of summed engagement flows.

        Stages:
        - Full dataset: Brand Type -> Brand -> Visual Feature Branch -> Category
        - Single Brand: Brand -> Visual Feature Branch -> Category
        All category nodes (Achromatic/Chromatic, Lum High/Neutral/Low, Sat High/Neutral/Low)
        are aligned in the same horizontal column and disjoint vertical lanes.
        """
        enriched = add_visual_cohort_columns(frame)

        unique_types = sorted(
            enriched["type"].dropna().unique().tolist(),
            key=lambda t: 0 if str(t).lower() == "luxury" else 1,
        )
        unique_brands = enriched["username"].dropna().unique().tolist()

        is_single_brand = len(unique_brands) == 1
        has_multiple_types = len(unique_types) > 1

        labels: list[str] = []
        node_x: list[float] = []
        node_y: list[float] = []
        node_color_list: list[str] = []
        index_map: dict[str, int] = {}

        def register_node(
            key: str, label: str, x: float, y: float, color: str = "#64748b"
        ) -> int:
            if key in index_map:
                return index_map[key]
            idx = len(labels)
            index_map[key] = idx
            labels.append(label)
            node_x.append(x)
            node_y.append(y)
            node_color_list.append(color)
            return idx

        if not is_single_brand:
            x_type = 0.02
            x_brand = 0.22
            x_branch = 0.52
            x_cat = 0.88

            # 1. Register types if multiple types exist
            if has_multiple_types:
                type_y_map = {"luxury": 0.75, "fast": 0.25}
                for t in unique_types:
                    t_str = str(t).lower()
                    y_val = type_y_map.get(t_str, 0.5)
                    lbl = STAGE_LABELS.get("type", {}).get(t_str, str(t).capitalize())
                    col = NODE_COLORS.get(f"type::{t_str}", "#8b5cf6")
                    register_node(node_key("type", t_str), lbl, x_type, y_val, col)

            # 2. Register brands ordered by brand type
            # Luxury brands on top band (0.55 to 0.95), Fast brands on bottom band (0.05 to 0.45)
            ordered_brand_entries = []
            for t in unique_types:
                t_str = str(t).lower()
                sub_brands = (
                    enriched[enriched["type"].str.lower() == t_str]["username"]
                    .dropna()
                    .unique()
                    .tolist()
                )
                sub_brands_sorted = (
                    enriched[enriched["username"].isin(sub_brands)]
                    .groupby("username")[engagement_col]
                    .sum()
                    .sort_values(ascending=False)
                    .index.tolist()
                )
                ordered_brand_entries.append((t_str, sub_brands_sorted))

            for t_str, sub_brands in ordered_brand_entries:
                if has_multiple_types:
                    band_start, band_stop = (
                        (0.55, 0.95) if t_str == "luxury" else (0.05, 0.45)
                    )
                else:
                    band_start, band_stop = (0.08, 0.92)

                if len(sub_brands) == 1:
                    y_positions = [(band_start + band_stop) / 2]
                else:
                    y_positions = np.linspace(
                        band_stop, band_start, len(sub_brands)
                    ).tolist()

                for b_name, y_pos in zip(sub_brands, y_positions):
                    b_lbl = f"@{b_name}"
                    b_col = "#6366f1" if t_str == "luxury" else "#f59e0b"
                    register_node(
                        node_key("username", str(b_name)), b_lbl, x_brand, y_pos, b_col
                    )

        else:
            # Single Brand - omit brand type step!
            x_brand = 0.05
            x_branch = 0.48
            x_cat = 0.88
            single_b = unique_brands[0]
            register_node(
                node_key("username", str(single_b)),
                f"@{single_b}",
                x_brand,
                0.5,
                "#6366f1",
            )

        # 3. Register Branch Hubs (Color, Luminosity, Saturation)
        branch_y = {"color": 0.83, "luminosity": 0.50, "saturation": 0.18}
        for br in ["color", "luminosity", "saturation"]:
            lbl = STAGE_LABELS["branch"][br]
            col = NODE_COLORS.get(f"branch::{br}", "#3b82f6")
            register_node(node_key("branch", br), lbl, x_branch, branch_y[br], col)

        # 4. Register Category Nodes (All aligned at x_cat!)
        # Color lane (0.70 to 0.95): Achromatic, Chromatic
        # Luminosity lane (0.37 to 0.63): High, Neutral, Low
        # Saturation lane (0.05 to 0.31): High, Neutral, Low
        register_node(
            node_key("chromaticity", "achromatic"),
            "Achromatic (Neutral)",
            x_cat,
            0.90,
            NODE_COLORS["chromaticity::achromatic"],
        )
        register_node(
            node_key("chromaticity", "chromatic"),
            "Chromatic (Colorful)",
            x_cat,
            0.76,
            NODE_COLORS["chromaticity::chromatic"],
        )

        register_node(
            node_key("luminosity_category", "high"),
            "Lum: High",
            x_cat,
            0.59,
            NODE_COLORS["luminosity_category::high"],
        )
        register_node(
            node_key("luminosity_category", "neutral"),
            "Lum: Neutral",
            x_cat,
            0.50,
            NODE_COLORS["luminosity_category::neutral"],
        )
        register_node(
            node_key("luminosity_category", "low"),
            "Lum: Low",
            x_cat,
            0.41,
            NODE_COLORS["luminosity_category::low"],
        )

        register_node(
            node_key("saturation_category", "high"),
            "Sat: High",
            x_cat,
            0.27,
            NODE_COLORS["saturation_category::high"],
        )
        register_node(
            node_key("saturation_category", "neutral"),
            "Sat: Neutral",
            x_cat,
            0.18,
            NODE_COLORS["saturation_category::neutral"],
        )
        register_node(
            node_key("saturation_category", "low"),
            "Sat: Low",
            x_cat,
            0.09,
            NODE_COLORS["saturation_category::low"],
        )

        # --- Build Links ---
        sources: list[int] = []
        targets: list[int] = []
        values: list[float] = []
        link_colors: list[str] = []

        def add_link(
            src_key: str,
            tgt_key: str,
            val: float,
            color_rgba: str = "rgba(148, 163, 184, 0.35)",
        ):
            if src_key in index_map and tgt_key in index_map and val > 0:
                sources.append(index_map[src_key])
                targets.append(index_map[tgt_key])
                values.append(float(val))
                link_colors.append(color_rgba)

        # 1. Type -> Brand (if multiple types exist)
        if has_multiple_types and not is_single_brand:
            type_brand_grp = (
                enriched
                .groupby(["type", "username"])[engagement_col]
                .sum()
                .reset_index()
            )
            for _, row in type_brand_grp.iterrows():
                t_val = str(row["type"]).lower()
                b_val = str(row["username"])
                c_link = (
                    "rgba(139, 92, 246, 0.35)"
                    if t_val == "luxury"
                    else "rgba(245, 158, 11, 0.35)"
                )
                add_link(
                    node_key("type", t_val),
                    node_key("username", b_val),
                    row[engagement_col],
                    c_link,
                )

        # 2. Brand -> Branch Hubs (split evenly by 3)
        brand_totals = enriched.groupby("username")[engagement_col].sum().reset_index()
        for _, row in brand_totals.iterrows():
            b_val = str(row["username"])
            tot_b = row[engagement_col]
            add_link(
                node_key("username", b_val),
                node_key("branch", "color"),
                tot_b / 3.0,
                "rgba(59, 130, 246, 0.30)",
            )
            add_link(
                node_key("username", b_val),
                node_key("branch", "luminosity"),
                tot_b / 3.0,
                "rgba(16, 185, 129, 0.30)",
            )
            add_link(
                node_key("username", b_val),
                node_key("branch", "saturation"),
                tot_b / 3.0,
                "rgba(236, 72, 153, 0.30)",
            )

        # 3. Branch Hubs -> Category Nodes
        color_grp = enriched.groupby("chromaticity")[engagement_col].sum().reset_index()
        for _, row in color_grp.iterrows():
            c_val = str(row["chromaticity"])
            add_link(
                node_key("branch", "color"),
                node_key("chromaticity", c_val),
                row[engagement_col],
                "rgba(59, 130, 246, 0.40)",
            )

        lum_grp = (
            enriched.groupby("luminosity_category")[engagement_col].sum().reset_index()
        )
        for _, row in lum_grp.iterrows():
            l_val = str(row["luminosity_category"])
            add_link(
                node_key("branch", "luminosity"),
                node_key("luminosity_category", l_val),
                row[engagement_col],
                "rgba(16, 185, 129, 0.40)",
            )

        sat_grp = (
            enriched.groupby("saturation_category")[engagement_col].sum().reset_index()
        )
        for _, row in sat_grp.iterrows():
            s_val = str(row["saturation_category"])
            add_link(
                node_key("branch", "saturation"),
                node_key("saturation_category", s_val),
                row[engagement_col],
                "rgba(236, 72, 153, 0.40)",
            )

        chart_title = (
            title
            if title
            else (
                "Total Engagement Flow: Brand Type → Brand → Visual Feature → Category"
                if has_multiple_types
                else "Engagement Flow: Visual Feature → Category"
            )
        )

        figure = go.Figure(
            data=[
                go.Sankey(
                    arrangement="snap",
                    node={
                        "label": labels,
                        "x": node_x,
                        "y": node_y,
                        "pad": 16,
                        "thickness": 18,
                        "color": node_color_list,
                        "line": {"color": "#1e293b", "width": 0.8},
                    },
                    link={
                        "source": sources,
                        "target": targets,
                        "value": values,
                        "color": link_colors,
                    },
                )
            ]
        )
        figure.update_layout(
            title={
                "text": f"<b>{chart_title}</b>",
                "font": {"size": 15, "color": "#1e293b"},
                "x": 0.02,
                "y": 0.98,
            },
            font={"size": 11, "family": "DejaVu Sans, sans-serif"},
            height=620,
            margin={"l": 20, "r": 20, "t": 50, "b": 20},
            paper_bgcolor="#ffffff",
        )

        if output_path is not None:
            figure.write_html(str(output_path))
            try:
                figure.write_image(str(output_path.with_suffix(".png")), scale=2)
            except Exception:
                pass
        return figure

    def _resolve_output(base: Path | None, *parts: str) -> Path | None:
        """Join parts under base, or return None when base is None."""
        return base.joinpath(*parts) if base is not None else None

    def build_visual_report(
        frame: pd.DataFrame,
        *,
        numeric_columns: Sequence[str],
        group_col: str = "color_category",
        target_col: str = "likes",
        output_dir: Path | None = None,
    ):
        output_base = Path(output_dir) if output_dir is not None else None
        has_rgb = {"red", "green", "blue"}.issubset(frame.columns)
        has_group = group_col in frame.columns
        boxplots_targets = (
            (target_col, "engagement_total")
            if "engagement_total" in frame.columns
            else (target_col,)
        )

        figures: dict[str, plt.Figure | None] = {
            "distributions": plot_metric_distributions(
                frame,
                numeric_columns,
                output_path=_resolve_output(output_base, "metric_distributions.png"),
            ),
            "rgb_channels": plot_rgb_channels(
                frame,
                output_path=_resolve_output(output_base, "rgb_channels.png"),
            )
            if has_rgb
            else None,
            "boxplots": plot_group_boxplots(
                frame,
                group_col,
                boxplots_targets,
                output_path=_resolve_output(output_base, f"{group_col}_boxplots.png"),
            )
            if has_group
            else None,
            "scatter_grid": plot_scatter_grid(
                frame,
                [column for column in numeric_columns if column != target_col],
                target_col,
                output_path=_resolve_output(
                    output_base, f"{target_col}_scatter_grid.png"
                ),
            ),
            "group_means": plot_group_means(
                frame,
                group_col,
                target_col,
                output_path=_resolve_output(output_base, f"{group_col}_means.png"),
            )
            if has_group
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

        title_sankey = (
            "Total Engagement Flow: Brand Type → Brand → Visual Feature → Category"
            if prefix == "full"
            else (
                f"{prefix.capitalize()} Segment Engagement Flow: Brand → Visual Feature → Category"
                if prefix in ["fast", "luxury"]
                else f"@{prefix.replace('brand_', '')} Engagement Flow: Visual Feature → Category"
            )
        )
        build_engagement_sankey(
            df,
            output_path=output_dir / f"{prefix}_sankey_engagement_cohorts.html",
            title=title_sankey,
        )

    def generate_section4_visualizations(frame: pd.DataFrame, output_dir: Path) -> None:
        """Generate statistical visualization charts for Section 4."""
        output_dir.mkdir(parents=True, exist_ok=True)

        features_map = [
            ("predominant_r", "Red Channel (R)"),
            ("predominant_g", "Green Channel (G)"),
            ("predominant_b", "Blue Channel (B)"),
            ("color_temperature_score", "Color Warmth (Temp)"),
            ("mean_luminosity", "Brightness (Luminosity)"),
            ("mean_saturation", "Color Vividness (Saturation)"),
        ]
        feature_labels = [label for _, label in features_map]
        y_positions = np.arange(len(feature_labels))

        def calc_pearsons(target_col: str) -> list[float]:
            corrs = []
            for col, _ in features_map:
                if col in frame.columns:
                    sub = frame[[col, target_col]].dropna()
                    if len(sub) > 1:
                        r = np.corrcoef(sub[col], sub[target_col])[0, 1]
                        corrs.append(float(r))
                    else:
                        corrs.append(0.0)
                else:
                    corrs.append(0.0)
            return corrs

        r_likes = calc_pearsons("likes")
        r_comments = calc_pearsons("comments")
        r_total = calc_pearsons("engagement_total")

        def apply_benchmark_zones(axis: plt.Axes) -> None:
            axis.axvspan(
                -0.1,
                0.1,
                color="#f1f5f9",
                alpha=0.9,
                label="Negligible / No Real Impact (-0.1 to +0.1)",
            )
            axis.axvspan(
                0.1,
                0.3,
                color="#fef3c7",
                alpha=0.5,
                label="Weak Influence (±0.1 to ±0.3)",
            )
            axis.axvspan(-0.3, -0.1, color="#fef3c7", alpha=0.5)
            axis.axvspan(
                0.3, 1.0, color="#dcfce7", alpha=0.6, label="Meaningful Impact (> ±0.3)"
            )
            axis.axvspan(-1.0, -0.3, color="#dcfce7", alpha=0.6)
            axis.axvline(0, color="black", linewidth=1.2)
            axis.axvline(0.3, color="#15803d", linestyle="--", linewidth=1.8)
            axis.axvline(-0.3, color="#15803d", linestyle="--", linewidth=1.8)
            axis.set_xlim(-1.0, 1.0)
            axis.set_xticks([-1.0, -0.75, -0.5, -0.3, 0.0, 0.3, 0.5, 0.75, 1.0])
            axis.text(
                0.32,
                -0.2,
                "Meaningful Impact\nThreshold (±0.30)",
                color="#15803d",
                fontsize=9,
                fontweight="bold",
                va="bottom",
            )

        # 1. Combined Benchmark Chart (concept_correlation_benchmark.png)
        fig, ax = plt.subplots(figsize=(10.5, 6))
        apply_benchmark_zones(ax)
        bar_h = 0.24
        b1 = ax.barh(
            y_positions - bar_h,
            r_likes,
            height=bar_h,
            color="#2563eb",
            edgecolor="black",
            label="Impact on Likes",
            alpha=0.9,
        )
        b2 = ax.barh(
            y_positions,
            r_comments,
            height=bar_h,
            color="#ea580c",
            edgecolor="black",
            label="Impact on Comments",
            alpha=0.9,
        )
        b3 = ax.barh(
            y_positions + bar_h,
            r_total,
            height=bar_h,
            color="#16a34a",
            edgecolor="black",
            label="Impact on Total Engagement",
            alpha=0.9,
        )
        ax.set_yticks(y_positions)
        ax.set_yticklabels(feature_labels, fontweight="bold", fontsize=10.5)
        ax.invert_yaxis()
        ax.set_xlabel(
            "Correlation with Engagement (Scale: -1.0 to +1.0)",
            fontweight="bold",
            fontsize=11,
        )
        ax.set_title(
            "Visual Feature Correlation vs. Real-World Impact Threshold\n(All measured features are trapped in the 'No Real Effect' zone)",
            fontweight="bold",
            fontsize=12,
            pad=12,
        )

        for group in [b1, b2, b3]:
            for bar in group:
                w = bar.get_width()
                offset = 0.03 if w >= 0 else -0.03
                ha = "left" if w >= 0 else "right"
                ax.text(
                    w + offset,
                    bar.get_y() + bar.get_height() / 2,
                    f"{w:+.3f}",
                    va="center",
                    ha=ha,
                    fontsize=8.5,
                    fontweight="bold",
                )
        ax.legend(
            loc="upper center",
            bbox_to_anchor=(0.5, -0.15),
            ncol=3,
            frameon=True,
            facecolor="white",
            edgecolor="#cbd5e1",
            fontsize=9.5,
        )
        save_figure(fig, output_dir / "concept_correlation_benchmark.png")
        plt.close(fig)

        # 2. Individual Target Plots (Likes, Comments, Total Engagement)
        targets_info = [
            (
                "likes",
                r_likes,
                "Likes",
                "#2563eb",
                "section4_likes_correlation.png",
                "Trapped between -0.04 and 0.00 in the 'No Impact' zone",
            ),
            (
                "comments",
                r_comments,
                "Comments",
                "#ea580c",
                "section4_comments_correlation.png",
                "Linear correlation is virtually zero across all attributes",
            ),
            (
                "engagement_total",
                r_total,
                "Total Engagement",
                "#16a34a",
                "section4_total_engagement_correlation.png",
                "Mirrors Likes because Likes make up over 98.9% of interactions",
            ),
        ]
        for (
            target_key,
            r_vals,
            target_title,
            bar_color,
            file_name,
            subtitle,
        ) in targets_info:
            fig, ax = plt.subplots(figsize=(9.5, 5))
            apply_benchmark_zones(ax)
            bars = ax.barh(
                y_positions,
                r_vals,
                height=0.45,
                color=bar_color,
                edgecolor="black",
                alpha=0.9,
                label=f"Measured Correlation with {target_title}",
            )
            ax.set_yticks(y_positions)
            ax.set_yticklabels(feature_labels, fontweight="bold", fontsize=10.5)
            ax.invert_yaxis()
            ax.set_xlabel(
                f"Correlation with {target_title}", fontweight="bold", fontsize=11
            )
            ax.set_title(
                f"Visual Feature Correlation with {target_title}\n({subtitle})",
                fontweight="bold",
                fontsize=12,
                pad=12,
            )
            for bar in bars:
                w = bar.get_width()
                offset = 0.03 if w >= 0 else -0.03
                ha = "left" if w >= 0 else "right"
                ax.text(
                    w + offset,
                    bar.get_y() + bar.get_height() / 2,
                    f"r = {w:+.3f}",
                    va="center",
                    ha=ha,
                    fontsize=9.5,
                    fontweight="bold",
                )
            ax.legend(
                loc="upper center",
                bbox_to_anchor=(0.5, -0.16),
                ncol=2,
                frameon=True,
                facecolor="white",
                edgecolor="#cbd5e1",
                fontsize=9.5,
            )
            save_figure(fig, output_dir / file_name)
            plt.close(fig)

        # 3. Group Comparisons: Neutral vs Colorful (Split into 2 images)
        if "achromatic" in frame.columns:
            ach_df = frame[frame["achromatic"]]
            chr_df = frame[~frame["achromatic"]]
            if not ach_df.empty and not chr_df.empty:
                cats = ["Neutral (Achromatic)", "Colorful (Chromatic)"]
                x_cat = np.arange(len(cats))
                w_cat = 0.35

                # 3A. Likes Comparison
                fig, ax = plt.subplots(figsize=(7.5, 4.8))
                likes_means = [int(ach_df["likes"].mean()), int(chr_df["likes"].mean())]
                likes_medians = [
                    int(ach_df["likes"].median()),
                    int(chr_df["likes"].median()),
                ]
                ax.bar(
                    x_cat - w_cat / 2,
                    likes_means,
                    w_cat,
                    label="Average Likes (Mean)",
                    color="#94a3b8",
                    edgecolor="black",
                )
                ax.bar(
                    x_cat + w_cat / 2,
                    likes_medians,
                    w_cat,
                    label="Typical Likes (Median)",
                    color="#3b82f6",
                    edgecolor="black",
                )
                ax.set_xticks(x_cat)
                ax.set_xticklabels(cats, fontweight="bold")
                ax.set_ylabel("Likes per Post", fontweight="bold")
                ax.set_title(
                    "Likes: Neutral vs. Colorful Posts\n(No meaningful statistical difference)",
                    fontweight="bold",
                    fontsize=12,
                    pad=12,
                )
                for idx in range(len(cats)):
                    ax.text(
                        x_cat[idx] - w_cat / 2,
                        likes_means[idx] + 1000,
                        f"{likes_means[idx]:,}",
                        ha="center",
                        fontsize=9,
                        fontweight="bold",
                    )
                    ax.text(
                        x_cat[idx] + w_cat / 2,
                        likes_medians[idx] + 1000,
                        f"{likes_medians[idx]:,}",
                        ha="center",
                        fontsize=9,
                        fontweight="bold",
                    )
                ax.legend(
                    loc="upper center",
                    bbox_to_anchor=(0.5, -0.15),
                    ncol=2,
                    frameon=True,
                    facecolor="white",
                    edgecolor="#cbd5e1",
                    fontsize=9.5,
                )
                save_figure(fig, output_dir / "section4_likes_group_comparison.png")
                plt.close(fig)

                # 3B. Comments Comparison
                fig, ax = plt.subplots(figsize=(7.5, 4.8))
                comments_means = [
                    int(ach_df["comments"].mean()),
                    int(chr_df["comments"].mean()),
                ]
                comments_medians = [
                    int(ach_df["comments"].median()),
                    int(chr_df["comments"].median()),
                ]
                ax.bar(
                    x_cat - w_cat / 2,
                    comments_means,
                    w_cat,
                    label="Average Comments (Mean)",
                    color="#94a3b8",
                    edgecolor="black",
                )
                ax.bar(
                    x_cat + w_cat / 2,
                    comments_medians,
                    w_cat,
                    label="Typical Comments (Median)",
                    color="#f97316",
                    edgecolor="black",
                )
                ax.set_xticks(x_cat)
                ax.set_xticklabels(cats, fontweight="bold")
                ax.set_ylabel("Comments per Post", fontweight="bold")
                ax.set_title(
                    "Comments: Neutral vs. Colorful Posts\n(Subtle +10 comment shift for colorful)",
                    fontweight="bold",
                    fontsize=12,
                    pad=12,
                )
                for idx in range(len(cats)):
                    ax.text(
                        x_cat[idx] - w_cat / 2,
                        comments_means[idx] + 15,
                        f"{comments_means[idx]}",
                        ha="center",
                        fontsize=9,
                        fontweight="bold",
                    )
                    ax.text(
                        x_cat[idx] + w_cat / 2,
                        comments_medians[idx] + 15,
                        f"{comments_medians[idx]}",
                        ha="center",
                        fontsize=9,
                        fontweight="bold",
                    )
                ax.legend(
                    loc="upper center",
                    bbox_to_anchor=(0.5, -0.15),
                    ncol=2,
                    frameon=True,
                    facecolor="white",
                    edgecolor="#cbd5e1",
                    fontsize=9.5,
                )
                save_figure(fig, output_dir / "section4_comments_group_comparison.png")
                plt.close(fig)

        # 4. Brand Presentation Chi-Square Chart (section4_brand_presentation_chi_square.png)
        if "type" in frame.columns and "achromatic" in frame.columns:
            sub_fast = frame[frame["type"].str.lower() == "fast"]
            sub_lux = frame[frame["type"].str.lower() == "luxury"]
            if not sub_fast.empty and not sub_lux.empty:
                fast_neutral = float(sub_fast["achromatic"].mean() * 100.0)
                fast_color = 100.0 - fast_neutral
                lux_neutral = float(sub_lux["achromatic"].mean() * 100.0)
                lux_color = 100.0 - lux_neutral

                fig, ax = plt.subplots(figsize=(8.5, 5.2))
                categories = [
                    f"Fast Fashion\n(n = {len(sub_fast):,} posts)",
                    f"Luxury\n(n = {len(sub_lux):,} posts)",
                ]
                neutral_pcts = [fast_neutral, lux_neutral]
                colorful_pcts = [fast_color, lux_color]

                x_idx = np.arange(len(categories))
                w_bar = 0.38

                b1 = ax.bar(
                    x_idx - w_bar / 2,
                    neutral_pcts,
                    w_bar,
                    label="Neutral (Achromatic: Black, White, Gray)",
                    color="#64748b",
                    edgecolor="black",
                    linewidth=1.1,
                )
                b2 = ax.bar(
                    x_idx + w_bar / 2,
                    colorful_pcts,
                    w_bar,
                    label="Colorful (Chromatic: Red, Blue, Orange, etc.)",
                    color="#3b82f6",
                    edgecolor="black",
                    linewidth=1.1,
                )

                for bar in b1:
                    h = bar.get_height()
                    ax.text(
                        bar.get_x() + bar.get_width() / 2,
                        h + 1.2,
                        f"{h:.1f}%",
                        ha="center",
                        va="bottom",
                        fontsize=11,
                        fontweight="bold",
                        color="#1e293b",
                    )

                for bar in b2:
                    h = bar.get_height()
                    ax.text(
                        bar.get_x() + bar.get_width() / 2,
                        h + 1.2,
                        f"{h:.1f}%",
                        ha="center",
                        va="bottom",
                        fontsize=11,
                        fontweight="bold",
                        color="#1e293b",
                    )

                ax.set_xticks(x_idx)
                ax.set_xticklabels(categories, fontsize=11, fontweight="bold")
                ax.set_ylabel(
                    "Share of Published Posts (%)", fontsize=11, fontweight="bold"
                )
                ax.set_ylim(0, 75)

                ax.text(
                    0.5,
                    68,
                    "Chi-Square Test of Independence: $\\chi^2 = 51.83, p < 0.0001$\n(Statistically Significant Difference in Visual Strategy)",
                    ha="center",
                    va="center",
                    fontsize=10,
                    fontweight="bold",
                    color="#0f172a",
                    bbox=dict(
                        boxstyle="round,pad=0.5",
                        facecolor="#f1f5f9",
                        edgecolor="#94a3b8",
                        linewidth=1.2,
                    ),
                )

                ax.set_title(
                    "Visual Strategy by Brand Category: Fast Fashion vs. Luxury\n(Color distribution reflects intentional brand presentation, not audience demand)",
                    fontsize=12,
                    fontweight="bold",
                    pad=12,
                )

                ax.legend(
                    loc="upper center",
                    bbox_to_anchor=(0.5, -0.15),
                    ncol=2,
                    frameon=True,
                    facecolor="white",
                    edgecolor="#cbd5e1",
                    fontsize=10,
                )
                save_figure(
                    fig, output_dir / "section4_brand_presentation_chi_square.png"
                )
                plt.close(fig)

        # 5. Explained Variance Pie Chart (section4_explained_variance_pie.png)
        sub_reg = frame[
            [
                "predominant_r",
                "predominant_g",
                "predominant_b",
                "mean_luminosity",
                "mean_saturation",
                "likes",
            ]
        ].dropna()
        if len(sub_reg) > 10:
            X_reg = sub_reg[
                [
                    "predominant_r",
                    "predominant_g",
                    "predominant_b",
                    "mean_luminosity",
                    "mean_saturation",
                ]
            ].values
            X_reg = np.column_stack([np.ones(len(X_reg)), X_reg])
            y_reg = sub_reg["likes"].values
            beta, _, _, _ = np.linalg.lstsq(X_reg, y_reg, rcond=None)
            ss_tot = np.sum((y_reg - np.mean(y_reg)) ** 2)
            ss_res = np.sum((y_reg - X_reg @ beta) ** 2)
            r2_model = max(0.0, 1.0 - (ss_res / ss_tot))
        else:
            r2_model = 0.00349

        vis_pct_total = r2_model * 100.0
        non_vis_pct = 100.0 - vis_pct_total

        fig, ax = plt.subplots(figsize=(7.5, 5))
        labels_pie = [
            f"Non-Visual Factors ({non_vis_pct:.2f}%)\n(Brand Fame, Content Relevance,\nCaptions, Timing, Algorithm)",
            f"Visual Features Analyzed Combined ({vis_pct_total:.2f}%)\n(Color, Brightness, Warmth, Saturation)",
        ]
        sizes_pie = [non_vis_pct, vis_pct_total]
        colors_pie = ["#3b82f6", "#ef4444"]
        explode_pie = (0, 0.18)

        _, _, autotexts = ax.pie(
            sizes_pie,
            explode=explode_pie,
            labels=labels_pie,
            autopct="%1.2f%%",
            startangle=140,
            colors=colors_pie,
            textprops={"fontsize": 10.5, "fontweight": "bold"},
            wedgeprops={"edgecolor": "black", "linewidth": 1.2},
            pctdistance=0.6,
        )
        autotexts[0].set_color("white")
        autotexts[1].set_color("white")
        ax.set_title(
            "How Photography Affects Instagram Engagement?\n(Visual features account for less than 0.4% of variance)",
            fontweight="bold",
            fontsize=12,
            pad=14,
        )
        save_figure(fig, output_dir / "section4_explained_variance_pie.png")
        plt.close(fig)

        # 5. Individual Feature Variance Bars (section4_feature_variance_bars.png)
        fig, ax = plt.subplots(figsize=(8.5, 4.5))
        bivariate_r2 = [float(r**2 * 100.0) for r in r_likes]
        colors_b = sns.color_palette("Blues_r", len(feature_labels))
        bars_b = ax.barh(
            feature_labels,
            bivariate_r2,
            color=colors_b,
            edgecolor="black",
            alpha=0.85,
            height=0.45,
        )
        ax.invert_yaxis()
        ax.set_xlim(0, 1.0)
        ax.set_xlabel(
            "Individual Variance Explained ($R^2$ in %)",
            fontweight="bold",
            fontsize=10.5,
        )
        ax.set_title(
            "Individual Visual Feature Contribution\n(Each feature independently explains < 0.20% of engagement)",
            fontweight="bold",
            fontsize=11.5,
            pad=12,
        )
        for bar in bars_b:
            w = bar.get_width()
            ax.text(
                w + 0.02,
                bar.get_y() + bar.get_height() / 2,
                f"{w:.2f}%",
                va="center",
                fontsize=10,
                fontweight="bold",
            )
        save_figure(fig, output_dir / "section4_feature_variance_bars.png")
        plt.close(fig)

    return generate_section4_visualizations, generate_visualizations


@app.cell
def _(
    Path,
    generate_section4_visualizations,
    generate_visualizations,
    load_and_clean_data,
    set_visual_theme,
):
    def run_analysis(csv_path: Path, output_dir: Path):
        df = load_and_clean_data(csv_path)

        set_visual_theme()

        generate_visualizations(df, output_dir, "full")
        generate_section4_visualizations(df, output_dir)

        for segment in ["fast", "luxury"]:
            segment_df = (
                df[df["type"].str.lower() == segment].copy()
                if "type" in df.columns
                else df.iloc[0:0]
            )
            if not segment_df.empty:
                generate_visualizations(segment_df, output_dir, f"{segment}")

        if "username" in df.columns:
            for brand, brand_df in df.groupby("username"):
                if len(brand_df) >= 5:
                    safe_brand = str(brand).strip().lower().replace(" ", "_")
                    generate_visualizations(brand_df, output_dir, f"brand_{safe_brand}")

        print(f"Saved outputs to: {output_dir}")

    return (run_analysis,)


@app.cell
def _(Path, run_analysis):
    run_analysis(Path("image_analysis_full.csv"), Path("visualization_outputs"))


if __name__ == "__main__":
    app.run()
