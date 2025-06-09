# wiki_bot.py

import mwclient
import re

def connect_to_wiki(wiki_url, wiki_path, username, password):
    """Connects to the MediaWiki site."""
    site = mwclient.Site(wiki_url, path=wiki_path)
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

def fetch_channels_needing_updates(site, page_title):
    """Fetches the list of channels needing updates from the specified wiki page."""
    page = site.pages[page_title]
    content = page.text()

    channels = []
    for line in content.splitlines():
        if line.lstrip().startswith('*'):
            match = re.search(r'@[^\s)]+', line)
            if match:
                channels.append(match.group(0))

    return channels
