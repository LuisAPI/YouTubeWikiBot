# tests/test_wiki_bot.py

import pytest
from unittest.mock import MagicMock, patch
from src.wiki_bot import connect_to_wiki, update_wiki_page, check_page_exists, fetch_channels_needing_updates
from dotenv import load_dotenv
import os

# Load environment variables
load_dotenv()
TEST_WIKI_URL = os.getenv('TEST_WIKI_URL')
TEST_WIKI_PATH = os.getenv('TEST_WIKI_PATH')
TEST_USERNAME = os.getenv('TEST_USERNAME')
TEST_PASSWORD = os.getenv('TEST_PASSWORD')

@pytest.fixture
def mock_site():
    """Fixture to mock mwclient.Site."""
    with patch('mwclient.Site') as MockSite:
        yield MockSite

def test_connect_to_wiki(mock_site):
    """Test connecting to the wiki."""
    mock_site.return_value.login.return_value = True  # Mock successful login

    # Call the function with test settings
    site = connect_to_wiki(TEST_WIKI_URL, TEST_WIKI_PATH, TEST_USERNAME, TEST_PASSWORD)

    # Assertions
    mock_site.assert_called_once_with(TEST_WIKI_URL, path=TEST_WIKI_PATH)
    mock_site.return_value.login.assert_called_once_with(TEST_USERNAME, TEST_PASSWORD)
    assert site == mock_site.return_value

def test_update_wiki_page(mock_site):
    """Test updating a wiki page."""
    mock_page = MagicMock()
    mock_site.return_value.pages.__getitem__.return_value = mock_page  # Mock accessing the page

    # Call the function
    update_wiki_page(mock_site.return_value, 'Test Page', 'New content', 'Test summary')

    # Assertions
    mock_site.return_value.pages.__getitem__.assert_called_once_with('Test Page')
    mock_page.save.assert_called_once_with('New content', summary='Test summary')

def test_check_page_exists(mock_site):
    """Test checking if a wiki page exists."""
    mock_page = MagicMock()
    mock_page.exists = True
    mock_page.text.return_value = "Page content"
    mock_site.return_value.pages.__getitem__.return_value = mock_page  # Mock accessing the page

    # Call the function
    exists, content = check_page_exists(mock_site.return_value, 'Test Page')

    # Assertions
    mock_site.return_value.pages.__getitem__.assert_called_once_with('Test Page')
    assert exists is True
    assert content == "Page content"

def test_fetch_channels_needing_updates(mock_site):
    """Test fetching channels that need updates."""
    mock_page = MagicMock()
    mock_page.text.return_value = """
    * Handle: @example_channel
    * Handle: @another_channel
    """
    mock_site.return_value.pages.__getitem__.return_value = mock_page  # Mock accessing the page

    # Call the function
    channels = fetch_channels_needing_updates(mock_site.return_value, 'Channel Update Requests')

    # Assertions
    mock_site.return_value.pages.__getitem__.assert_called_once_with('Channel Update Requests')
    assert channels == ['@example_channel', '@another_channel']

@pytest.mark.parametrize("page_text, expected_channels", [
    ("* Handle: @channel_one\n* Handle: @channel_two", ['@channel_one', '@channel_two']),
    ("* Handle: @only_channel", ['@only_channel']),
    ("No handles here", []),
    ("* Random text without proper format", []),
])
def test_fetch_channels_needing_updates_various(mock_site, page_text, expected_channels):
    """Test fetching channels under various content scenarios."""
    mock_page = MagicMock()
    mock_page.text.return_value = page_text
    mock_site.return_value.pages.__getitem__.return_value = mock_page  # Mock accessing the page

    # Call the function
    channels = fetch_channels_needing_updates(mock_site.return_value, 'Channel Update Requests')

    # Assertions
    mock_site.return_value.pages.__getitem__.assert_called_once_with('Channel Update Requests')
    assert channels == expected_channels
