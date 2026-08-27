# Statistical Analysis of Visual Features and Social Media Engagement in Fashion Images: A Draft Paper

## 1. Introduction and Overview

Understanding the drivers of social media engagement is crucial for digital
marketing and content creation. This study investigates the impact of visual
features—specifically color—on user engagement (likes) within a dataset of
Instagram fashion images. Unlike previous smaller-scale analyses that might have
indicated strong relationships, this comprehensive study leverages a larger
dataset to provide more reliable, statistically sound insights regarding the
relationship between image aesthetics and audience interaction.

## 2. Methodology & Dataset Characteristics

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
its visual identity, while fast-fashion stays in a safe, uniform brightness
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

3.5 graphs and images for each brand

<!-- bar color chart, bar color temperature chart, sankey diagram -->

<!-- 2 images per brand: one achromatic, one chromatic -->

## 4. Statistical Analysis

measurable influence on audience engagement, the analysis combined bivariate
correlations (Pearson's $r$ and Spearman's $\rho$), two-group mean and rank
comparisons (One-Way ANOVA and Kruskal-Wallis tests), categorical tests of
independence ($\chi^2$), and multiple linear regression with variance inflation
factor (VIF) diagnostics.

The comparison between achromatic and chromatic images should be reported with
the final ANOVA result for this exact split. If the distribution of likes
departs from normality or shows strong dispersion, the Kruskal-Wallis test can
be used as a robust confirmation of the same pattern. The two tests serve
different purposes, but they should lead to the same general interpretation:
whether the visual classification is associated with a meaningful difference in
engagement. Engagement is evaluated across three outcome metrics: **likes**,
**comments**, and **total engagement** ($\text{likes} + \text{comments}$).
Continuous visual attributes include the predominant color channels (Red, Green,
Blue), the continuous Color Temperature Score, Mean Luminosity, and Mean
Saturation[^1].

### 4.1 Correlation Analysis of Visual Attributes

the bivariate relationships between visual attributes and user engagement
metrics are consistently negligible in magnitude. Although the large sample size
yields statistical significance ($p < 0.05$) for several visual predictors, the
correlation coefficients remain exceedingly close to zero ($|r| < 0.05$),
indicating that isolated visual color dimensions have minimal practical
predictive power for audience interaction.

#### 4.1.1 Correlation with Likes

- Standard luminosity: r = 0.0629 (p = 0.2149)
- Standard saturation Likes represent the primary engagement channel by absolute
  interaction volume. Table 4.1 displays both linear (Pearson $r$) and monotonic
  rank-order (Spearman $\rho$) correlation coefficients between the six
  continuous visual features and post likes.

<!-- this is by engagement_total -->

| Visual Attribute        | Pearson $r$ | $p$-value ($r$) | Spearman $\rho$ | $p$-value ($\rho$) |
| :---------------------- | :---------- | :-------------- | :-------------- | :----------------- |
| Red Channel (R)         | -0.0392     | 0.0005          | -0.0315         | 0.0049             |
| Green Channel (G)       | -0.0383     | 0.0006          | -0.0445         | 0.0001             |
| Blue Channel (B)        | -0.0303     | 0.0070          | -0.0381         | 0.0007             |
| Color Temperature Score | -0.0391     | 0.0005          | -0.0782         | < 0.0001           |
| Mean Luminosity         | -0.0415     | 0.0002          | -0.0412         | 0.0002             |
| Mean Saturation         | +0.0045     | 0.6878          | -0.0032         | 0.7727             |

Taken together, these values indicate that the visual variables examined in this
study explain very little of the variation in engagement. Both linear and
rank-based relationships appear negligible, suggesting that the association
between color properties and likes is weak regardless of the measurement
approach. _Table 4.1: Bivariate correlation coefficients between visual features
and likes ($N = 7,935$)._

4.1 likes The Pearson correlation analysis reveals slight negative associations
between likes and all three RGB color channels, color temperature, and
luminosity, while saturation exhibits virtually zero linear correlation
($r = +0.0045, p = 0.6878$). Spearman rank correlations confirm this monotonic
pattern, with Color Temperature Score exhibiting the highest relative rank
correlation ($\rho = -0.0782, p < 0.0001$). Even in this case, the proportion of
shared variance ($R^2 < 0.006$) is trivial.

<!-- highlight the results in correlation for likes with graphs and a table of each attribute -->

#### 4.1.2 Correlation with Comments

4.2 comments Comments reflect a higher-friction form of user engagement than
likes. Table 4.2 details the associations between visual dimensions and comment
volume.

| Visual Attribute        | Pearson $r$ | $p$-value ($r$) | Spearman $\rho$ | $p$-value ($\rho$) |
| :---------------------- | :---------- | :-------------- | :-------------- | :----------------- |
| Red Channel (R)         | -0.0035     | 0.7533          | -0.0314         | 0.0051             |
| Green Channel (G)       | -0.0018     | 0.8706          | -0.0446         | 0.0001             |
| Blue Channel (B)        | +0.0006     | 0.9582          | -0.0405         | 0.0003             |
| Color Temperature Score | -0.0102     | 0.3613          | -0.0604         | < 0.0001           |
| Mean Luminosity         | +0.0011     | 0.9220          | -0.0448         | 0.0001             |
| Mean Saturation         | +0.0012     | 0.9164          | +0.0238         | 0.0339             |

_Table 4.2: Bivariate correlation coefficients between visual features and
comments ($N = 7,935$)._

In the linear domain, none of the six visual attributes exhibit a statistically
significant Pearson correlation with comments ($p > 0.35$ for all attributes).
In the rank-order domain, subtle negative associations emerge for RGB channels,
luminosity, and temperature, alongside a marginal positive rank correlation for
saturation ($\rho = +0.0238, p = 0.0339$).

#### 4.1.3 Correlation with Total Engagement

Total engagement aggregates likes and comments
($\text{engagement\_total} = \text{likes} + \text{comments}$). Because likes
constitute more than 98.9% of total interactions across the dataset, the
correlation structure for total engagement closely mirrors that of likes.

| Visual Attribute        | Pearson $r$ | $p$-value ($r$) | Spearman $\rho$ | $p$-value ($\rho$) |
| :---------------------- | :---------- | :-------------- | :-------------- | :----------------- |
| Red Channel (R)         | -0.0390     | 0.0005          | -0.0313         | 0.0054             |
| Green Channel (G)       | -0.0381     | 0.0007          | -0.0444         | 0.0001             |
| Blue Channel (B)        | -0.0300     | 0.0076          | -0.0380         | 0.0007             |
| Color Temperature Score | -0.0391     | 0.0005          | -0.0772         | < 0.0001           |
| Mean Luminosity         | -0.0411     | 0.0002          | -0.0405         | 0.0003             |
| Mean Saturation         | +0.0045     | 0.6875          | -0.0035         | 0.7523             |

_Table 4.3: Bivariate correlation coefficients between visual features and total
engagement ($N = 7,935$)._

### 4.2 Group Comparisons: Achromatic vs. Chromatic Images

To test whether categorizing images into neutral (achromatic) versus colorful
(chromatic) aesthetics produces significant differences in engagement,
parametric One-Way ANOVA and non-parametric Kruskal-Wallis tests were conducted.

| Metric               | Achromatic ($n = 4,371$) Mean (SD) | Achromatic Median | Chromatic ($n = 3,564$) Mean (SD) | Chromatic Median | ANOVA $F(1, 7933)$ | ANOVA $p$ | Kruskal-Wallis $H(1)$ | Kruskal-Wallis $p$ |
| :------------------- | :--------------------------------- | :---------------- | :-------------------------------- | :--------------- | :----------------- | :-------- | :-------------------- | :----------------- |
| **Likes**            | 38,622.2 (120,415.1)               | 17,977.0          | 40,256.6 (118,924.5)              | 18,562.5         | 0.3657             | 0.5454    | 1.8988                | 0.1682             |
| **Comments**         | 437.1 (5,287.6)                    | 104.0             | 417.2 (2,861.7)                   | 114.0            | 0.0410             | 0.8395    | 11.6097               | 0.0007             |
| **Total Engagement** | 39,059.3 (121,404.9)               | 18,152.0          | 40,673.7 (120,003.0)              | 18,728.5         | 0.3508             | 0.5537    | 1.9485                | 0.1627             |

_Table 4.4: Comparison of engagement distributions between achromatic and
chromatic images._

For both likes and total engagement, differences in group means are not
statistically significant ($F = 0.3657, p = 0.5454$ for likes;
$F = 0.3508, p = 0.5537$ for total engagement). Due to the positive skewness and
high variance inherent in social media interaction metrics, the Kruskal-Wallis
test serves as a robust distribution-free check; it corroborates the absence of
a meaningful rank shift ($H = 1.8988, p = 0.1682$).

For comments, the parametric ANOVA detects no significant difference in mean
volume ($F = 0.0410, p = 0.8395$), whereas the Kruskal-Wallis test identifies a
slight, statistically significant rank difference favoring chromatic posts
($H = 11.6097, p = 0.0007$), reflected in a marginally higher median comment
count (114 vs. 104).

### 4.3 Categorical Independence: Brand Segment and Color Choice

A Chi-square ($\chi^2$) test of independence was performed on the contingency
table cross-classifying brand segment (fast fashion vs. luxury) and chromaticity
category.

| Segment          | Achromatic ($n$) | Chromatic ($n$) | Total ($n$) | % Achromatic |
| :--------------- | :--------------- | :-------------- | :---------- | :----------- |
| **Fast Fashion** | 1,880            | 1,249           | 3,129       | 60.1%        |
| **Luxury**       | 2,491            | 2,315           | 4,806       | 51.8%        |
| **Total**        | 4,371            | 3,564           | 7,935       | 55.1%        |

_Table 4.5: Contingency table of brand segment against chromaticity
classification._

The test indicates a highly significant association between brand segment and
chromaticity classification ($\chi^2(1) = 51.8275, p = 6.06 \times 10^{-13}$).
Fast-fashion accounts rely significantly more on neutral/achromatic imagery than
luxury accounts. When viewed alongside the group comparison tests in Section
4.2, this demonstrates that visual color distribution is driven primarily by
brand positioning and curation norms rather than by user engagement feedback.

### 4.4 Multiple Regression and Multicollinearity (VIF)

To determine whether visual attributes jointly predict engagement when
considered simultaneously, Ordinary Least Squares (OLS) multiple regression
models were fitted for likes, comments, and total engagement.

| Model Target         | Predictor Variables                      | $R^2$   | Adjusted $R^2$ | $F$-statistic | $p$-value |
| :------------------- | :--------------------------------------- | :------ | :------------- | :------------ | :-------- |
| **Likes**            | Red, Green, Blue, Luminosity, Saturation | 0.00349 | 0.00286        | 5.56          | < 0.0001  |
| **Comments**         | Red, Green, Blue, Luminosity, Saturation | 0.00023 | -0.00040       | 0.36          | 0.8752    |
| **Total Engagement** | Red, Green, Blue, Luminosity, Saturation | 0.00346 | 0.00284        | 5.51          | < 0.0001  |

_Table 4.6: Multiple regression summary across engagement outcomes._

In the model predicting likes, the full set of five visual predictors explains
only $0.35\%$ ($R^2 = 0.00349$) of the total variance. For comments, the
explained variance is virtually zero
($R^2 = 0.00023, \text{Adjusted } R^2 = -0.00040, p = 0.8752$).

#### Multicollinearity Assessment (VIF)

Variance Inflation Factor (VIF) diagnostics were calculated to evaluate
collinearity among the continuous visual predictors:

- **Red Channel (R)**: $\text{VIF} = 10.92$
- **Green Channel (G)**: $\text{VIF} = 46.07$
- **Blue Channel (B)**: $\text{VIF} = 30.83$
- **Mean Luminosity**: $\text{VIF} = 3.98$
- **Mean Saturation**: $\text{VIF} = 1.44$

The elevated VIF values observed among individual color channels reflect natural
inter-channel covariance in pixel RGB representations (where overall brightness
shifts R, G, and B simultaneously). Conversely, Mean Luminosity
($\text{VIF} = 3.98$) and Mean Saturation ($\text{VIF} = 1.44$) remain below
standard multicollinearity thresholds ($\text{VIF} < 5$). When modeling
engagement using the composite Color Temperature Score alongside Luminosity and
Saturation, all VIF values remain strictly low ($\text{VIF} < 1.6$), yielding an
equivalent overall model fit ($R^2 = 0.00252, p < 0.0001$).

---

[^1]: **Variable Definitions**:

- **Red, Green, Blue Channels**: Scaled 0–255, extracted from the primary
  cluster center ($k$-means, $k=5$) of image pixel data.
- **Color Temperature Score**: Continuous warmth metric calculated as
  $\frac{R \times 1.0 + G \times 0.5}{2} - \frac{B \times 1.0 + G \times 0.3}{2}$.
  Higher values indicate warmer (red/orange) hues, while lower values indicate
  cooler (blue/cyan) hues.
- **Mean Luminosity**: Grayscale intensity computed across all image pixels
  (0–255).
- **Mean Saturation**: Mean HSV S-channel intensity computed across all image
  pixels (0–255).

## 5. Discussion

The main result of this study is not that color has no role at all, but that its
isolated effect is too small to explain engagement by itself. The
achromatic/chromatic split is useful as a clean descriptive classification, yet
it does not produce a strong separation in likes.

This supports a multifactorial interpretation of social media engagement.
Factors such as content relevance, audience interest, posting time, caption
quality, account identity, and platform dynamics are likely more important than
the presence or absence of visible color alone. In that sense, the image itself
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
