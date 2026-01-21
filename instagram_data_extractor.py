"""
Instagram Data Extractor
This script extracts data from Instagram API including post_id, photo_url,
like_count, comments_count, metadata, and timestamp.

Supports extracting data from:
- Authenticated user's account (user_id="me")
- Any Instagram Business Account by username (e.g., @louisvuitton)
"""

import requests
import json
import os
from datetime import datetime
from typing import Dict, List, Optional
import time


class InstagramDataExtractor:
    """
    A class to extract data from Instagram API.
    
    Note: This requires Instagram Graph API access token.
    You need to have a Facebook Developer account and create an app
    to get access to Instagram Graph API.
    
    For extracting data from other business accounts:
    - The target account must be an Instagram Business or Creator account
    - Your app needs the instagram_basic and pages_show_list permissions
    """
    
    def __init__(self, access_token: str):
        """
        Initialize the Instagram Data Extractor.
        
        Args:
            access_token: Instagram API access token
        """
        self.access_token = access_token
        self.base_url = "https://graph.instagram.com"
        self.facebook_api_url = "https://graph.facebook.com/v18.0"
        
    def get_business_account_id(self, username: str) -> Optional[str]:
        """
        Get Instagram Business Account ID from username.
        
        Note: This requires the Instagram account to be a Business or Creator account.
        For public accounts, you may need to use the Instagram Basic Display API
        or scraping methods (not recommended due to ToS).
        
        Args:
            username: Instagram username (without @)
            
        Returns:
            Instagram Business Account ID or None if not found
        """
        # Note: Instagram Graph API doesn't provide a direct username-to-ID lookup
        # This is a limitation of the API. Users need to provide the account ID directly
        # or use alternative methods like the Facebook Pages API if they manage the page.
        
        print(f"Note: Instagram Graph API requires the Instagram Business Account ID.")
        print(f"For username '{username}', you need to obtain the account ID through:")
        print("1. If you manage the page: Use Facebook Graph API to get connected Instagram accounts")
        print("2. Use Instagram Basic Display API (for personal accounts)")
        print("3. Contact the account owner to provide their Instagram Business Account ID")
        
        return None
    
    def get_all_media_paginated(self, user_id: str, max_posts: Optional[int] = None) -> List[Dict]:
        """
        Get all media posts from Instagram with pagination support.
        
        Args:
            user_id: Instagram user ID or "me" for authenticated user
            max_posts: Maximum number of posts to retrieve (None for all posts)
            
        Returns:
            List of all media posts with metadata
        """
        all_media = []
        endpoint = f"{self.base_url}/{user_id}/media"
        params = {
            "fields": "id,caption,media_type,media_url,permalink,timestamp,like_count,comments_count,username",
            "access_token": self.access_token,
            "limit": 100  # Maximum allowed per request
        }
        
        print(f"Starting to fetch media for user: {user_id}")
        page_count = 0
        
        while True:
            try:
                page_count += 1
                print(f"Fetching page {page_count}...")
                
                response = requests.get(endpoint, params=params, timeout=30)
                response.raise_for_status()
                data = response.json()
                
                # Add posts from current page
                posts = data.get("data", [])
                all_media.extend(posts)
                
                print(f"Retrieved {len(posts)} posts from page {page_count}. Total: {len(all_media)}")
                
                # Check if we've reached max_posts limit
                if max_posts and len(all_media) >= max_posts:
                    all_media = all_media[:max_posts]
                    print(f"Reached maximum limit of {max_posts} posts.")
                    break
                
                # Check for pagination
                paging = data.get("paging", {})
                next_url = paging.get("next")
                
                if not next_url:
                    print("No more pages to fetch.")
                    break
                
                # Update endpoint and params for next page
                endpoint = next_url
                params = {}  # Next URL already includes all parameters
                
                # Small delay to respect rate limits
                time.sleep(0.5)
                
            except requests.exceptions.RequestException as e:
                print(f"Error fetching media on page {page_count}: {e}")
                break
        
        print(f"Finished fetching. Total posts retrieved: {len(all_media)}")
        return all_media
    
    def get_user_media(self, user_id: str = "me", limit: int = 25) -> List[Dict]:
        """
        Get user's media posts from Instagram.
        
        Args:
            user_id: Instagram user ID (default: "me" for authenticated user)
            limit: Number of posts to retrieve
            
        Returns:
            List of media posts with metadata
        """
        endpoint = f"{self.base_url}/{user_id}/media"
        params = {
            "fields": "id,caption,media_type,media_url,permalink,timestamp,like_count,comments_count,username",
            "access_token": self.access_token,
            "limit": limit
        }
        
        try:
            response = requests.get(endpoint, params=params, timeout=30)
            response.raise_for_status()
            return response.json().get("data", [])
        except requests.exceptions.RequestException as e:
            print(f"Error fetching media: {e}")
            return []
    
    def get_media_details(self, media_id: str) -> Optional[Dict]:
        """
        Get detailed information about a specific media post.
        
        Args:
            media_id: Instagram media ID
            
        Returns:
            Dictionary containing media details
        """
        endpoint = f"{self.base_url}/{media_id}"
        params = {
            "fields": "id,caption,media_type,media_url,permalink,timestamp,like_count,comments_count,username,children",
            "access_token": self.access_token
        }
        
        try:
            response = requests.get(endpoint, params=params, timeout=30)
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            print(f"Error fetching media details: {e}")
            return None
    
    def extract_post_data(self, post: Dict) -> Dict:
        """
        Extract relevant data from a post.
        
        Args:
            post: Raw post data from Instagram API
            
        Returns:
            Dictionary with extracted data
        """
        return {
            "post_id": post.get("id"),
            "photo_url": post.get("media_url"),
            "permalink": post.get("permalink"),
            "like_count": post.get("like_count", 0),
            "comments_count": post.get("comments_count", 0),
            "timestamp": post.get("timestamp"),
            "caption": post.get("caption", ""),
            "media_type": post.get("media_type"),
            "username": post.get("username"),
            "extracted_at": datetime.now().isoformat()
        }
    
    def save_to_json(self, data: List[Dict], filename: str = "instagram_data.json"):
        """
        Save extracted data to a JSON file.
        
        Args:
            data: List of extracted post data
            filename: Output filename
        """
        output_dir = "data"
        os.makedirs(output_dir, exist_ok=True)
        filepath = os.path.join(output_dir, filename)
        
        with open(filepath, "w", encoding="utf-8") as f:
            json.dump(data, f, indent=2, ensure_ascii=False)
        
        print(f"Data saved to {filepath}")
    
    def extract_and_save(self, user_id: str = "me", limit: Optional[int] = 25, output_file: str = "instagram_data.json", fetch_all: bool = False):
        """
        Extract Instagram data and save to file.
        
        Args:
            user_id: Instagram user ID or Business Account ID
            limit: Number of posts to retrieve (ignored if fetch_all=True)
            output_file: Output filename
            fetch_all: If True, fetches all posts with pagination (ignores limit)
        """
        print(f"Fetching media for user: {user_id}")
        
        if fetch_all:
            print("Fetching ALL posts (pagination enabled)...")
            media_list = self.get_all_media_paginated(user_id, max_posts=None)
        else:
            print(f"Fetching up to {limit} posts...")
            media_list = self.get_user_media(user_id, limit)
        
        if not media_list:
            print("No media found or error occurred.")
            return
        
        print(f"Found {len(media_list)} posts. Extracting data...")
        extracted_data = []
        
        for i, post in enumerate(media_list, 1):
            extracted_post = self.extract_post_data(post)
            extracted_data.append(extracted_post)
            if i % 50 == 0:
                print(f"Extracted {i}/{len(media_list)} posts...")
        
        self.save_to_json(extracted_data, output_file)
        print(f"Successfully extracted {len(extracted_data)} posts.")
    
    def extract_by_username(self, username: str, output_file: str = "instagram_data.json", fetch_all: bool = True):
        """
        Extract Instagram data by username (for Business/Creator accounts).
        
        Note: This is a convenience method that requires you to provide the Business Account ID.
        Instagram Graph API doesn't support direct username lookup.
        
        Args:
            username: Instagram username (without @)
            output_file: Output filename
            fetch_all: If True, fetches all posts with pagination
        """
        print(f"Attempting to extract data for @{username}")
        print("\nIMPORTANT: Instagram Graph API requires the Instagram Business Account ID.")
        print("Please provide the account ID instead of username, or use one of these methods:")
        print("1. If you manage the account: Get the ID from Facebook Business Manager")
        print("2. Use the account ID directly in extract_and_save(user_id='ACCOUNT_ID')")
        print("\nFor now, this method cannot proceed without the account ID.")
        
        return None


def main():
    """
    Main function to run the Instagram data extractor.
    
    Usage:
        1. Set your Instagram access token as an environment variable:
           export INSTAGRAM_ACCESS_TOKEN="your_access_token_here"
        
        2. Run the script with optional command-line arguments:
           python instagram_data_extractor.py [--user-id USER_ID] [--all] [--limit N]
           
        Examples:
           # Extract all posts from authenticated user
           python instagram_data_extractor.py --all
           
           # Extract 50 posts from authenticated user
           python instagram_data_extractor.py --limit 50
           
           # Extract all posts from a specific business account (requires account ID)
           python instagram_data_extractor.py --user-id 17841405793187218 --all
    """
    import argparse
    
    # Parse command line arguments
    parser = argparse.ArgumentParser(description='Extract Instagram post data')
    parser.add_argument('--user-id', default='me', help='Instagram user ID or Business Account ID (default: "me")')
    parser.add_argument('--all', action='store_true', help='Fetch all posts with pagination')
    parser.add_argument('--limit', type=int, default=25, help='Number of posts to fetch (default: 25, ignored if --all is used)')
    parser.add_argument('--output', default='instagram_data.json', help='Output filename (default: instagram_data.json)')
    
    args = parser.parse_args()
    
    # Get access token from environment variable
    access_token = os.environ.get("INSTAGRAM_ACCESS_TOKEN")
    
    if not access_token:
        print("Error: INSTAGRAM_ACCESS_TOKEN environment variable not set.")
        print("\nTo get an access token:")
        print("1. Go to https://developers.facebook.com/")
        print("2. Create an app and configure Instagram Graph API")
        print("3. Generate an access token")
        print("4. Set it as an environment variable:")
        print("   export INSTAGRAM_ACCESS_TOKEN='your_token_here'")
        return
    
    # Initialize extractor
    extractor = InstagramDataExtractor(access_token)
    
    # Extract and save data
    if args.user_id != "me":
        print(f"\nNote: Extracting from Business Account ID: {args.user_id}")
        print("Make sure this is a valid Instagram Business Account ID that you have access to.\n")
    
    extractor.extract_and_save(
        user_id=args.user_id, 
        limit=args.limit, 
        output_file=args.output,
        fetch_all=args.all
    )


if __name__ == "__main__":
    main()
