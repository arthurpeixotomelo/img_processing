import marimo

__generated_with = "0.23.16"
app = marimo.App()


@app.cell
def _():
    import polars as pl

    return (pl,)


@app.cell
def _(pl):
    df = pl.read_csv('image_analysis_full.csv')
    return (df,)


@app.cell
def _(df, pl):
    chromaticity = (
        pl.when(pl.col('color_category').is_in(['Black', 'White', 'Gray']))
        .then(pl.lit('achromatic'))
        .otherwise(pl.lit('chromatic'))
    )
    enriched = df.with_columns(chromaticity.alias('chromaticity'))
    return (enriched,)


@app.cell
def _(enriched, pl):
    GROUPS = {
        'full': enriched,
        'fast': enriched.filter(pl.col('type') == 'fast'),
        'luxury': enriched.filter(pl.col('type') == 'luxury'),
    }

    ORDER = {
        'chromaticity': ['achromatic', 'chromatic'],
        'color_temperature': ['warm', 'cool'],
        'luminosity_category': ['low', 'neutral', 'high'],
        'saturation_category': ['low', 'neutral', 'high'],
    }

    def group_pct(group, column, value):
        frame = GROUPS[group]
        return 100.0 * frame.filter(pl.col(column) == value).height / frame.height

    def metric_table(column):
        header = '| Segment | Category | n | % |'
        sep = '|---|---|---|---|'
        rows = []
        for group_name in ('full', 'fast', 'luxury'):
            frame = GROUPS[group_name]
            total = frame.height
            rows.append(f'| {group_name} | — | {total} | 100% |')
            for value in ORDER[column]:
                count = frame.filter(pl.col(column) == value).height
                if count:
                    rows.append(
                        f'| {group_name} | {value} | {count} | {group_pct(group_name, column, value):.1f}% |'
                    )
        return '\n'.join([header, sep] + rows)

    metric_tables = {column: metric_table(column) for column in ORDER}
    return GROUPS, group_pct, metric_tables


@app.cell
def _(group_pct):
    insights = {}
    for column in ('chromaticity', 'color_temperature', 'luminosity_category', 'saturation_category'):
        insights[column] = {
            group: {
                value: group_pct(group, column, value)
                for value in ('low', 'neutral', 'high', 'warm', 'cool', 'achromatic', 'chromatic')
            }
            for group in ('full', 'fast', 'luxury')
        }
    return (insights,)


@app.cell
def _(GROUPS, pl):
    COLOR_FAMILIES = ['White', 'Gray', 'Black', 'Orange', 'Blue', 'Red']
    color_family_pct = {
        family: 100.0 * GROUPS['full'].filter(
            pl.col('color_category') == family
        ).height / GROUPS['full'].height
        for family in COLOR_FAMILIES
    }
    return (color_family_pct,)


@app.cell
def _(color_family_pct, insights, metric_tables):
    def build_section_3():
        ach = insights['chromaticity']
        temp = insights['color_temperature']
        lum = insights['luminosity_category']
        sat = insights['saturation_category']
        cfc = color_family_pct
        return f"""## 3. Results

    The descriptive analysis shows how the sample is split between the two broad
    color groups, and how that split shifts between fast-fashion and luxury
    accounts.

    - **Achromatic (full):** {ach['full']['achromatic']:.1f}%
    - **Chromatic (full):** {ach['full']['chromatic']:.1f}%

    Although the full sample leans moderately neutral, the balance changes
    noticeably by account type. Fast-fashion posts are the most neutral-looking,
    while luxury posts come the closest to an even split between neutral and
    colorful imagery.

    ### 3.1 Achromatic and Chromatic Images: Detail

    {metric_tables['chromaticity']}

    The steady increase in color across the sample is easy to miss at first, but it
    is consistent: fast-fashion content is the most neutral ({ach['fast']['achromatic']:.1f}%
    achromatic), luxury content is the least ({ach['luxury']['achromatic']:.1f}%), and the
    sample as a whole sits in between ({ach['full']['achromatic']:.1f}%). The two account
    types are not merely different in size; they lean toward different visual
    styles. Fast-fashion tends to present a clean, minimal, neutral look, whereas
    luxury accounts are more willing to show strong, clearly colored images.

    Within the neutral group, the sample is dominated by white, gray, and black
    families. Among the colorful images, the picture is lopsided as well: warm
    hues, especially orange and red, are the most common color families in the
    sample, and they appear more often in luxury imagery.

    ### 3.2 Dominant Color Families: Detail

    | Tone family | full (%) |
    |---|---|
    | White | {cfc['White']:.1f} |
    | Gray | {cfc['Gray']:.1f} |
    | Black | {cfc['Black']:.1f} |
    | Orange | {cfc['Orange']:.1f} |
    | Blue | {cfc['Blue']:.1f} |
    | Red | {cfc['Red']:.1f} |

    This table makes the earlier description concrete. The three neutral families
    (white, gray, black) together account for the majority of the sample, and the
    only colored families that reach any meaningful share are the warm ones. The
    overall pattern is consistent: what color exists in the dataset is concentrated
    in warm tones, and neutral "no-color" imagery is the norm rather than the
    exception.

    ### 3.3 Warm and Cool Tones: Detail

    {metric_tables['color_temperature']}

    Warm tones dominate every part of the sample, which is expected for fashion
    imagery. The interesting part is the margin: fast-fashion is almost entirely
    warm ({temp['fast']['warm']:.1f}%), while luxury content, although still
    predominantly warm ({temp['luxury']['warm']:.1f}%), includes a noticeably larger
    share of cool, blue-leaning imagery. The overall sample is {temp['full']['warm']:.1f}%
    warm and {temp['full']['cool']:.1f}% cool.

    ### 3.4 Luminosity: Detail

    {metric_tables['luminosity_category']}

    Most images in every group fall in the neutral brightness band, but the two
    account types diverge at the extremes. Fast-fashion rarely uses very dark
    imagery ({lum['fast']['low']:.1f}% low), keeping most content evenly lit
    ({lum['fast']['neutral']:.1f}% neutral). Luxury accounts use a wider range of
    lighting: they are more likely than fast-fashion to produce both very dark,
    dramatically lit images ({lum['luxury']['low']:.1f}% low) and extremely bright
    ones ({lum['luxury']['high']:.1f}% high). In other words, luxury leans on
    lighting as part of its visual identity, while fast-fashion stays in a safe,
    uniform brightness range.

    ### 3.5 Saturation: Detail

    {metric_tables['saturation_category']}

    Low saturation dominates everywhere, and the overall impression is that most
    fashion images are deliberately muted rather than vivid. The difference is one
    of degree. Fast-fashion is the most muted of all ({sat['fast']['low']:.1f}%
    low saturation) and almost never uses highly vivid colors
    ({sat['fast']['high']:.1f}%). Luxury is slightly more colorful
    ({sat['luxury']['low']:.1f}% low) and is the only group where strongly
    saturated imagery appears at all ({sat['luxury']['high']:.1f}%). Across the
    full sample, low saturation comfortably exceeds the neutral and high levels
    combined.
    """
    print('section 3 builder ready')
    return (build_section_3,)


@app.cell
def _(build_section_3):
    section_3 = build_section_3()
    return (section_3,)


@app.cell
def _(section_3):
    print(section_3)
    return


@app.cell
def _():
    from pathlib import Path

    return (Path,)


@app.cell
def _(Path, section_3):
    paper = Path('FINAL_PAPER_DRAFT.md')
    text = paper.read_text(encoding='utf-8')

    start_marker = '## 3. Results'
    end_marker = '## 4. Statistical Analysis'

    start = text.index(start_marker)
    end = text.index(end_marker)

    updated = text[:start] + section_3.rstrip('\n') + '\n\n' + text[end:]
    paper.write_text(updated, encoding='utf-8')
    print('Written section 3 into FINAL_PAPER_DRAFT.md')
    return


if __name__ == "__main__":
    app.run()
