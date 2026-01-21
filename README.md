# Instagram Image Processing Pipeline

A comprehensive Python-based pipeline for extracting Instagram data, downloading images, and performing image analysis to extract luminosity, saturation, and predominant color information.

## Features

### 1. Instagram Data Extraction

#### Option A: Web Scraper (`instagram_scraper.py`) - **RECOMMENDED for Public Profiles**
Extract data from any public Instagram profile without API access:
- Works with any public Instagram account (no authorization needed)
- Extracts all visible posts from profile page
- Multiple images per post supported
- Post ID/shortcode, photo URLs, like count, comments count
- Timestamp and caption (with hashtags)
- **No API keys or permissions required**

**Note:** Web scraping may violate Instagram's Terms of Service. Use responsibly.

#### Option B: API Extractor (`instagram_data_extractor.py`)
Extract data from Instagram Graph API (requires authorization):
- Post ID, photo URL, like count, comments count
- Timestamp and other metadata
- **Limitations:** Only works with Business/Creator accounts you manage

### 2. Photo Downloader (`photo_downloader.py`)
Download images from extracted URLs with:
- Automatic retry mechanism
- Progress tracking
- Rate limiting
- Error handling

### 3. Image Analysis (`image_analysis.ipynb`)
Analyze downloaded images to extract:
- **Luminosity**: Mean and median grayscale values
- **Saturation**: Median of S channel in HSV color space
- **Predominant Color**: K-means clustering with color percentages
- Statistical summaries and visualizations

## Installation

1. Clone the repository:
```bash
git clone https://github.com/arthurpeixotomelo/img_processing.git
cd img_processing
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

## Usage

### Step 1: Extract Instagram Data

#### Option A: Web Scraping (Recommended for Public Profiles)

Extract data from any public Instagram profile without API keys:

```bash
# Extract posts from a public profile (e.g., Louis Vuitton)
python instagram_scraper.py louisvuitton

# Extract limited number of posts
python instagram_scraper.py louisvuitton --max-posts 12

# Custom output filename
python instagram_scraper.py nike --output nike_posts.json
```

**Advantages:**
- Works with any public profile (no API access needed)
- No authorization or permissions required
- Extracts multiple images per post
- Simple and straightforward

**Limitations:**
- May violate Instagram's Terms of Service
- Only gets posts visible on initial page load (typically 12 posts)
- Doesn't work with private accounts
- May break if Instagram changes their page structure

This will create a `data/instagram_scraped_data.json` file.

#### Option B: Instagram Graph API (For Accounts You Manage)

For accounts connected to Facebook Pages you manage:

1. Get an Instagram API access token from [Facebook Developers](https://developers.facebook.com/)
2. Set your access token:
   ```bash
   export INSTAGRAM_ACCESS_TOKEN='your_access_token_here'
   ```

3. Extract data:
   ```bash
   # Extract all posts from your account
   python instagram_data_extractor.py --all
   
   # Extract from a business account (requires account ID)
   python instagram_data_extractor.py --user-id 17841405793187218 --all
   
   # Find business account IDs you have access to
   python get_instagram_id.py
   ```

**Advantages:**
- Official API (complies with ToS)
- Can fetch all posts with pagination
- More reliable and structured data

**Limitations:**
- Requires API access token
- Only works with Business/Creator accounts
- Account must be connected to a Facebook Page you manage
- Cannot extract from arbitrary public profiles

This creates a `data/instagram_data.json` file.

### Step 2: Download Photos

Download images from the extracted URLs:
```bash
# Auto-detects which JSON file to use (scraper or API output)
python photo_downloader.py

# Or specify a custom JSON file
python photo_downloader.py data/instagram_scraped_data.json
```

The downloader automatically handles:
- Multiple images per post (for carousel posts)
- Retry mechanism with exponential backoff
- Rate limiting
- Skipping already downloaded files

Images will be saved to the `images/` directory.

### Step 3: Analyze Images

Open and run the Jupyter notebook:
```bash
jupyter notebook image_analysis.ipynb
```

The notebook will:
1. Load all downloaded images
2. Calculate luminosity (grayscale analysis)
3. Calculate saturation (median of S in HSV)
4. Identify predominant colors using K-means clustering
5. Generate visualizations and statistics
6. Export results to CSV

## Project Structure

```
img_processing/
├── instagram_scraper.py           # Web scraper for public profiles (RECOMMENDED)
├── instagram_data_extractor.py    # API-based extractor (requires auth)
├── get_instagram_id.py            # Helper to find Instagram Business Account IDs
├── photo_downloader.py            # Download photos from URLs (works with both)
├── image_analysis.ipynb           # Jupyter notebook for image analysis
├── requirements.txt               # Python dependencies
├── data/                          # Directory for JSON data (created automatically)
│   ├── instagram_scraped_data.json  # Scraped Instagram data
│   └── instagram_data.json          # API extracted data
├── images/                        # Directory for downloaded images (created automatically)
└── image_analysis_results.csv     # Analysis results (generated by notebook)
```

## API Requirements

### Instagram Graph API

The `instagram_data_extractor.py` script uses the Instagram Graph API. You need:

- A Facebook Developer account
- An Instagram Business or Creator account (for the account you want to extract from)
- An app configured with Instagram Graph API permissions:
  - `instagram_basic` - Read posts and media
  - `pages_show_list` - Access connected Facebook Pages
  - `instagram_manage_insights` (optional) - For insights data
- A valid access token

**Limitations:**
- You can only extract data from Instagram Business/Creator accounts
- The account must be connected to a Facebook Page you manage
- Personal Instagram accounts cannot be accessed via Graph API (use Basic Display API instead)
- Rate limits apply (200 calls per hour per user)

For more information, visit:
- [Instagram Graph API Documentation](https://developers.facebook.com/docs/instagram-api/)
- [Instagram Basic Display API](https://developers.facebook.com/docs/instagram-basic-display-api/)

## Output Examples

### Extracted Data (JSON)
```json
{
  "post_id": "1234567890",
  "photo_url": "https://instagram.com/...",
  "permalink": "https://www.instagram.com/p/...",
  "like_count": 150,
  "comments_count": 23,
  "timestamp": "2024-01-14T12:00:00+0000",
  "caption": "Beautiful sunset!",
  "media_type": "IMAGE",
  "username": "example_user"
}
```

### Analysis Results (CSV)
The notebook generates a CSV file with columns:
- filename
- width, height, channels
- mean_luminosity, median_luminosity, std_luminosity
- mean_saturation, median_saturation, std_saturation
- predominant_color, predominant_color_percentage

## Dependencies

- **requests**: API calls and image downloads
- **opencv-python**: Image processing
- **numpy**: Numerical operations
- **pandas**: Data manipulation
- **scikit-learn**: K-means clustering
- **matplotlib/seaborn**: Visualizations
- **jupyter**: Interactive analysis

See `requirements.txt` for complete list.

## Notes

- The Instagram API has rate limits; the downloader includes delays between requests
- Access tokens expire and need to be refreshed periodically
- Large image collections may take time to download and analyze
- The K-means clustering for color detection uses 5 clusters by default (configurable)

## License

MIT License

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.