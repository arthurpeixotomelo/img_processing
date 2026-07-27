# /// script
# requires-python = ">=3.13"
# dependencies = [
#     "marimo>=0.23.3",
#     "polars",
# ]
# ///

import marimo

__generated_with = "0.23.14"
app = marimo.App()


@app.cell
def _():
    import polars as pl

    df = pl.read_parquet("structured_scrapper_data.parquet")
    return df, pl


@app.cell
def _(pl):
    df = pl.read_csv("image_analysis_full.csv").with_columns(
        pl
        .when(pl.col("color_category").is_in(["White", "Black", "Gray"]))
        .then(pl.lit("achromatic"))
        .otherwise(pl.lit("chromatic"))
        .alias("primary_color_category")
    )
    df
    return (df,)


@app.cell
def _(df, pl):
    # df.group_by("primary_color_category").agg(
    #     pl.len().alias("count"),
    #     pl.col("color_category").value_counts().alias("color_category_counts")
    # )

    df.group_by("color_temperature").agg(
        pl.len().alias("count"),
    )
    return


if __name__ == "__main__":
    app.run()
