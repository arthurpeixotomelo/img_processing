"""
Instagram Web Scraper
This script extracts data from public Instagram profiles using web scraping.

WARNING: Web scraping Instagram may violate Instagram's Terms of Service.
Use this script responsibly and at your own risk. Consider rate limiting and
respect Instagram's robots.txt file.

This script extracts:
- Post images (single or multiple)
- Like count
- Comment count
- Timestamp
- Caption text (including hashtags)
"""

import requests
from bs4 import BeautifulSoup
import json
import os
import time
from datetime import datetime
from typing import Dict, List, Optional
import re
from urllib.parse import urljoin
import random


class InstagramScraper:
    """
    A class to scrape data from public Instagram profiles.
    
    Note: This uses web scraping which may be against Instagram's ToS.
    Use responsibly and implement appropriate rate limiting.
    """
    
    def __init__(self, delay_range=(2, 5)):
        """
        Initialize the Instagram Scraper.
        
        Args:
            delay_range: Tuple of (min, max) seconds to wait between requests
        """
        self.delay_range = delay_range
        self.session = requests.Session()
        
        # Set headers to mimic a real browser
        self.session.headers.update({
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
            'Accept-Language': 'en-US,en;q=0.5',
            'Accept-Encoding': 'gzip, deflate, br',
            'DNT': '1',
            'Connection': 'keep-alive',
            'Upgrade-Insecure-Requests': '1'
        })
    
    def _random_delay(self):
        """Add random delay between requests to avoid being blocked."""
        delay = random.uniform(self.delay_range[0], self.delay_range[1])
        time.sleep(delay)
    
    def get_profile_page(self, username: str) -> Optional[str]:
        """
        Fetch the profile page HTML for a given username.
        
        Args:
            username: Instagram username (without @)
            
        Returns:
            HTML content of the profile page or None if failed
        """
        url = f"https://www.instagram.com/{username}/"
        
        try:
            print(f"Fetching profile page for @{username}...")
            response = self.session.get(url, timeout=30)
            response.raise_for_status()
            
            if response.status_code == 200:
                return response.text
            else:
                print(f"Failed to fetch profile. Status code: {response.status_code}")
                return None
                
        except requests.exceptions.RequestException as e:
            print(f"Error fetching profile: {e}")
            return None
    
    def extract_shared_data(self, html: str) -> Optional[Dict]:
        """
        Extract the shared data JSON from Instagram's page HTML.
        
        Instagram embeds post data in a JavaScript variable called window._sharedData
        
        Args:
            html: HTML content of the page
            
        Returns:
            Dictionary containing shared data or None if not found
        """
        try:
            # Look for the shared data in script tags
            soup = BeautifulSoup(html, 'html.parser')
            
            # Try to find the script tag with window._sharedData
            scripts = soup.find_all('script', type='text/javascript')
            
            for script in scripts:
                if script.string and 'window._sharedData' in script.string:
                    # Extract the JSON data
                    match = re.search(r'window\._sharedData\s*=\s*({.+?});', script.string)
                    if match:
                        json_data = json.loads(match.group(1))
                        return json_data
            
            # Alternative: Look for application/json script tags (newer Instagram format)
            for script in soup.find_all('script', type='application/ld+json'):
                if script.string:
                    try:
                        json_data = json.loads(script.string)
                        return json_data
                    except json.JSONDecodeError:
                        continue
            
            print("Could not find shared data in page HTML")
            return None
            
        except Exception as e:
            print(f"Error extracting shared data: {e}")
            return None
    
    def parse_post_data(self, post_node: Dict) -> Dict:
        """
        Parse a post node from Instagram's data structure.
        
        Args:
            post_node: Dictionary containing post data
            
        Returns:
            Cleaned dictionary with extracted post information
        """
        try:
            # Extract basic information
            post_id = post_node.get('id', '')
            shortcode = post_node.get('shortcode', '')
            
            # Get media URLs
            media_urls = []
            if post_node.get('is_video'):
                media_urls.append(post_node.get('video_url', ''))
            else:
                display_url = post_node.get('display_url', '')
                if display_url:
                    media_urls.append(display_url)
            
            # Check for carousel (multiple images)
            edge_sidecar = post_node.get('edge_sidecar_to_children', {})
            if edge_sidecar and 'edges' in edge_sidecar:
                media_urls = []
                for edge in edge_sidecar['edges']:
                    node = edge.get('node', {})
                    if node.get('is_video'):
                        media_urls.append(node.get('video_url', ''))
                    else:
                        media_urls.append(node.get('display_url', ''))
            
            # Extract engagement metrics
            edge_liked_by = post_node.get('edge_liked_by', {}) or post_node.get('edge_media_preview_like', {})
            like_count = edge_liked_by.get('count', 0)
            
            edge_comments = post_node.get('edge_media_to_comment', {}) or post_node.get('edge_media_preview_comment', {})
            comment_count = edge_comments.get('count', 0)
            
            # Extract caption
            caption = ''
            edge_caption = post_node.get('edge_media_to_caption', {})
            if edge_caption and 'edges' in edge_caption and len(edge_caption['edges']) > 0:
                caption = edge_caption['edges'][0].get('node', {}).get('text', '')
            
            # Extract timestamp
            timestamp = post_node.get('taken_at_timestamp', 0)
            if timestamp:
                timestamp = datetime.fromtimestamp(timestamp).isoformat()
            
            # Build post URL
            post_url = f"https://www.instagram.com/p/{shortcode}/" if shortcode else ''
            
            return {
                'post_id': post_id,
                'shortcode': shortcode,
                'post_url': post_url,
                'media_urls': media_urls,
                'like_count': like_count,
                'comment_count': comment_count,
                'caption': caption,
                'timestamp': timestamp,
                'is_video': post_node.get('is_video', False),
                'extracted_at': datetime.now().isoformat()
            }
            
        except Exception as e:
            print(f"Error parsing post data: {e}")
            return {}
    
    def scrape_profile(self, username: str, max_posts: Optional[int] = None) -> List[Dict]:
        """
        Scrape posts from a public Instagram profile.
        
        Args:
            username: Instagram username (without @)
            max_posts: Maximum number of posts to scrape (None for all available)
            
        Returns:
            List of post dictionaries
        """
        print(f"\n{'='*60}")
        print(f"Scraping Instagram profile: @{username}")
        print(f"{'='*60}\n")
        
        # Fetch profile page
        html = self.get_profile_page(username)
        if not html:
            print("Failed to fetch profile page.")
            return []
        
        # Extract shared data
        shared_data = self.extract_shared_data(html)
        if not shared_data:
            print("Failed to extract data from page.")
            print("\nNote: Instagram may have changed its page structure or you may be blocked.")
            print("Consider using the Instagram API with proper authentication instead.")
            return []
        
        # Navigate through the data structure to find posts
        posts = []
        
        try:
            # Try different possible data structures
            entry_data = shared_data.get('entry_data', {})
            
            if 'ProfilePage' in entry_data:
                profile_page = entry_data['ProfilePage'][0]
                graphql = profile_page.get('graphql', {})
                user = graphql.get('user', {})
                edge_owner_to_timeline_media = user.get('edge_owner_to_timeline_media', {})
                edges = edge_owner_to_timeline_media.get('edges', [])
                
                print(f"Found {len(edges)} posts on the initial page load.")
                
                for edge in edges:
                    if max_posts and len(posts) >= max_posts:
                        break
                    
                    node = edge.get('node', {})
                    post_data = self.parse_post_data(node)
                    
                    if post_data:
                        posts.append(post_data)
                        print(f"Extracted post {len(posts)}: {post_data.get('shortcode', 'N/A')}")
                
            else:
                print("Could not find ProfilePage in entry_data")
                print("Available keys:", list(entry_data.keys()))
        
        except Exception as e:
            print(f"Error extracting posts: {e}")
        
        print(f"\nTotal posts extracted: {len(posts)}")
        
        return posts
    
    def save_to_json(self, data: List[Dict], filename: str = "instagram_scraped_data.json"):
        """
        Save scraped data to a JSON file.
        
        Args:
            data: List of post dictionaries
            filename: Output filename
        """
        output_dir = "data"
        os.makedirs(output_dir, exist_ok=True)
        filepath = os.path.join(output_dir, filename)
        
        with open(filepath, "w", encoding="utf-8") as f:
            json.dump(data, f, indent=2, ensure_ascii=False)
        
        print(f"\nData saved to {filepath}")
    
    def scrape_and_save(self, username: str, max_posts: Optional[int] = None, output_file: str = "instagram_scraped_data.json"):
        """
        Scrape Instagram profile and save to file.
        
        Args:
            username: Instagram username (without @)
            max_posts: Maximum number of posts to scrape
            output_file: Output filename
        """
        posts = self.scrape_profile(username, max_posts)
        
        if posts:
            self.save_to_json(posts, output_file)
            print(f"\nSuccessfully scraped {len(posts)} posts from @{username}")
        else:
            print(f"\nNo posts extracted from @{username}")
            print("\nPossible reasons:")
            print("1. The account is private")
            print("2. The account doesn't exist")
            print("3. Instagram's page structure has changed")
            print("4. You may be rate-limited or blocked")
            print("\nConsider using Instagram's official API with proper authentication.")


def main():
    """
    Main function to run the Instagram scraper.
    
    Usage:
        python instagram_scraper.py [username] [--max-posts N]
        
    Examples:
        python instagram_scraper.py louisvuitton
        python instagram_scraper.py louisvuitton --max-posts 12
    """
    import argparse
    
    parser = argparse.ArgumentParser(
        description='Scrape public Instagram profiles',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
WARNING: Web scraping may violate Instagram's Terms of Service.
Use this script responsibly and at your own risk.

Examples:
  python instagram_scraper.py louisvuitton
  python instagram_scraper.py louisvuitton --max-posts 12
  python instagram_scraper.py nike --output nike_posts.json

Note: This only works with public Instagram profiles and may not work
if Instagram changes its page structure or implements blocking mechanisms.
        """
    )
    
    parser.add_argument('username', help='Instagram username (without @)')
    parser.add_argument('--max-posts', type=int, help='Maximum number of posts to scrape')
    parser.add_argument('--output', default='instagram_scraped_data.json', help='Output filename')
    parser.add_argument('--delay-min', type=float, default=2.0, help='Minimum delay between requests (seconds)')
    parser.add_argument('--delay-max', type=float, default=5.0, help='Maximum delay between requests (seconds)')
    
    args = parser.parse_args()
    
    # Initialize scraper
    scraper = InstagramScraper(delay_range=(args.delay_min, args.delay_max))
    
    # Scrape and save
    scraper.scrape_and_save(args.username, args.max_posts, args.output)
    
    print("\n" + "="*60)
    print("IMPORTANT DISCLAIMER")
    print("="*60)
    print("This script uses web scraping, which may violate Instagram's")
    print("Terms of Service. Use at your own risk and responsibility.")
    print("For production use, consider using Instagram's official API")
    print("with proper authentication and permissions.")
    print("="*60)


if __name__ == "__main__":
    main()
