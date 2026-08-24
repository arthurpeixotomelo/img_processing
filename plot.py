import marimo

__generated_with = "0.23.16"
app = marimo.App()


@app.cell
def _():
    import ast
    import re
    from collections.abc import Iterable, Sequence
    from dataclasses import dataclass
    from pathlib import Path

    import matplotlib.pyplot as plt
    import numpy as np
    import pandas as pd
    import plotly.graph_objects as go
    import seaborn as sns

    return Iterable, Path, Sequence, ast, dataclass, go, np, pd, plt, re, sns


@app.cell
def _(Iterable, Path, Sequence, ast, np, pd, plt, re, sns):
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

        return df

    return (load_and_clean_data,)


@app.cell
def _(
    Path,
    Sequence,
    dataclass,
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

    # Preferred display order per stage; entries not listed keep their natural order.
    STAGE_ORDER: dict[str, list[str]] = {
        "chromaticity": ["achromatic", "chromatic"],
        "branch": ["color", "luminosity", "saturation"],
        "saturation_category": ["high", "neutral", "low"],
        "luminosity_category": ["high", "neutral", "low"],
        "color_temperature": ["warm", "cool"],
    }

    # Stages whose values share vocabulary (low/neutral/high) and need a prefix
    # in the rendered label so they are visually unambiguous.
    STAGE_LABEL_PREFIX: dict[str, str] = {
        "saturation_category": "Sat",
        "luminosity_category": "Lum",
    }

    # Vertical lanes allocated to each post-branch chain. Keep them disjoint so
    # nodes from different branches never share y coordinates.
    LANE_BANDS: dict[str, tuple[float, float]] = {
        "color": (0.66, 0.94),
        "luminosity": (0.36, 0.62),
        "saturation": (0.06, 0.32),
    }

    @dataclass(frozen=True)
    class StageSpec:
        """Placement metadata for a column-derived Sankey stage."""

        stage: str
        x: float
        y_band: tuple[float, float]

        @property
        def preferred_order(self) -> list[str]:
            return STAGE_ORDER.get(self.stage, [])

    def normalize_unique(values: pd.Series) -> list[str]:
        """Drop NA and return deterministic string values in first-seen order."""
        return [str(value) for value in values.dropna().unique().tolist()]

    def ordered_values(stage: str, values: list[str]) -> list[str]:
        preferred = STAGE_ORDER.get(stage, [])
        ordered = [value for value in preferred if value in values]
        ordered.extend([value for value in values if value not in preferred])
        return ordered

    def stage_label(stage: str, value: str) -> str:
        prefix = STAGE_LABEL_PREFIX.get(stage)
        return f"{prefix} {value}" if prefix else value

    def node_key(stage: str, value: str) -> str:
        return f"{stage}::{value}"

    def spread_positions(count: int, start: float, stop: float) -> list[float]:
        if count <= 1:
            return [(start + stop) / 2]
        return np.linspace(start, stop, count).tolist()

    class NodeRegistry:
        """Registers Sankey nodes and accumulates links against stage-qualified keys."""

        def __init__(self) -> None:
            self.labels: list[str] = []
            self.x: list[float] = []
            self.y: list[float] = []
            self._index: dict[str, int] = {}
            self._sources: list[int] = []
            self._targets: list[int] = []
            self._values: list[float] = []

        def add_stage(self, spec: StageSpec, values: list[str]) -> None:
            ordered = ordered_values(spec.stage, values)
            band_start, band_stop = spec.y_band
            for value, y_pos in zip(
                ordered, spread_positions(len(ordered), band_start, band_stop)
            ):
                self._register(
                    node_key(spec.stage, value),
                    stage_label(spec.stage, value),
                    spec.x,
                    y_pos,
                )

        def add_fixed(self, spec: StageSpec, values: list[str]) -> None:
            """Register nodes for a stage with predefined values (order respected)."""
            band_start, band_stop = spec.y_band
            for value, y_pos in zip(
                values, spread_positions(len(values), band_start, band_stop)
            ):
                self._register(node_key(spec.stage, value), value, spec.x, y_pos)

        def _register(self, key: str, label: str, x: float, y: float) -> int:
            if key in self._index:
                return self._index[key]
            index = len(self.labels)
            self._index[key] = index
            self.labels.append(label)
            self.x.append(x)
            self.y.append(y)
            return index

        def link(self, source_key: str, target_key: str, value: float) -> None:
            self._sources.append(self._index[source_key])
            self._targets.append(self._index[target_key])
            self._values.append(float(max(value, 0.0)))

        def has(self, key: str) -> bool:
            return key in self._index

        def validate_links(self) -> None:
            """Ensure every link endpoint resolves to a registered node."""
            missing = {key for key in self._index if not self.has(key)}
            if missing:
                raise ValueError(
                    f"Sankey links reference unknown nodes: {sorted(missing)}"
                )

        @property
        def sources(self) -> list[int]:
            return self._sources

        @property
        def targets(self) -> list[int]:
            return self._targets

        @property
        def values(self) -> list[float]:
            return self._values

    def build_edge_frame(
        frame: pd.DataFrame,
        engagement_col: str,
        *,
        by: Sequence[str],
        source_key: str | None = None,
        target_prefix: str | None = None,
    ) -> pd.DataFrame:
        """Aggregate engagement by `by` columns using a sum and normalize to edges.

        When `source_key` is provided, every aggregating row becomes a single edge
        from that fixed node to a target keyed by `target_prefix::value`.
        Otherwise the first column in `by` is the source and the rest form the
        target key (joined with '::').
        """
        grouped = (
            frame.groupby(list(by), dropna=False)[engagement_col].sum().reset_index()
        )
        records: list[dict[str, object]] = []
        for _, row in grouped.iterrows():
            if any(pd.isna(row[col]) for col in by):
                continue
            if source_key is not None:
                target_value = str(row[by[0]])
                target_key = node_key(target_prefix or by[0], target_value)
                source = source_key
            else:
                source_value = str(row[by[0]])
                target_values = [str(row[col]) for col in by[1:]]
                source = node_key(by[0], source_value)
                target_key = node_key("::".join(by[1:]), "::".join(target_values))
            records.append({
                "source": source,
                "target": target_key,
                "value": row[engagement_col],
            })
        return pd.DataFrame(records, columns=["source", "target", "value"])

    def build_engagement_sankey(
        frame: pd.DataFrame,
        *,
        engagement_col: str = "engagement_total",
        output_path: Path | None = None,
    ) -> go.Figure:
        """Build a lane-separated Sankey of summed engagement flows.

        Stages: type -> username -> branch(color|luminosity|saturation) -> category.
        Each post-branch chain owns its own vertical lane so saturation and
        luminosity low/neutral/high nodes never overlap.
        """
        enriched = add_visual_cohort_columns(frame)
        require_columns(
            enriched,
            [
                "type",
                "username",
                "chromaticity",
                "color_temperature",
                "saturation_category",
                "luminosity_category",
                engagement_col,
            ],
        )

        registry = NodeRegistry()

        # Stage 1: type (far left)
        registry.add_fixed(
            StageSpec("type", 0.02, (0.35, 0.65)),
            ordered_values("type", normalize_unique(enriched["type"])),
        )

        # Stage 2: username
        registry.add_fixed(
            StageSpec("username", 0.22, (0.08, 0.92)),
            ordered_values("username", normalize_unique(enriched["username"])),
        )

        # Stage 3: branch hub nodes (color/luminosity/saturation)
        # Reverse band so color (top lane) gets highest y, saturation (bottom) gets lowest
        registry.add_fixed(
            StageSpec("branch", 0.46, (0.82, 0.18)),
            ordered_values("branch", ["color", "luminosity", "saturation"]),
        )

        # Stage 4: category nodes, each branch in its own vertical lane.
        color_stage = StageSpec("chromaticity", 0.70, LANE_BANDS["color"])
        saturation_stage = StageSpec(
            "saturation_category", 0.82, LANE_BANDS["saturation"]
        )
        luminosity_stage = StageSpec(
            "luminosity_category", 0.82, LANE_BANDS["luminosity"]
        )
        temperature_stage = StageSpec("color_temperature", 0.94, LANE_BANDS["color"])

        registry.add_stage(color_stage, normalize_unique(enriched["chromaticity"]))
        registry.add_stage(
            saturation_stage, normalize_unique(enriched["saturation_category"])
        )
        registry.add_stage(
            luminosity_stage, normalize_unique(enriched["luminosity_category"])
        )
        registry.add_stage(
            temperature_stage, normalize_unique(enriched["color_temperature"])
        )

        # --- Edges (summed engagement) -----------------------------------------
        # Each chain segment is aggregated with `.sum()` and normalized to the
        # (source, target, value) schema, then concatenated once at the end.

        # type -> username
        type_to_brand = build_edge_frame(
            enriched,
            engagement_col,
            by=["type", "username"],
        )

        # username -> each branch hub (brand total split evenly across 3 branches)
        brand_totals = (
            enriched
            .groupby("username", dropna=False)[engagement_col]
            .sum()
            .reset_index()
        )
        branch_edges: list[dict[str, object]] = []
        for _, row in brand_totals.iterrows():
            if pd.isna(row["username"]):
                continue
            brand_key = node_key("username", str(row["username"]))
            for branch in ("color", "luminosity", "saturation"):
                branch_edges.append({
                    "source": brand_key,
                    "target": node_key("branch", branch),
                    "value": row[engagement_col] / 3.0,
                })

        # branch::color -> chromaticity
        branch_color_edges = build_edge_frame(
            enriched,
            engagement_col,
            by=["chromaticity"],
            source_key="branch::color",
            target_prefix="chromaticity",
        )
        # branch::luminosity -> luminosity_category
        luminosity_edges = build_edge_frame(
            enriched,
            engagement_col,
            by=["luminosity_category"],
            source_key="branch::luminosity",
            target_prefix="luminosity_category",
        )
        # branch::saturation -> saturation_category
        saturation_edges = build_edge_frame(
            enriched,
            engagement_col,
            by=["saturation_category"],
            source_key="branch::saturation",
            target_prefix="saturation_category",
        )

        # chromaticity -> color_temperature (two-column groupby, then remap keys)
        temperature_edges = build_edge_frame(
            enriched,
            engagement_col,
            by=["chromaticity", "color_temperature"],
        )
        temperature_edges["source"] = temperature_edges["source"].apply(
            lambda key: node_key("chromaticity", key.split("::", 1)[1])
        )
        temperature_edges["target"] = temperature_edges["target"].apply(
            lambda key: node_key("color_temperature", key)
        )

        all_edges = pd.concat(
            [
                type_to_brand,
                pd.DataFrame(branch_edges),
                branch_color_edges,
                luminosity_edges,
                saturation_edges,
                temperature_edges,
            ],
            ignore_index=True,
        )

        # Drop any edges whose source/target was not registered as a node.
        all_edges = all_edges[
            all_edges["source"].apply(registry.has)
            & all_edges["target"].apply(registry.has)
        ].reset_index(drop=True)

        for _, row in all_edges.iterrows():
            registry.link(row["source"], row["target"], row["value"])

        figure = go.Figure(
            data=[
                go.Sankey(
                    arrangement="snap",
                    node={
                        "label": registry.labels,
                        "x": registry.x,
                        "y": registry.y,
                        "pad": 18,
                        "thickness": 16,
                        "line": {"color": "#2a2a2a", "width": 0.5},
                    },
                    link={
                        "source": registry.sources,
                        "target": registry.targets,
                        "value": registry.values,
                        "color": "rgba(120, 144, 184, 0.35)",
                    },
                )
            ]
        )
        figure.update_layout(
            title="Engagement flow (sum): brand type → brand → branch → category",
            font_size=12,
            height=620,
            margin={"l": 16, "r": 16, "t": 60, "b": 16},
        )

        if output_path is not None:
            figure.write_html(str(output_path))
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

        build_engagement_sankey(
            df,
            output_path=output_dir / f"{prefix}_sankey_engagement_cohorts.html",
        )

    return (generate_visualizations,)


@app.cell
def _(Path, generate_visualizations, load_and_clean_data, set_visual_theme):
    def run_analysis(csv_path: Path, output_dir: Path):
        df = load_and_clean_data(csv_path)

        set_visual_theme()

        generate_visualizations(df, output_dir, "full")

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
