# Statistical Analysis of Visual Features and Social Media Engagement in Fashion Images: A Draft Paper

## 1. Introduction and Overview

Understanding the drivers of social media engagement is crucial for digital
marketing and content creation. This study investigates the impact of visual
features—specifically color—on user engagement (likes, comments, and total
interactions) within a dataset of Instagram fashion images. Unlike previous
smaller-scale analyses that might have indicated strong relationships, this
comprehensive study leverages a larger dataset to provide more reliable,
statistically sound insights regarding the relationship between image aesthetics
and audience interaction.

## 2. Methodology & Dataset Characteristics

The dataset consists of 7,935 Instagram posts collected across 10 global fashion
brand accounts, divided into two distinct market segments: **Luxury**
($n = 4,806$, 60.6%) and **Fast Fashion** ($n = 3,129$, 39.4%).

| Segment / Account Type       | Brand Account   | Images ($n$) | Segment Share (%) | Total Sample Share (%) |
| :--------------------------- | :-------------- | :----------- | :---------------- | :--------------------- |
| **All Brands (Full Sample)** | **—**           | **7,935**    | **—**             | **100.0%**             |
| **Luxury**                   | **Subtotal**    | **4,806**    | **100.0%**        | **60.6%**              |
| luxury                       | @prada          | 1,375        | 28.6%             | 17.3%                  |
| luxury                       | @chanelofficial | 1,261        | 26.2%             | 15.9%                  |
| luxury                       | @louisvuitton   | 1,172        | 24.4%             | 14.8%                  |
| luxury                       | @dior           | 677          | 14.1%             | 8.5%                   |
| luxury                       | @gucci          | 321          | 6.7%              | 4.0%                   |
| **Fast Fashion**             | **Subtotal**    | **3,129**    | **100.0%**        | **39.4%**              |
| fast fashion                 | @zara           | 835          | 26.7%             | 10.5%                  |
| fast fashion                 | @mango          | 646          | 20.6%             | 8.1%                   |
| fast fashion                 | @bershka        | 629          | 20.1%             | 7.9%                   |
| fast fashion                 | @boohoo         | 580          | 18.5%             | 7.3%                   |
| fast fashion                 | @stradivarius   | 439          | 14.0%             | 5.5%                   |

The analysis was conducted using only Instagram posts, and when a post contained
more than one photo, only the first image was included in the dataset. This
choice was made to keep the sample consistent and to avoid counting multiple
images from the same post as separate observations.

The study used one color classification scheme with two groups: **achromatic**
and **chromatic**. Achromatic images are those dominated by neutral tones such
as black, white, and gray, where color is weak or absent. Chromatic images are
those where a clear hue is visible, such as red, blue, green, yellow, or similar
color families. The separation was based on the dominant visual characteristics
of the image, especially hue presence and the proportion of pixels that belonged
to the main color region. In simple terms, the goal was to distinguish images
that are mostly neutral from images that show a strong recognizable color.

This classification was used because it gives a simple and reproducible way to
compare neutral-looking images with clearly colored ones. It also avoids forcing
too many small color labels into the analysis when the main question is whether
visible color presence itself relates to engagement.

The statistical methods below were used to check the results from different
angles. Each one answers a slightly different question about the data.

### 2.1 Analysis of Variance (ANOVA)

ANOVA is a test that compares the average likes across several groups at once.
In simple terms, it asks whether one color group seems to get more engagement
than the others. It is useful when the goal is to compare more than two
categories in a single test. We used it to see whether engagement changes
depending on the dominant color class. This helped determine whether the
observed differences between groups were strong enough to be considered
statistically meaningful.

### 2.2 Kruskal-Wallis Test

The Kruskal-Wallis test is similar to ANOVA, but it is safer when the data are
uneven or not perfectly normal. Instead of comparing averages directly, it
compares the general ranking of the values. This makes it useful when some
categories have very large or very small values that could distort a simple
average. We used it as a second check on the group comparison results. Its role
was to confirm whether the color categories still looked different even when the
data did not follow ideal statistical assumptions.

### 2.3 Chi-Square Test

The Chi-Square test is used for counting how often things appear in different
categories. It does not look at the size of likes directly, but at whether
category frequencies seem uneven or connected. This is helpful when the question
is whether certain color classes appear more often than expected. We used it to
examine whether the distribution of color categories was balanced or heavily
concentrated in a few groups. That matters because a very uneven distribution
can shape how the rest of the analysis should be interpreted.

### 2.4 Multiple Regression and VIF

Multiple regression is a method that looks at several predictors at the same
time. It helps show whether color-related variables still matter after
accounting for the influence of other variables. In plain language, it asks
whether a feature has any independent relationship with likes when the other
features are already included. We used it to test whether visual factors could
jointly explain engagement rather than only one at a time. VIF, or Variance
Inflation Factor, was added to check whether some predictors were too similar to
each other and might confuse the model.

### 2.5 Pearson Correlation

Pearson correlation measures how strongly two numerical variables move together
in a straight-line pattern. If one value goes up and the other usually goes up
too, the correlation is positive. If one goes up while the other goes down, the
correlation is negative. We used Pearson correlation to test whether specific
color measurements had a simple linear relationship with likes. This was
important because it gives a quick first look at whether color intensity,
brightness, or channel values might be connected to engagement.

### 2.6 Spearman Correlation

Spearman correlation is another relationship test, but it focuses on whether
values move together in the same order rather than in a straight line. It is
useful when the relationship may be curved, uneven, or influenced by outliers.
In simpler terms, it asks whether bigger values in one variable generally match
bigger values in another, even if the pattern is not perfectly linear. We used
it to check for more flexible relationships between color features and likes.
This made the analysis less dependent on the assumption that the relationship
had to be a straight line.

## 3. Results

The descriptive analysis shows how the sample is split between the two broad
color groups, and how that split shifts between fast-fashion and luxury
accounts.

- **Achromatic (full):** 55.1%
- **Chromatic (full):** 44.9%

Although the full sample leans moderately neutral, the balance changes
noticeably by account type. Fast-fashion posts are the most neutral-looking,
while luxury posts come the closest to an even split between neutral and
colorful imagery.

### 3.1 Achromatic and Chromatic Images: Detail

| Segment | Category   | n    | %     |
| ------- | ---------- | ---- | ----- |
| full    | —          | 7935 | 100%  |
| full    | achromatic | 4371 | 55.1% |
| full    | chromatic  | 3564 | 44.9% |
| fast    | —          | 3129 | 100%  |
| fast    | achromatic | 1880 | 60.1% |
| fast    | chromatic  | 1249 | 39.9% |
| luxury  | —          | 4806 | 100%  |
| luxury  | achromatic | 2491 | 51.8% |
| luxury  | chromatic  | 2315 | 48.2% |

The steady increase in color across the sample is easy to miss at first, but it
is consistent: fast-fashion content is the most neutral (60.1% achromatic),
luxury content is the least (51.8%), and the sample as a whole sits in between
(55.1%). The two account types are not merely different in size; they lean
toward different visual styles. Fast-fashion tends to present a clean, minimal,
neutral look, whereas luxury accounts are more willing to show strong, clearly
colored images.

Within the neutral group, the sample is dominated by white, gray, and black
families. Among the colorful images, the picture is lopsided as well: warm hues,
especially orange and red, are the most common color families in the sample, and
they appear more often in luxury imagery.

### 3.2 Dominant Color Families: Detail

| Tone family | full (%) |
| ----------- | -------- |
| White       | 32.0     |
| Gray        | 15.8     |
| Black       | 7.3      |
| Orange      | 17.5     |
| Blue        | 9.2      |
| Red         | 7.2      |

This table makes the earlier description concrete. The three neutral families
(white, gray, black) together account for the majority of the sample, and the
only colored families that reach any meaningful share are the warm ones. The
overall pattern is consistent: what color exists in the dataset is concentrated
in warm tones, and neutral "no-color" imagery is the norm rather than the
exception.

### 3.3 Warm and Cool Tones: Detail

| Segment | Category | n    | %     |
| ------- | -------- | ---- | ----- |
| full    | —        | 7935 | 100%  |
| full    | warm     | 6892 | 86.9% |
| full    | cool     | 1043 | 13.1% |
| fast    | —        | 3129 | 100%  |
| fast    | warm     | 2848 | 91.0% |
| fast    | cool     | 281  | 9.0%  |
| luxury  | —        | 4806 | 100%  |
| luxury  | warm     | 4044 | 84.1% |
| luxury  | cool     | 762  | 15.9% |

Warm tones dominate every part of the sample, which is expected for fashion
imagery. The interesting part is the margin: fast-fashion is almost entirely
warm (91.0%), while luxury content, although still predominantly warm (84.1%),
includes a noticeably larger share of cool, blue-leaning imagery. The overall
sample is 86.9% warm and 13.1% cool.

### 3.4 Luminosity: Detail

| Segment | Category | n    | %     |
| ------- | -------- | ---- | ----- |
| full    | —        | 7935 | 100%  |
| full    | low      | 1573 | 19.8% |
| full    | neutral  | 4765 | 60.1% |
| full    | high     | 1597 | 20.1% |
| fast    | —        | 3129 | 100%  |
| fast    | low      | 412  | 13.2% |
| fast    | neutral  | 2176 | 69.5% |
| fast    | high     | 541  | 17.3% |
| luxury  | —        | 4806 | 100%  |
| luxury  | low      | 1161 | 24.2% |
| luxury  | neutral  | 2589 | 53.9% |
| luxury  | high     | 1056 | 22.0% |

Most images in every group fall in the neutral brightness band, but the two
account types diverge at the extremes. Fast-fashion rarely uses very dark
imagery (13.2% low), keeping most content evenly lit (69.5% neutral). Luxury
accounts use a wider range of lighting: they are more likely than fast-fashion
to produce both very dark, dramatically lit images (24.2% low) and extremely
bright ones (22.0% high). In other words, luxury leans on lighting as part of
its visual presentation, while fast-fashion stays in a safe, uniform brightness
range.

### 3.5 Saturation: Detail

| Segment | Category | n    | %     |
| ------- | -------- | ---- | ----- |
| full    | —        | 7935 | 100%  |
| full    | low      | 5702 | 71.9% |
| full    | neutral  | 2003 | 25.2% |
| full    | high     | 230  | 2.9%  |
| fast    | —        | 3129 | 100%  |
| fast    | low      | 2483 | 79.4% |
| fast    | neutral  | 609  | 19.5% |
| fast    | high     | 37   | 1.2%  |
| luxury  | —        | 4806 | 100%  |
| luxury  | low      | 3219 | 67.0% |
| luxury  | neutral  | 1394 | 29.0% |
| luxury  | high     | 193  | 4.0%  |

Low saturation dominates everywhere, and the overall impression is that most
fashion images are deliberately muted rather than vivid. The difference is one
of degree. Fast-fashion is the most muted of all (79.4% low saturation) and
almost never uses highly vivid colors (1.2%). Luxury is slightly more colorful
(67.0% low) and is the only group where strongly saturated imagery appears at
all (4.0%). Across the full sample, low saturation comfortably exceeds the
neutral and high levels combined.

### 3.6 Overall Visual Flows & Brand Profiles

To understand how visual choices translate into engagement at both the aggregate
and brand levels, we examined the overall flow of audience interaction across
visual cohorts and analyzed the individual profiles of each analyzed account.

#### 3.6.1 Macro Visual Engagement Flows

Across the entire dataset of 7,935 posts, the distribution of engagement across
color families and temperature cohorts reflects the dominant styling choices of
the fashion industry:

![Full Dataset: Engagement by Color Category](visualization_outputs/full_bar_color_category_engagement.png)

![Full Dataset: Engagement by Color Temperature](visualization_outputs/full_bar_color_temperature_engagement.png)

![Full Dataset: Engagement Flow Sankey](visualization_outputs/full_sankey_engagement_cohorts.png)

The macro Sankey flow shows that while Luxury and Fast Fashion generate massive
interaction volumes through both achromatic and chromatic palettes, engagement
remains evenly distributed across brightness and saturation tiers rather than
concentrating in any single visual extreme.

---

#### 3.6.2 Fast-Fashion Brand Profiles

##### @bershka (Fast Fashion)

Bershka balances neutral catalog photography with high-energy streetwear
promotions. Warm tones and neutral luminosity carry the majority of audience
interactions.

- **Visual Performance Charts**:
  - ![Bershka Engagement by Color Category](visualization_outputs/brand_bershka_bar_color_category_engagement.png)
  - ![Bershka Engagement by Color Temperature](visualization_outputs/brand_bershka_bar_color_temperature_engagement.png)
  - ![Bershka Engagement Flow](visualization_outputs/brand_bershka_sankey_engagement_cohorts.png)
- **Top-Performing Content**:
  - **Achromatic Leader** (Gray, Warm, Neutral Lum, Low Sat): **101,510 likes**,
    169 comments ([View Post](https://www.instagram.com/p/CyvtT6nItwI/))
    ![Bershka Top Achromatic Post](visualization_outputs/brand_bershka_sample_achromatic.jpg)
  - **Chromatic Leader** (Red, Warm, Neutral Lum, Neutral Sat): **106,782
    likes**, 549 comments
    ([View Post](https://www.instagram.com/p/C4nVJCtofcW/))
    ![Bershka Top Chromatic Post](visualization_outputs/brand_bershka_sample_chromatic.jpg)

##### @boohoo (Fast Fashion)

Boohoo exhibits a high concentration of dark, low-luminosity imagery alongside
vibrant seasonal drops. Neutral and cool tones perform comparably well.

- **Visual Performance Charts**:
  - ![Boohoo Engagement by Color Category](visualization_outputs/brand_boohoo_bar_color_category_engagement.png)
  - ![Boohoo Engagement by Color Temperature](visualization_outputs/brand_boohoo_bar_color_temperature_engagement.png)
  - ![Boohoo Engagement Flow](visualization_outputs/brand_boohoo_sankey_engagement_cohorts.png)
- **Top-Performing Content**:
  - **Achromatic Leader** (Black, Warm, Low Lum, Low Sat): **175,871 likes**, 64
    comments ([View Post](https://www.instagram.com/p/DEfl5GyOKWf/))
    ![Boohoo Top Achromatic Post](visualization_outputs/brand_boohoo_sample_achromatic.jpg)
  - **Chromatic Leader** (Blue, Cool, Low Lum, Neutral Sat): **169,958 likes**,
    404 comments ([View Post](https://www.instagram.com/p/DP3yhymkWJi/))
    ![Boohoo Top Chromatic Post](visualization_outputs/brand_boohoo_sample_chromatic.jpg)

##### @mango (Fast Fashion)

Mango relies heavily on crisp, clean, high-luminosity Mediterranean neutrals
(whites, beiges, creams). White and warm tones dominate their engagement totals.

- **Visual Performance Charts**:
  - ![Mango Engagement by Color Category](visualization_outputs/brand_mango_bar_color_category_engagement.png)
  - ![Mango Engagement by Color Temperature](visualization_outputs/brand_mango_bar_color_temperature_engagement.png)
  - ![Mango Engagement Flow](visualization_outputs/brand_mango_sankey_engagement_cohorts.png)
- **Top-Performing Content**:
  - **Achromatic Leader** (White, Warm, Neutral Lum, Low Sat): **228,081
    likes**, 458 comments
    ([View Post](https://www.instagram.com/p/DAsbfQAo_fi/))
    ![Mango Top Achromatic Post](visualization_outputs/brand_mango_sample_achromatic.jpg)
  - **Chromatic Leader** (Orange, Warm, Neutral Lum, Neutral Sat): **16,142
    likes**, 196 comments
    ([View Post](https://www.instagram.com/p/DRkNnY4AY7n/))
    ![Mango Top Chromatic Post](visualization_outputs/brand_mango_sample_chromatic.jpg)

##### @stradivarius (Fast Fashion)

Stradivarius focuses on bright, accessible lifestyle styling with low saturation
and warm temperatures across both neutral and colorful pieces.

- **Visual Performance Charts**:
  - ![Stradivarius Engagement by Color Category](visualization_outputs/brand_stradivarius_bar_color_category_engagement.png)
  - ![Stradivarius Engagement by Color Temperature](visualization_outputs/brand_stradivarius_bar_color_temperature_engagement.png)
  - ![Stradivarius Engagement Flow](visualization_outputs/brand_stradivarius_sankey_engagement_cohorts.png)
- **Top-Performing Content**:
  - **Achromatic Leader** (White, Warm, High Lum, Low Sat): **30,603 likes**, 42
    comments ([View Post](https://www.instagram.com/p/C7BjTI7M0d7/))
    ![Stradivarius Top Achromatic Post](visualization_outputs/brand_stradivarius_sample_achromatic.jpg)
  - **Chromatic Leader** (Orange, Warm, Neutral Lum, Low Sat): **14,837 likes**,
    44 comments ([View Post](https://www.instagram.com/p/C6CPWIArOOg/))
    ![Stradivarius Top Chromatic Post](visualization_outputs/brand_stradivarius_sample_chromatic.jpg)

##### @zara (Fast Fashion)

Zara combines high-contrast editorial studio photography with dramatic lighting.
High comments volume characterizes their most viral posts.

- **Visual Performance Charts**:
  - ![Zara Engagement by Color Category](visualization_outputs/brand_zara_bar_color_category_engagement.png)
  - ![Zara Engagement by Color Temperature](visualization_outputs/brand_zara_bar_color_temperature_engagement.png)
  - ![Zara Engagement Flow](visualization_outputs/brand_zara_sankey_engagement_cohorts.png)
- **Top-Performing Content**:
  - **Achromatic Leader** (White, Warm, High Lum, Low Sat): **340,221 likes**,
    325,022 comments ([View Post](https://www.instagram.com/p/C0vxGLVu9Vt/))
    ![Zara Top Achromatic Post](visualization_outputs/brand_zara_sample_achromatic.jpg)
  - **Chromatic Leader** (Yellow, Warm, Low Lum, High Sat): **240,426 likes**,
    141,515 comments ([View Post](https://www.instagram.com/p/CzRZ-uzKKLw/))
    ![Zara Top Chromatic Post](visualization_outputs/brand_zara_sample_chromatic.jpg)

---

#### 3.6.3 Luxury Brand Profiles

##### @chanelofficial (Luxury)

Chanel is renowned for its timeless black-and-white visual presentation,
punctuated by vibrant haute couture campaigns. Both achromatic and warm
chromatic imagery achieve top-tier reach.

- **Visual Performance Charts**:
  - ![Chanel Engagement by Color Category](visualization_outputs/brand_chanelofficial_bar_color_category_engagement.png)
  - ![Chanel Engagement by Color Temperature](visualization_outputs/brand_chanelofficial_bar_color_temperature_engagement.png)
  - ![Chanel Engagement Flow](visualization_outputs/brand_chanelofficial_sankey_engagement_cohorts.png)
- **Top-Performing Content**:
  - **Achromatic Leader** (White, Warm, High Lum, Low Sat): **946,685 likes**,
    2,667 comments ([View Post](https://www.instagram.com/p/Crv2i6PNan3/))
    ![Chanel Top Achromatic Post](visualization_outputs/brand_chanelofficial_sample_achromatic.jpg)
  - **Chromatic Leader** (Orange, Warm, High Lum, Low Sat): **893,806 likes**,
    4,558 comments ([View Post](https://www.instagram.com/p/DZzsq53DB_t/))
    ![Chanel Top Chromatic Post](visualization_outputs/brand_chanelofficial_sample_chromatic.jpg)

##### @dior (Luxury)

Dior features dramatic, high-production runway and campaign imagery. While
white/neutral backdrops produce massive like counts, moody green/cool hues
generate strong conversational engagement.

- **Visual Performance Charts**:
  - ![Dior Engagement by Color Category](visualization_outputs/brand_dior_bar_color_category_engagement.png)
  - ![Dior Engagement by Color Temperature](visualization_outputs/brand_dior_bar_color_temperature_engagement.png)
  - ![Dior Engagement Flow](visualization_outputs/brand_dior_sankey_engagement_cohorts.png)
- **Top-Performing Content**:
  - **Achromatic Leader** (White, Warm, Neutral Lum, Low Sat): **1,340,782
    likes**, 14,890 comments
    ([View Post](https://www.instagram.com/p/DTAKS1bCNbf/))
    ![Dior Top Achromatic Post](visualization_outputs/brand_dior_sample_achromatic.jpg)
  - **Chromatic Leader** (Green, Cool, Low Lum, Neutral Sat): **355,814 likes**,
    5,464 comments ([View Post](https://www.instagram.com/p/DVdSzE6iJjB/))
    ![Dior Top Chromatic Post](visualization_outputs/brand_dior_sample_chromatic.jpg)

##### @gucci (Luxury)

Gucci is distinguished by its eclectic, maximalist color palettes. Chromatic
imagery (especially orange and blue hues) frequently outperforms neutral tones.

- **Visual Performance Charts**:
  - ![Gucci Engagement by Color Category](visualization_outputs/brand_gucci_bar_color_category_engagement.png)
  - ![Gucci Engagement by Color Temperature](visualization_outputs/brand_gucci_bar_color_temperature_engagement.png)
  - ![Gucci Engagement Flow](visualization_outputs/brand_gucci_sankey_engagement_cohorts.png)
- **Top-Performing Content**:
  - **Achromatic Leader** (Black, Warm, Neutral Lum, Low Sat): **672,353
    likes**, 4,262 comments
    ([View Post](https://www.instagram.com/p/DVTlwj7E2dA/))
    ![Gucci Top Achromatic Post](visualization_outputs/brand_gucci_sample_achromatic.jpg)
  - **Chromatic Leader** (Orange, Warm, Neutral Lum, Low Sat): **1,073,875
    likes**, 11,989 comments
    ([View Post](https://www.instagram.com/p/DVVnJiZDD1R/))
    ![Gucci Top Chromatic Post](visualization_outputs/brand_gucci_sample_chromatic.jpg)

##### @louisvuitton (Luxury)

Louis Vuitton leads the entire dataset in peak post engagement, driven by
celebrity ambassadors and high-contrast editorial photography. Dark,
low-luminosity posts and rich cool tones perform at scale.

- **Visual Performance Charts**:
  - ![Louis Vuitton Engagement by Color Category](visualization_outputs/brand_louisvuitton_bar_color_category_engagement.png)
  - ![Louis Vuitton Engagement by Color Temperature](visualization_outputs/brand_louisvuitton_bar_color_temperature_engagement.png)
  - ![Louis Vuitton Engagement Flow](visualization_outputs/brand_louisvuitton_sankey_engagement_cohorts.png)
- **Top-Performing Content**:
  - **Achromatic Leader** (Black, Warm, Low Lum, Low Sat): **3,543,199 likes**,
    7,834 comments ([View Post](https://www.instagram.com/p/C-uS7lZAUwa/))
    ![Louis Vuitton Top Achromatic Post](visualization_outputs/brand_louisvuitton_sample_achromatic.jpg)
  - **Chromatic Leader** (Blue, Cool, Neutral Lum, Neutral Sat): **2,486,338
    likes**, 24,906 comments
    ([View Post](https://www.instagram.com/p/CwPAQ6PtA08/))
    ![Louis Vuitton Top Chromatic Post](visualization_outputs/brand_louisvuitton_sample_chromatic.jpg)

##### @prada (Luxury)

Prada uses minimalist, architectural, and cinematic compositions. Gray and cool
blue palettes capture the brand's distinctive intellectual visual tone.

- **Visual Performance Charts**:
  - ![Prada Engagement by Color Category](visualization_outputs/brand_prada_bar_color_category_engagement.png)
  - ![Prada Engagement by Color Temperature](visualization_outputs/brand_prada_bar_color_temperature_engagement.png)
  - ![Prada Engagement Flow](visualization_outputs/brand_prada_sankey_engagement_cohorts.png)
- **Top-Performing Content**:
  - **Achromatic Leader** (Gray, Warm, Neutral Lum, Low Sat): **2,062,521
    likes**, 16,187 comments
    ([View Post](https://www.instagram.com/p/DB8SQPttuHM/))
    ![Prada Top Achromatic Post](visualization_outputs/brand_prada_sample_achromatic.jpg)
  - **Chromatic Leader** (Blue, Cool, Low Lum, Neutral Sat): **1,367,335
    likes**, 4,468 comments
    ([View Post](https://www.instagram.com/p/DIvcnmPtfEx/))
    ![Prada Top Chromatic Post](visualization_outputs/brand_prada_sample_chromatic.jpg)

---

## 4. Statistical Analysis

To determine whether an image's visual features have a real impact on audience
engagement, we tested our dataset of 7,935 Instagram posts using several
statistical tools. Rather than looking at colors in isolation, we examined how
individual visual attributes (RGB color channels, warmth, brightness, and
vividness) connect to **likes**, **comments**, and **total engagement**
($\text{likes} + \text{comments}$).

Overall, the data delivers a clear verdict: **isolated visual properties have
virtually no measurable impact on social media engagement.**

### 4.1 Correlation Analysis: Do Visual Attributes Move the Needle?

Correlation measures how closely two variables move together on a scale from
-1.0 to +1.0 (where 0 means no connection at all, and values above $\pm 0.30$
indicate a meaningful real-world impact). Across all 7,935 posts, every single
visual attribute scored between $-0.04$ and $+0.00$, remaining firmly trapped in
the "No Real Effect" zone.

![Visual Feature Correlation Benchmark vs Real-World Impact Threshold](visualization_outputs/concept_correlation_benchmark.png)

#### 4.1.1 Correlation with Likes

Likes represent the vast majority of social media interactions. If colorful or
bright images performed better, we would expect positive correlations well above
zero.

![Visual Feature Correlation with Likes](visualization_outputs/section4_likes_correlation.png)

As shown in the chart above:

- **Red, Green, Blue, Warmth, and Brightness** all hovered near **$r = -0.04$**
  ($p < 0.001$). While the large sample size makes this tiny negative trend
  statistically detectable, the effect size is so small that it has no practical
  consequence in real-world marketing.
- **Color Vividness (Saturation)** scored **$r = +0.004$** ($p = 0.688$),
  showing zero linear relationship with likes.

In short, tuning the lighting or color channels of an image will not
meaningfully increase or decrease its likes.

#### 4.1.2 Correlation with Comments

Leaving a comment requires more effort from a user than tapping "like." We
examined whether certain colors or lighting styles provoke more user commentary.

![Visual Feature Correlation with Comments](visualization_outputs/section4_comments_correlation.png)

As shown in the chart:

- Every visual feature produced a linear correlation near zero (**$r = -0.003$
  to $+0.001$**, $p > 0.35$).
- Looking at overall ranking patterns (rank correlation), warm tones and high
  brightness showed a very slight negative trend ($\rho = -0.060$), while higher
  color saturation showed a slight positive trend ($\rho = +0.024$).

This indicates that visual factors do not linearly drive comment volume, though
saturated colors may occasionally catch a viewer's eye enough to prompt a
response.

#### 4.1.3 Correlation with Total Engagement

Total engagement combines likes and comments ($\text{Likes} + \text{Comments}$).

![Visual Feature Correlation with Total Engagement](visualization_outputs/section4_total_engagement_correlation.png)

Because likes make up over 98.9% of all interactions, the total engagement
results mirror the likes analysis almost identically ($r = -0.039$ for color
channels and brightness; $r = +0.004$ for saturation). Across all combined
interactions, visual features remain negligible predictors of success.

---

### 4.2 Group Comparisons: Neutral vs. Colorful Images

Instead of looking at continuous sliders for color and brightness, what happens
if we group images into two broad styles: **Neutral (Achromatic: black, white,
gray)** versus **Colorful (Chromatic: red, blue, orange, green, etc.)**?

We compared both the mathematical average (mean) and the typical middle-tier
performance (median) between the two groups using standard comparison tests
(ANOVA and Kruskal-Wallis).

#### Likes Comparison: Neutral vs. Colorful

![Likes: Neutral vs. Colorful Comparison](visualization_outputs/section4_likes_group_comparison.png)

- **Neutral Posts ($n = 4,371$)**: Average of 38,622 likes (median: 17,977).
- **Colorful Posts ($n = 3,564$)**: Average of 40,257 likes (median: 18,563).
- **The Result**: While colorful posts show a slight average lead of ~1,600
  likes, statistical tests (ANOVA $F = 0.37, p = 0.545$) confirm this gap is
  completely random posting noise rather than a real advantage.

#### Comments Comparison: Neutral vs. Colorful

![Comments: Neutral vs. Colorful Comparison](visualization_outputs/section4_comments_group_comparison.png)

- **Neutral Posts ($n = 4,371$)**: Average of 437 comments (median: 104).
- **Colorful Posts ($n = 3,564$)**: Average of 417 comments (median: 114).
- **The Result**: Although the average comment counts are virtually identical
  ($F = 0.04, p = 0.840$), colorful posts had a modestly higher median (114 vs.
  104, Kruskal-Wallis $H = 11.61, p < 0.001$). This suggests that while color
  does not boost viral reach, it can serve as a subtle conversational hook.

---

### 4.3 Brand Presentation vs. Audience Choice: The Chi-Square Finding

If color has little impact on engagement, why do fast-fashion and luxury
accounts look so different?

![Visual Strategy by Brand Category: Fast Fashion vs. Luxury](visualization_outputs/section4_brand_presentation_chi_square.png)

Using a Chi-Square test of independence ($\chi^2 = 51.83, p < 0.0001$), we
evaluated whether brand category influences color choice:

- **Fast-Fashion accounts** chose neutral, achromatic palettes in **60.1%** of
  their posts ($n = 1,880$), keeping colorful imagery to **39.9%**
  ($n = 1,249$).
- **Luxury accounts** chose neutral palettes in **51.8%** of their posts
  ($n = 2,491$), displaying significantly more colorful imagery (**48.2%**,
  $n = 2,315$).

Because audience engagement is virtually identical between neutral and colorful
images across both categories, this statistical discrepancy proves that color
distribution is driven by intentional **brand presentation**[^1], not audience
demand. Fast-fashion brands intentionally curate a clean, uniform, neutral look
to showcase catalog merchandise clearly, whereas luxury brands deliberately
deploy rich, colorful, and moody palettes as part of their curated editorial
aesthetic.

---

### 4.4 The 99.6% Reality: Multiple Regression & Multicollinearity

To confirm whether visual features might have a combined impact that single
features missed, we built a multiple regression model combining Red, Green,
Blue, Brightness, and Saturation into one predictive formula.

![How Photography Affects Engagement](visualization_outputs/section4_explained_variance_pie.png)

#### The Big Picture:

- **The Combined Visual Model explains only 0.35% of likes ($R^2 = 0.0035$)**
  and **0.02% of comments**.
- The remaining **99.65%** of what makes an Instagram post succeed is driven by
  non-visual factors: brand reputation, caption quality, content relevance,
  timing, and platform recommendation algorithms.

#### Individual Feature Contribution:

Looking at each visual attribute independently confirms that none of them drive
engagement on their own:

![Individual Feature Contribution](visualization_outputs/section4_feature_variance_bars.png)

- **Brightness (Luminosity)** explains only **0.17%** ($R^2 = 0.0017$) of likes
  variance.
- **Warmth (Color Temperature)**, **Red Hue**, and **Green Hue** each
  independently explain only **0.15%**.
- **Blue Hue** explains **0.09%**, and **Saturation** explains **0.00%**.
  _(Note: Because color channels covary with overall lighting, their individual
  simple contributions share overlapping variance rather than adding up
  directly; together in a multiple regression model, their combined predictive
  power reaches 0.35%.)_

#### Understanding Feature Overlap (Multicollinearity / VIF):

When checking how predictors interact (using Variance Inflation Factor, or VIF),
we found that Red, Green, and Blue channels naturally move together when an
image gets brighter (leading to high inter-channel correlation,
$\text{VIF} > 10$). However, overall **Brightness ($\text{VIF} = 3.98$)** and
**Saturation ($\text{VIF} = 1.44$)** operate independently. When we simplify the
model to look at Color Warmth, Brightness, and Saturation, all variables are
completely independent ($\text{VIF} < 1.6$), confirming that our finding—that
the visual features analyzed do not drive engagement—is robust and statistically
sound.

---

[^1]: In this study, **brand presentation** refers specifically to the curated
    visual style and aesthetic choices—such as lighting setup, color palette
    selection, and compositional framing—that a brand deliberately uses to
    present its content to social media audiences. It reflects the account's
    intentional visual communication strategy rather than consumer-driven
    demand.

[^2]: **Technical Appendix & Methodology Notes**:

- **Sample Size**: $N = 7,935$ total Instagram posts (Fast fashion: $n = 3,129$;
  Luxury: $n = 4,806$).
- **RGB Extraction**: Cluster centers extracted via $k$-means clustering
  ($k = 5$) on 20,000 sampled image pixels.
- **Color Warmth Score**: Continuous index calculated as
  $\frac{R \times 1.0 + G \times 0.5}{2} - \frac{B \times 1.0 + G \times 0.3}{2}$.
- **Luminosity & Saturation**: Extracted from 0–255 grayscale conversion and HSV
  S-channel respectively.
- **Full Model Metrics**: Likes model
  ($F(5, 7929) = 5.56, p < 0.0001, R^2 = 0.00349, \text{Adjusted } R^2 = 0.00286$);
  Comments model ($F(5, 7929) = 0.36, p = 0.8752, R^2 = 0.00023$).

## 5. Discussion

The main result of this study is not that color has no role at all, but that its
isolated effect is too small to explain engagement by itself. The
achromatic/chromatic split is useful as a clean descriptive classification, yet
it does not produce a strong separation in likes.

This supports a multifactorial interpretation of social media engagement.
Factors such as content relevance, audience interest, posting time, caption
quality, account reach, and platform dynamics are likely more important than the
presence or absence of visible color alone. In that sense, the image itself
should be treated as only one component of a broader engagement context.

From a methodological point of view, the simplified classification scheme is
also preferable because it keeps the analysis interpretable. Instead of
introducing several fine-grained color labels that may be unstable or difficult
to compare, the achromatic/chromatic split allows a clearer discussion of
whether neutral images behave differently from colorful ones.

## 6. Conclusion

This analysis suggests that dominant color characteristics have limited direct
impact on Instagram engagement in this fashion-image dataset. The descriptive
imbalance between achromatic and chromatic images is clear, but the inferential
results and correlations do not support a strong relationship between visual
color features and likes.

The practical implication is that color should be understood as a secondary
factor rather than a primary predictor of success. For content creators and
marketers, engagement is better approached as a multidimensional outcome shaped
by content strategy, audience fit, and platform context, rather than by color
choice alone.
