"""
Photo Downloader
This script downloads photos from URLs extracted from Instagram data.
"""

import requests
import json
import os
from pathlib import Path
from typing import List, Dict, Optional
import time
from urllib.parse import urlparse


class PhotoDownloader:
    """
    A class to download photos from URLs.
    """
    
    def __init__(self, output_dir: str = "images", max_retries: int = 3, delay_between_downloads: float = 1.0):
        """
        Initialize the Photo Downloader.
        
        Args:
            output_dir: Directory to save downloaded images
            max_retries: Maximum number of retry attempts for failed downloads
            delay_between_downloads: Delay in seconds between downloads to avoid rate limiting
        """
        self.output_dir = output_dir
        self.max_retries = max_retries
        self.delay_between_downloads = delay_between_downloads
        self._create_output_dir()
    
    def _create_output_dir(self):
        """Create the output directory if it doesn't exist."""
        Path(self.output_dir).mkdir(parents=True, exist_ok=True)
        print(f"Output directory: {self.output_dir}")
    
    def _get_filename_from_url(self, url: str, post_id: str) -> str:
        """
        Generate a filename from URL or post_id.
        
        Args:
            url: Photo URL
            post_id: Instagram post ID
            
        Returns:
            Filename for the image
        """
        parsed_url = urlparse(url)
        extension = os.path.splitext(parsed_url.path)[1]
        
        # Default to .jpg if no extension found
        if not extension:
            extension = ".jpg"
        
        # Use post_id as filename to ensure uniqueness
        return f"{post_id}{extension}"
    
    def download_image(self, url: str, filename: str) -> bool:
        """
        Download a single image from URL.
        
        Args:
            url: Image URL
            filename: Output filename
            
        Returns:
            True if download successful, False otherwise
        """
        filepath = os.path.join(self.output_dir, filename)
        
        # Skip if file already exists
        if os.path.exists(filepath):
            print(f"Skipping {filename} (already exists)")
            return True
        
        for attempt in range(self.max_retries):
            try:
                response = requests.get(url, timeout=30, stream=True)
                response.raise_for_status()
                
                with open(filepath, 'wb') as f:
                    for chunk in response.iter_content(chunk_size=8192):
                        if chunk:
                            f.write(chunk)
                
                print(f"Downloaded: {filename}")
                return True
                
            except requests.exceptions.RequestException as e:
                print(f"Attempt {attempt + 1}/{self.max_retries} failed for {filename}: {e}")
                if attempt < self.max_retries - 1:
                    time.sleep(2 ** attempt)  # Exponential backoff
                else:
                    print(f"Failed to download {filename} after {self.max_retries} attempts")
                    return False
        
        return False
    
    def download_from_json(self, json_file: str) -> Dict[str, int]:
        """
        Download all photos from Instagram data JSON file.
        Supports both API extractor and web scraper output formats.
        
        Args:
            json_file: Path to JSON file containing Instagram data
            
        Returns:
            Dictionary with download statistics
        """
        if not os.path.exists(json_file):
            print(f"Error: File {json_file} not found.")
            return {"total": 0, "success": 0, "failed": 0, "skipped": 0}
        
        with open(json_file, 'r', encoding='utf-8') as f:
            data = json.load(f)
        
        stats = {"total": 0, "success": 0, "failed": 0, "skipped": 0}
        
        print(f"Starting download of images from {len(data)} posts...")
        
        for i, post in enumerate(data, 1):
            # Handle API extractor format (single photo_url)
            if "photo_url" in post and post.get("photo_url"):
                photo_urls = [post["photo_url"]]
            # Handle scraper format (multiple media_urls)
            elif "media_urls" in post and post.get("media_urls"):
                photo_urls = post["media_urls"]
            else:
                print(f"Skipping post {i}: No media URLs")
                stats["skipped"] += 1
                continue
            
            post_id = post.get("post_id") or post.get("shortcode", f"post_{i}")
            
            # Download all images from this post
            for j, photo_url in enumerate(photo_urls):
                stats["total"] += 1
                
                # Generate filename
                if len(photo_urls) > 1:
                    filename = self._get_filename_from_url(photo_url, f"{post_id}_{j+1}")
                else:
                    filename = self._get_filename_from_url(photo_url, post_id)
                
                print(f"\n[{i}/{len(data)}] Downloading {filename}...")
                
                if self.download_image(photo_url, filename):
                    stats["success"] += 1
                else:
                    stats["failed"] += 1
                
                # Delay between downloads
                if stats["total"] < sum([len(p.get("media_urls", [p.get("photo_url")] if p.get("photo_url") else [])) for p in data]):
                    time.sleep(self.delay_between_downloads)
        
        return stats
    
    def download_from_url_list(self, urls: List[str], filenames: Optional[List[str]] = None) -> Dict[str, int]:
        """
        Download photos from a list of URLs.
        
        Args:
            urls: List of image URLs
            filenames: Optional list of filenames (must match length of urls)
            
        Returns:
            Dictionary with download statistics
        """
        if filenames and len(urls) != len(filenames):
            raise ValueError("Length of urls and filenames must match")
        
        if not filenames:
            filenames = [f"image_{i:04d}.jpg" for i in range(len(urls))]
        
        stats = {"total": len(urls), "success": 0, "failed": 0, "skipped": 0}
        
        print(f"Starting download of {len(urls)} images...")
        
        for i, (url, filename) in enumerate(zip(urls, filenames), 1):
            print(f"\n[{i}/{len(urls)}] Downloading {filename}...")
            
            if self.download_image(url, filename):
                stats["success"] += 1
            else:
                stats["failed"] += 1
            
            # Delay between downloads
            if i < len(urls):
                time.sleep(self.delay_between_downloads)
        
        return stats
    
    def print_stats(self, stats: Dict[str, int]):
        """
        Print download statistics.
        
        Args:
            stats: Dictionary with download statistics
        """
        print("\n" + "=" * 50)
        print("Download Statistics:")
        print(f"Total attempted: {stats['total']}")
        print(f"Successful: {stats['success']}")
        print(f"Failed: {stats['failed']}")
        print(f"Skipped: {stats['skipped']}")
        print("=" * 50)


def main():
    """
    Main function to run the photo downloader.
    
    Usage:
        python photo_downloader.py [json_file]
    """
    import sys
    
    # Check if a custom JSON file is provided
    if len(sys.argv) > 1:
        json_file = sys.argv[1]
    else:
        # Try both possible JSON files
        if os.path.exists("data/instagram_scraped_data.json"):
            json_file = "data/instagram_scraped_data.json"
        elif os.path.exists("data/instagram_data.json"):
            json_file = "data/instagram_data.json"
        else:
            print("Error: No Instagram data file found.")
            print("\nPlease run one of the following first:")
            print("  - python instagram_scraper.py [username]")
            print("  - python instagram_data_extractor.py")
            return
    
    if not os.path.exists(json_file):
        print(f"Error: {json_file} not found.")
        return
    
    print(f"Using data file: {json_file}")
    
    # Initialize downloader
    downloader = PhotoDownloader(output_dir="images", max_retries=3, delay_between_downloads=1.0)
    
    # Download images
    stats = downloader.download_from_json(json_file)
    
    # Print statistics
    downloader.print_stats(stats)


if __name__ == "__main__":
    main()
