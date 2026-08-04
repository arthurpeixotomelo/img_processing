import marimo

__generated_with = "0.23.16"
app = marimo.App()


@app.cell
def _():
    import polars as pl

    return (pl,)


@app.cell
def _(pl):
    df = pl.read_parquet('structured_scrapper_data.parquet')
    df_2 = pl.read_parquet('structured_scrapper_data_2.parquet')
    return


if __name__ == "__main__":
    app.run()
