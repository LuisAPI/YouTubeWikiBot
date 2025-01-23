# YouTubeWikiBot

**YouTubeWikiBot** is a bot designed to create a database of the most popular creators on YouTube by fetching channel details and updating a MediaWiki site.

## Features

- Fetches YouTube channel details using the YouTube Data API.
- Updates a MediaWiki site with the fetched channel details.
- Automatically generates content for new and existing wiki pages.

## Installation

1. Clone the repository:
    ```sh
    git clone https://github.com/LuisAPI/YouTubeWikiBot.git
    cd YouTubeWikiBot
    ```

2. Create and activate a virtual environment (optional but recommended):
    ```sh
    python -m venv venv
    source venv/bin/activate  # On Windows use `venv\Scripts\activate`
    ```

3. Install the required dependencies:
    ```sh
    pip install -r requirements.txt
    ```

## Dependencies

The project requires the following dependencies, which are listed in `requirements.txt`:

- `google-api-python-client`: For interacting with the YouTube Data API.
- `python-dotenv`: For loading environment variables from a `.env` file.
- `mwclient`: For interacting with MediaWiki sites.
- `pycountry`: For retrieving full country names from country codes.
- `pytest`: For running tests.
- `setuptools`: For packaging the project.

## Environment Variables

The project relies on several environment variables, which should be defined in a `.env` file in the root directory of the project. Here is an example `.env` file:

```env
API_KEY=your_youtube_api_key
AUTHOR_EMAIL=your_email@example.com
WIKI_URL=your_wiki_url
WIKI_PATH=/w/
BOT_USERNAME=your_bot_username
BOT_PASSWORD=your_bot_password
CHANNELS_PAGE_TITLE=User:YouTubeWikiBot/Filters/Channel Update Requests
TEST_WIKI_URL=your_test_wiki_url
TEST_WIKI_PATH=/w/
TEST_USERNAME=your_test_username
TEST_PASSWORD=your_test_password
```

## Usage

1. Ensure that the `.env` file is correctly configured with your API keys and credentials.
2. Run the main script to fetch channel details and update the wiki:
    ```sh
    python src/main.py
    ```

## Testing

To run the tests, use the following command:
```sh
pytest
```

## Project Structure

```
YouTubeWikiBot/
├── .github/
│   └── workflows/
│       └── python-publish.yml
├── .gitignore
├── .env
├── LICENSE
├── README.md
├── requirements.txt
├── setup.py
├── src/
│   ├── __init__.py
│   ├── main.py
│   ├── utils.py
│   ├── wiki_bot.py
│   └── youtube_api.py
└── tests/
    ├── __init__.py
    └── test_wiki_bot.py
```

## Contributing

Contributions are welcome! Please open an issue or submit a pull request for any improvements or bug fixes.

## License

This project is licensed under the MIT License. See the `LICENSE` file for details.