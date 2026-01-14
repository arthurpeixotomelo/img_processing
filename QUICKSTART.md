# Quick Start Guide

Get started with the Instagram Image Processing Pipeline in 3 easy steps!

## Prerequisites

- Python 3.8 or higher
- Instagram API access token (see below)
- pip package manager

## Step 1: Install Dependencies

```bash
pip install -r requirements.txt
```

## Step 2: Get Instagram Access Token

### Option A: Instagram Basic Display API (for personal use)

1. Go to [Facebook Developers](https://developers.facebook.com/)
2. Click "My Apps" → "Create App"
3. Select "Consumer" type
4. Add "Instagram Basic Display" product
5. Configure OAuth redirect URIs
6. Get your access token from the "User Token Generator"

### Option B: Instagram Graph API (for business accounts)

1. Go to [Facebook Developers](https://developers.facebook.com/)
2. Create or select a Facebook app
3. Add "Instagram Graph API" product
4. Link your Instagram Business Account
5. Generate a User Access Token with required permissions

## Step 3: Run the Pipeline

### 3.1 Extract Instagram Data

```bash
# Set your access token
export INSTAGRAM_ACCESS_TOKEN='YOUR_TOKEN_HERE'

# Run the extractor
python instagram_data_extractor.py
```

**Output:** `data/instagram_data.json`

### 3.2 Download Photos

```bash
python photo_downloader.py
```

**Output:** Images saved to `images/` directory

### 3.3 Analyze Images

```bash
jupyter notebook image_analysis.ipynb
```

**Actions:**
- Run all cells in the notebook (Cell → Run All)
- View generated visualizations
- Check `image_analysis_results.csv` for exported data

## Example Output

After running the complete pipeline, you'll have:

```
img_processing/
├── data/
│   └── instagram_data.json        # Extracted Instagram data
├── images/
│   ├── 1234567890.jpg              # Downloaded images
│   ├── 1234567891.jpg
│   └── ...
└── image_analysis_results.csv      # Analysis results
```

## Troubleshooting

### "Access token expired"
- Instagram access tokens expire after 1 hour (short-lived) or 60 days (long-lived)
- Generate a new token or implement token refresh logic

### "No media found"
- Ensure your access token has the correct permissions
- Check that your Instagram account has posts
- Verify the account type (Personal vs Business)

### "Failed to download image"
- Check internet connectivity
- Some Instagram URLs may expire
- The script automatically retries failed downloads

### Import errors
- Ensure all dependencies are installed: `pip install -r requirements.txt`
- Check Python version: `python --version` (should be 3.8+)

## What Gets Analyzed?

The image analysis notebook extracts:

1. **Luminosity Metrics**
   - Mean and median brightness
   - Standard deviation
   - Min/max values

2. **Saturation Metrics**
   - Median saturation (HSV color space)
   - Mean saturation
   - Distribution statistics

3. **Color Analysis**
   - Top 5 predominant colors
   - Percentage of each color
   - RGB values for each color

## Next Steps

- Customize analysis parameters in the notebook (e.g., number of color clusters)
- Export data to different formats (JSON, Excel, etc.)
- Build visualizations and dashboards
- Compare images across different time periods

## Need Help?

- Check the full documentation in `README.md`
- View example code in `example_usage.py`
- Refer to [Instagram API documentation](https://developers.facebook.com/docs/instagram-api/)

Happy analyzing! 🎨📸
