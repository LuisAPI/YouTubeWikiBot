import mwclient
from googleapiclient.discovery import build
from dotenv import load_dotenv
import os
from datetime import datetime

# Get environment variables
load_dotenv()
API_KEY = os.getenv('API_KEY')

CHANNEL_USERNAME = 'alanbecker'
WIKI_URL = os.getenv('WIKI_URL')
USERNAME = os.getenv('BOT_USERNAME')
PASSWORD = os.getenv('BOT_PASSWORD')

# Build the YouTube API client
youtube = build('youtube', 'v3', developerKey=API_KEY)

# Request channel details
request = youtube.channels().list(
    part='snippet,contentDetails,statistics',
    forUsername=CHANNEL_USERNAME  # Use 'forUsername' to fetch by username
)
response = request.execute()

# Extract relevant information
channel_info = response['items'][0]['snippet']
page_title = f"{channel_info['title']}"
statistics = response['items'][0]['statistics']
join_date_raw = channel_info.get('publishedAt', 'Not available')

# Format the join date
if join_date_raw != 'Not available':
    join_date = datetime.strptime(join_date_raw, '%Y-%m-%dT%H:%M:%SZ').strftime('%b %d, %Y')
else:
    join_date = 'Not available'

# Create the auto-generated paragraph
auto_generated_paragraph = f"'''{channel_info['title']}''' is a YouTube channel"

# Add the creation date clause
auto_generated_paragraph += f" created on {join_date}"

# Add the subscriber count clause if available
subscriber_count = statistics.get('subscriberCount')
if subscriber_count:
    auto_generated_paragraph += f", with over {subscriber_count} subscribers"

# Add the view count clause if available
view_count = statistics.get('viewCount')
if view_count:
    auto_generated_paragraph += f", and has accumulated {view_count} views"

# End the sentence
auto_generated_paragraph += "."

# Print or use the auto_generated_paragraph in your script as needed
print(auto_generated_paragraph)

# Format the content for the MediaWiki page
marker_comment = """<!--
*         Please leave the bottom part alone         *
*        The channel box is updated regularly        *
■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■-->"""

wiki_content = f"""
{marker_comment}

{{{{Channel page
|channel      = {channel_info['title']}
|channel-link = @{CHANNEL_USERNAME}
|subs         = {statistics.get('subscriberCount', 'N/A')}
|description  =
{channel_info['description']}
|joindate     = {join_date}
|views        = {statistics.get('viewCount', 'N/A')}
|country      = {channel_info.get('country', 'Not specified')}
}}}}
"""

# Connect to the MediaWiki site
site = mwclient.Site(WIKI_URL, path='/')
site.login(USERNAME, PASSWORD)

# Check if the page already exists
page = site.pages[page_title]
existing_content = page.text()

if not page.exists:
    # The page is new, include the auto-generated paragraph
    full_content = auto_generated_paragraph + "\n\n" + wiki_content
else:
    # The page already exists, update without the auto-generated paragraph
    if marker_comment in existing_content:
        # Replace everything before the marker comment
        full_content = existing_content.split(marker_comment)[0] + wiki_content
    else:
        # Append the new content followed by the existing freeform text
        full_content = existing_content + "\n" + wiki_content

# Save the updated content to the page
page.save(full_content, summary=f'Uploaded YouTube channel information for {page_title}')

print(f"Page '{page_title}' has been updated successfully.")
