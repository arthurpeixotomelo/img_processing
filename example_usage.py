"""
Example Usage Script
This script demonstrates how to use the Instagram data extraction and image processing pipeline.
"""

import os
import sys

def print_section(title):
    """Print a formatted section header."""
    print("\n" + "=" * 60)
    print(f"  {title}")
    print("=" * 60 + "\n")


def example_extract_instagram_data():
    """Example: Extract Instagram data using the API."""
    print_section("STEP 1: Extract Instagram Data")
    
    print("Two options available:")
    print("\n**Option A: Web Scraping (Recommended for Public Profiles)**")
    print("Extract from any public Instagram profile without API keys:")
    print("\nExample commands:")
    print("  # Extract from a company profile (e.g., Louis Vuitton)")
    print("  python instagram_scraper.py louisvuitton")
    print("  ")
    print("  # Extract limited posts")
    print("  python instagram_scraper.py louisvuitton --max-posts 12")
    print("  ")
    print("  # Custom output")
    print("  python instagram_scraper.py nike --output nike_posts.json")
    
    print("\nProgrammatic usage:")
    print("""
from instagram_scraper import InstagramScraper

# Initialize scraper
scraper = InstagramScraper(delay_range=(2, 5))

# Scrape and save data
scraper.scrape_and_save('louisvuitton', max_posts=12, output_file='louis_vuitton.json')
    """)
    
    print("\n**Option B: Instagram Graph API (For Accounts You Manage)**")
    print("For Business/Creator accounts connected to Facebook Pages:")
    print("\nExample commands:")
    print("  export INSTAGRAM_ACCESS_TOKEN='your_token_here'")
    print("  ")
    print("  # Extract all posts from your account")
    print("  python instagram_data_extractor.py --all")
    print("  ")
    print("  # Extract from a business account (requires account ID)")
    print("  python instagram_data_extractor.py --user-id 17841405793187218 --all")
    print("  ")
    print("  # Find business account IDs you have access to")
    print("  python get_instagram_id.py")
    
    print("\nProgrammatic usage:")
    print("""
from instagram_data_extractor import InstagramDataExtractor

# Initialize with your access token
extractor = InstagramDataExtractor(access_token='your_token')

# Extract all posts from your account with pagination
extractor.extract_and_save(user_id='me', fetch_all=True)

# Extract all posts from a business account
extractor.extract_and_save(user_id='17841405793187218', fetch_all=True)

# Extract limited posts
extractor.extract_and_save(user_id='me', limit=50, fetch_all=False)
    """)


def example_download_photos():
    """Example: Download photos from URLs."""
    print_section("STEP 2: Download Photos")
    
    print("After extracting Instagram data, download the photos:")
    print("\nExample command:")
    print("  # Auto-detects which JSON file to use")
    print("  python photo_downloader.py")
    print("  ")
    print("  # Or specify a custom file")
    print("  python photo_downloader.py data/instagram_scraped_data.json")
    
    print("\nProgrammatic usage:")
    print("""
from photo_downloader import PhotoDownloader

# Initialize downloader
downloader = PhotoDownloader(output_dir='images', max_retries=3)

# Download from JSON file (works with both scraper and API output)
stats = downloader.download_from_json('data/instagram_scraped_data.json')

# Print statistics
downloader.print_stats(stats)
    """)


def example_analyze_images():
    """Example: Analyze downloaded images."""
    print_section("STEP 3: Analyze Images")
    
    print("Analyze the downloaded images using the Jupyter notebook:")
    print("\nExample command:")
    print("  jupyter notebook image_analysis.ipynb")
    
    print("\nThe notebook will:")
    print("  • Calculate luminosity (grayscale values)")
    print("  • Calculate saturation (median of S in HSV)")
    print("  • Identify predominant colors (K-means clustering)")
    print("  • Generate visualizations")
    print("  • Export results to CSV")
    
    print("\nProgrammatic usage (Python script):")
    print("""
import cv2
import numpy as np
from sklearn.cluster import KMeans

# Load image
image = cv2.imread('images/example.jpg')

# Calculate luminosity
gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
mean_luminosity = np.mean(gray)
print(f'Mean luminosity: {mean_luminosity}')

# Calculate saturation
hsv = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)
saturation = hsv[:, :, 1]
median_saturation = np.median(saturation)
print(f'Median saturation: {median_saturation}')

# Get predominant color
pixels = image.reshape(-1, 3)
kmeans = KMeans(n_clusters=5, random_state=42, n_init=10)
kmeans.fit(pixels)
predominant_color = kmeans.cluster_centers_[0].astype(int)
print(f'Predominant color (BGR): {predominant_color}')
    """)


def example_complete_pipeline():
    """Example: Complete pipeline from extraction to analysis."""
    print_section("Complete Pipeline Example")
    
    print("""
# Web Scraping Approach (Simple - No API Keys)
from instagram_scraper import InstagramScraper
from photo_downloader import PhotoDownloader

# Step 1: Scrape Instagram data
scraper = InstagramScraper(delay_range=(2, 5))
scraper.scrape_and_save('louisvuitton', max_posts=12)

# Step 2: Download photos
downloader = PhotoDownloader(output_dir='images')
stats = downloader.download_from_json('data/instagram_scraped_data.json')
downloader.print_stats(stats)

# Step 3: Analyze images (use Jupyter notebook for full analysis)
print("Run 'jupyter notebook image_analysis.ipynb' to analyze images")

# OR using API Approach (Official - Requires Auth)
import os
from instagram_data_extractor import InstagramDataExtractor
from photo_downloader import PhotoDownloader

access_token = os.environ.get('INSTAGRAM_ACCESS_TOKEN')
if access_token:
    # Step 1: Extract Instagram data
    extractor = InstagramDataExtractor(access_token)
    extractor.extract_and_save(user_id='me', fetch_all=True)
    
    # Step 2: Download photos
    downloader = PhotoDownloader(output_dir='images')
    stats = downloader.download_from_json('data/instagram_data.json')
    downloader.print_stats(stats)
    
    # Step 3: Analyze images
    print("Run 'jupyter notebook image_analysis.ipynb' to analyze images")
else:
    print("Please set INSTAGRAM_ACCESS_TOKEN or use the web scraper")
    """)


def main():
    """Main function to display all examples."""
    print("\n" + "=" * 60)
    print("  Instagram Image Processing Pipeline - Usage Examples")
    print("=" * 60)
    
    print("\nThis script demonstrates how to use the Instagram data")
    print("extraction and image processing pipeline.")
    
    example_extract_instagram_data()
    example_download_photos()
    example_analyze_images()
    example_complete_pipeline()
    
    print_section("Additional Resources")
    print("• README.md - Full documentation")
    print("• requirements.txt - Required dependencies")
    print("• Instagram Graph API: https://developers.facebook.com/docs/instagram-api/")
    print("\n")


if __name__ == "__main__":
    main()
