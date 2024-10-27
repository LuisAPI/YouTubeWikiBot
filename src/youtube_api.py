# youtube_api.py

from googleapiclient.discovery import build
from datetime import datetime

def get_youtube_client(api_key):
    """Build the YouTube API client."""
    return build('youtube', 'v3', developerKey=api_key)

def get_channel_details(youtube, username):
    """Fetches the channel details for the given handle."""
    request = youtube.channels().list(
        part='snippet,contentDetails,statistics',
        forHandle=username
    )
    response = request.execute()
    return response['items'][0] if response['items'] else None

def format_join_date(join_date_raw):
    # Try parsing with fractional seconds first
    try:
        return datetime.strptime(join_date_raw, '%Y-%m-%dT%H:%M:%S.%fZ').strftime('%b %d, %Y')
    except ValueError:
        # Fallback to the original format without fractional seconds
        return datetime.strptime(join_date_raw, '%Y-%m-%dT%H:%M:%SZ').strftime('%b %d, %Y')