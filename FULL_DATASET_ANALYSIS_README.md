# Full Dataset Statistical Analysis Notebook

## Overview
This notebook (`full_dataset_statistical_analysis.ipynb`) provides a comprehensive statistical analysis of the full Instagram fashion image dataset (401 images) with enhanced RGB color classification.

## Key Features

### 1. Data Loading and Preprocessing
- Loads the complete dataset from `image_analysis_results_full.csv` (401 records)
- Extracts RGB values from predominant colors
- Handles missing values
- Creates both original and RGB-based color classifications

### 2. RGB Color Classification
The notebook implements a robust RGB classification system that categorizes images into:
- **Achromatic colors**: Black/Dark, White/Light, Gray/Neutral
- **Single-channel dominant**: Red Dominant, Green Dominant, Blue Dominant
- **Two-channel combinations**: Yellow/Warm (R+G), Magenta/Purple (R+B), Cyan/Cool (G+B)
- **Balanced**: Mixed/Balanced

This provides a more fundamental color perspective compared to the original 8-9 semantic color categories.

### 3. Statistical Analyses Performed

#### Correlation Analysis
- **Pearson correlation**: Linear relationships between features and engagement
- **Spearman correlation**: Non-linear rank-based relationships
- Comprehensive correlation heatmaps for visual features vs engagement metrics

#### Statistical Tests
- **ANOVA (F-test)**: Tests if color categories have significantly different engagement levels
- **Kruskal-Wallis Test**: Non-parametric alternative to ANOVA
- **Chi-Square Test**: Association between color categories and engagement levels
- **Multiple Regression**: Predicts engagement based on multiple visual features
- **VIF Analysis**: Checks for multicollinearity in predictive features

### 4. Visualizations
- Distribution plots for luminosity, saturation, RGB channels, and engagement metrics
- Correlation heatmaps (Pearson and Spearman)
- Box plots comparing engagement across color categories
- Scatter plots with trend lines for key relationships
- Bar charts comparing original vs RGB classification performance

### 5. Comparative Analysis
- Compares findings between original color categories (8-9 categories) and RGB-based categories
- Shows how results differ when using broader RGB categories vs specific color names
- Demonstrates differences from small dataset analysis

## How to Use

1. **Install dependencies** (if not already installed):
   ```bash
   pip install pandas numpy matplotlib seaborn scipy scikit-learn statsmodels
   ```

2. **Open the notebook**:
   ```bash
   jupyter notebook full_dataset_statistical_analysis.ipynb
   ```

3. **Run all cells**: Execute cells sequentially to perform the complete analysis

## Key Findings

The notebook generates comprehensive insights including:
- Correlation strengths between visual features and engagement
- Statistical significance of color categories on engagement
- Comparison of RGB vs semantic color classification effectiveness
- Variance explained by visual features in predicting engagement
- Individual RGB channel correlations with engagement metrics

## Differences from Initial Notebook

This notebook differs from `image_analysis.ipynb` by:
1. Using advanced statistical techniques (ANOVA, Chi-Square, VIF, Multiple Regression)
2. Implementing RGB-based color classification alongside original categories
3. Providing more robust statistical inferences
4. Offering comparative analysis between classification schemes
5. Analyzing the full dataset to identify differences from small sample findings

## Output

The notebook produces:
- Statistical tables showing correlations, means, medians, and variances
- Multiple visualizations (heatmaps, distributions, box plots, scatter plots)
- P-values and test statistics for hypothesis testing
- Detailed insights and conclusions section
- Comparison metrics between classification schemes

## Notes

- The notebook automatically handles missing values in the engagement data
- All statistical tests report both test statistics and p-values
- Visualizations are configured for publication-quality output
- Results highlight the multifactorial nature of social media engagement

## Requirements

- Python 3.8+
- Jupyter Notebook or JupyterLab
- Required packages: pandas, numpy, matplotlib, seaborn, scipy, scikit-learn, statsmodels
- Input file: `image_analysis_results_full.csv` (must be in the same directory)
