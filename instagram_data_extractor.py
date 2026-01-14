"""
Instagram Data Extractor
This script extracts data from Instagram API including post_id, photo_url,
like_count, comments_count, metadata, and timestamp.
"""

import requests
import json
import os
from datetime import datetime
from typing import Dict, List, Optional


class InstagramDataExtractor:
    """
    A class to extract data from Instagram API.
    
    Note: This requires Instagram Graph API access token.
    You need to have a Facebook Developer account and create an app
    to get access to Instagram Basic Display API or Instagram Graph API.
    """
    
    def __init__(self, access_token: str):
        """
        Initialize the Instagram Data Extractor.
        
        Args:
            access_token: Instagram API access token
        """
        self.access_token = access_token
        self.base_url = "https://graph.instagram.com"
        
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
            response = requests.get(endpoint, params=params)
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
            response = requests.get(endpoint, params=params)
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
    
    def extract_and_save(self, user_id: str = "me", limit: int = 25, output_file: str = "instagram_data.json"):
        """
        Extract Instagram data and save to file.
        
        Args:
            user_id: Instagram user ID
            limit: Number of posts to retrieve
            output_file: Output filename
        """
        print(f"Fetching media for user: {user_id}")
        media_list = self.get_user_media(user_id, limit)
        
        if not media_list:
            print("No media found or error occurred.")
            return
        
        print(f"Found {len(media_list)} posts. Extracting data...")
        extracted_data = []
        
        for post in media_list:
            extracted_post = self.extract_post_data(post)
            extracted_data.append(extracted_post)
            print(f"Extracted: {extracted_post['post_id']}")
        
        self.save_to_json(extracted_data, output_file)
        print(f"Successfully extracted {len(extracted_data)} posts.")


def main():
    """
    Main function to run the Instagram data extractor.
    
    Usage:
        1. Set your Instagram access token as an environment variable:
           export INSTAGRAM_ACCESS_TOKEN="your_access_token_here"
        
        2. Run the script:
           python instagram_data_extractor.py
    """
    # Get access token from environment variable
    access_token = os.environ.get("INSTAGRAM_ACCESS_TOKEN")
    
    if not access_token:
        print("Error: INSTAGRAM_ACCESS_TOKEN environment variable not set.")
        print("\nTo get an access token:")
        print("1. Go to https://developers.facebook.com/")
        print("2. Create an app and configure Instagram Basic Display or Graph API")
        print("3. Generate an access token")
        print("4. Set it as an environment variable:")
        print("   export INSTAGRAM_ACCESS_TOKEN='your_token_here'")
        return
    
    # Initialize extractor
    extractor = InstagramDataExtractor(access_token)
    
    # Extract and save data
    extractor.extract_and_save(user_id="me", limit=25, output_file="instagram_data.json")


if __name__ == "__main__":
    main()
