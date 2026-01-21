"""
Helper Script: Get Instagram Business Account ID

This script helps you find the Instagram Business Account ID for a company/brand
that you want to extract data from.

IMPORTANT: 
- The Instagram account must be a Business or Creator account
- You need to have the appropriate permissions to access the account's data
- For public accounts that you don't own, you typically need them to grant you access
"""

import requests
import os
import sys


def get_instagram_business_accounts(access_token):
    """
    Get list of Instagram Business Accounts you have access to.
    
    This works if you manage the Instagram account through a Facebook Page.
    
    Args:
        access_token: Facebook/Instagram access token with appropriate permissions
    """
    # First, get Facebook Pages
    url = "https://graph.facebook.com/v18.0/me/accounts"
    params = {
        "access_token": access_token,
        "fields": "id,name,instagram_business_account"
    }
    
    try:
        print("Fetching your Facebook Pages...")
        response = requests.get(url, params=params, timeout=30)
        response.raise_for_status()
        data = response.json()
        
        pages = data.get("data", [])
        
        if not pages:
            print("\nNo Facebook Pages found.")
            print("To extract data from an Instagram Business Account:")
            print("1. The Instagram account must be connected to a Facebook Page")
            print("2. You must be an admin of that Facebook Page")
            return
        
        print(f"\nFound {len(pages)} Facebook Page(s):\n")
        
        instagram_accounts = []
        for page in pages:
            page_name = page.get("name")
            page_id = page.get("id")
            ig_account = page.get("instagram_business_account")
            
            print(f"Facebook Page: {page_name} (ID: {page_id})")
            
            if ig_account:
                ig_id = ig_account.get("id")
                instagram_accounts.append({
                    "page_name": page_name,
                    "instagram_id": ig_id
                })
                print(f"  ✓ Connected Instagram Business Account ID: {ig_id}")
            else:
                print(f"  ✗ No Instagram Business Account connected")
            
            print()
        
        if instagram_accounts:
            print("=" * 60)
            print("Instagram Business Account IDs you can access:")
            print("=" * 60)
            for acc in instagram_accounts:
                print(f"Page: {acc['page_name']}")
                print(f"Instagram ID: {acc['instagram_id']}")
                print(f"\nTo extract data from this account, use:")
                print(f"  python instagram_data_extractor.py --user-id {acc['instagram_id']} --all")
                print()
        else:
            print("No Instagram Business Accounts found.")
            print("\nTo connect an Instagram Business Account:")
            print("1. Go to your Facebook Page settings")
            print("2. Navigate to Instagram section")
            print("3. Connect your Instagram Business Account")
    
    except requests.exceptions.RequestException as e:
        print(f"Error: {e}")
        print("\nMake sure your access token has the following permissions:")
        print("- pages_show_list")
        print("- instagram_basic")
        print("- instagram_manage_insights")


def get_instagram_account_info(instagram_id, access_token):
    """
    Get information about a specific Instagram Business Account.
    
    Args:
        instagram_id: Instagram Business Account ID
        access_token: Access token
    """
    url = f"https://graph.facebook.com/v18.0/{instagram_id}"
    params = {
        "fields": "id,username,name,profile_picture_url,followers_count,follows_count,media_count",
        "access_token": access_token
    }
    
    try:
        response = requests.get(url, params=params, timeout=30)
        response.raise_for_status()
        data = response.json()
        
        print("\nInstagram Account Information:")
        print("=" * 60)
        print(f"ID: {data.get('id')}")
        print(f"Username: @{data.get('username')}")
        print(f"Name: {data.get('name')}")
        print(f"Followers: {data.get('followers_count', 'N/A')}")
        print(f"Following: {data.get('follows_count', 'N/A')}")
        print(f"Posts: {data.get('media_count', 'N/A')}")
        print("=" * 60)
        
        return data
        
    except requests.exceptions.RequestException as e:
        print(f"Error fetching account info: {e}")
        return None


def main():
    """Main function."""
    import argparse
    
    parser = argparse.ArgumentParser(
        description='Get Instagram Business Account IDs',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  # List all Instagram Business Accounts you have access to
  python get_instagram_id.py
  
  # Get info about a specific Instagram Business Account
  python get_instagram_id.py --account-id 17841405793187218
  
Note: Set INSTAGRAM_ACCESS_TOKEN environment variable with your access token.
        """
    )
    
    parser.add_argument(
        '--account-id', 
        help='Get info for a specific Instagram Business Account ID'
    )
    
    args = parser.parse_args()
    
    # Get access token
    access_token = os.environ.get("INSTAGRAM_ACCESS_TOKEN")
    
    if not access_token:
        print("Error: INSTAGRAM_ACCESS_TOKEN environment variable not set.")
        print("\nTo get an access token:")
        print("1. Go to https://developers.facebook.com/")
        print("2. Create an app and add Instagram Graph API")
        print("3. Generate an access token with required permissions:")
        print("   - pages_show_list")
        print("   - instagram_basic")
        print("   - instagram_manage_insights (optional, for insights)")
        print("4. Set it as an environment variable:")
        print("   export INSTAGRAM_ACCESS_TOKEN='your_token_here'")
        sys.exit(1)
    
    if args.account_id:
        # Get info for specific account
        get_instagram_account_info(args.account_id, access_token)
    else:
        # List all accessible accounts
        get_instagram_business_accounts(access_token)
    
    print("\n" + "=" * 60)
    print("IMPORTANT NOTES:")
    print("=" * 60)
    print("• You can only extract data from Instagram Business/Creator accounts")
    print("• The account must be connected to a Facebook Page you manage")
    print("• For accounts you don't manage (like @louisvuitton):")
    print("  - You cannot extract their data without authorization")
    print("  - They would need to grant your app access")
    print("  - Consider using official Instagram partnerships or APIs")
    print("=" * 60)


if __name__ == "__main__":
    main()
