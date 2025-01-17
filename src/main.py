# main.py

import os
from dotenv import load_dotenv
from youtube_api import get_youtube_client, get_channel_details, format_join_date
from wiki_bot import connect_to_wiki, update_wiki_page, check_page_exists, fetch_channels_needing_updates
from utils import generate_auto_paragraph, generate_wiki_content, combine_content

# Load environment variables
load_dotenv()
API_KEY = os.getenv('API_KEY')
WIKI_URL = os.getenv('WIKI_URL')
WIKI_PATH = os.getenv('WIKI_PATH')
USERNAME = os.getenv('BOT_USERNAME')
PASSWORD = os.getenv('BOT_PASSWORD')
CHANNELS_PAGE_TITLE = os.getenv('CHANNELS_PAGE_TITLE')

# Connect to MediaWiki
site = connect_to_wiki(WIKI_URL, WIKI_PATH, USERNAME, PASSWORD)

# Fetch the list of channels to update from the selected wiki page
CHANNELS_TO_UPDATE = fetch_channels_needing_updates(site, CHANNELS_PAGE_TITLE)

# Initialize YouTube client
youtube = get_youtube_client(API_KEY)

# Iterate over each channel to update
for channel_handle in CHANNELS_TO_UPDATE:
    print(f"Processing channel: {channel_handle}")

    # Fetch channel details using the channel handle
    channel_details = get_channel_details(youtube, channel_handle)
    if not channel_details:
        print(f"Channel '{channel_handle}' not found.")
        continue

    channel_info = channel_details['snippet']
    statistics = channel_details['statistics']
    join_date_raw = channel_info.get('publishedAt', 'Not available')
    join_date = format_join_date(join_date_raw)

    # Generate the content for the MediaWiki page
    auto_paragraph = generate_auto_paragraph(channel_info, join_date, statistics)
    marker_comment, wiki_content = generate_wiki_content(channel_info, channel_handle, join_date, statistics)

    # Check if the page already exists
    page_title = channel_info['title']
    exists, existing_content = check_page_exists(site, page_title)

    # Combine content based on whether the page is new or existing
    new_content = combine_content(existing_content, marker_comment, wiki_content, auto_paragraph if not exists else None)

    # Update the page
    update_wiki_page(site, page_title, new_content, summary=f'Uploaded YouTube channel information for {page_title}')
    print(f"Page '{page_title}' has been updated successfully.")
