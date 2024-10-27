# wiki_bot.py

import mwclient

def connect_to_wiki(wiki_url, username, password):
    """Connects to the MediaWiki site."""
    site = mwclient.Site(wiki_url, path='/')
    site.login(username, password)
    return site

def update_wiki_page(site, page_title, new_content, summary):
    """Updates the specified wiki page with the given content."""
    page = site.pages[page_title]
    page.save(new_content, summary=summary)
    return page

def check_page_exists(site, page_title):
    """Checks if the page already exists on the wiki."""
    page = site.pages[page_title]
    return page.exists, page.text()

def fetch_channels_needing_updates(wiki_url, page_title, username, password):
    # Connect to the MediaWiki site
    site = mwclient.Site(wiki_url, path='/')
    site.login(username, password)
    
    # Access the specified page
    page = site.pages[page_title]
    content = page.text()
    
    # Parse the content to find channels (assumes a simple list format)
    channels = []
    lines = content.splitlines()
    for line in lines:
        if line.startswith('*'):
            # Extract the channel handle from the line
            channel_info = line.split('(')
            if len(channel_info) > 1:
                # Get the handle without "Handle: " label
                channel_handle = channel_info[1].replace('Handle: ', '').strip(') ')
                channels.append(channel_handle)
    
    return channels
