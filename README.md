# Data Web Scraper

## Project Description

The Data Web Scraper is a versatile Python-based tool designed to extract structured data from websites. It leverages `requests` for fetching web content and `BeautifulSoup` for efficient HTML parsing. Users can define specific target URLs and data points using CSS selectors within a configuration file, and the scraped data can then be exported to either CSV or JSON formats. This project is ideal for automating data collection tasks, market research, content aggregation, and building datasets from web sources.

## Features

*   **Configurable Targets**: Easily define multiple target URLs and the specific data elements to scrape via `config.py`.
*   **Flexible Selectors**: Utilizes CSS selectors for precise and robust data extraction from HTML documents.
*   **Multiple Export Formats**: Supports exporting scraped data to industry-standard CSV and JSON file formats.
*   **Error Handling**: Includes mechanisms for gracefully handling common issues such as network errors, HTTP status codes, and missing elements.
*   **Modular Design**: The codebase is structured into distinct modules (`scraper.py`, `exporter.py`, `utils.py`) for improved maintainability, readability, and scalability.
*   **Virtual Environment Support**: Encourages best practices for dependency management using Python virtual environments.

## Tech Stack

*   **Python 3.x**: The core programming language.
*   **BeautifulSoup4**: A Python library for parsing HTML and XML documents, making it easy to extract data.
*   **Requests**: An elegant and simple HTTP library for Python, used for making web requests.

## Installation

To set up and run the Data Web Scraper on your local machine, follow these steps:

1.  **Clone the repository**:
    ```bash
    git clone https://github.com/your-username/data-web-scraper.git
    cd data-web-scraper
    ```
    (Replace `your-username` with the actual GitHub username or organization.)

2.  **Create a virtual environment**:
    It's highly recommended to use a virtual environment to isolate project dependencies.
    ```bash
    python3 -m venv venv
    ```

3.  **Activate the virtual environment**:
    *   On macOS/Linux:
        ```bash
        source venv/bin/activate
        ```
    *   On Windows:
        ```bash
        .\venv\Scripts\activate
        ```

4.  **Install dependencies**:
    Install all required Python packages listed in `requirements.txt`.
    ```bash
    pip install -r requirements.txt
    ```

## Configuration

The scraper's behavior is primarily controlled by the `config.py` file. You must configure this file to specify the websites to scrape, the data points to extract, and the desired output format.

Here's an example of what your `config.py` might look like:

```python
# config.py

# Define the target URLs and the data points to scrape.
# Each entry in TARGET_CONFIG should be a dictionary with:
# - 'url': The URL of the web page to scrape.
# - 'name': A unique name for this scraping task (used for naming output files).
# - 'selectors': A dictionary where keys are desired data field names (e.g., 'title', 'price')
#                and values are CSS selectors to extract that data.
#                For selectors that might return multiple elements (e.g., a list of tags),
#                the scraper logic in `src/scraper.py` is designed to collect all matching
#                elements (e.g., into a list of strings).
#                Example: "div.quote span.text::text" will get the text of the first matching element.
#                Example: "div.quote div.tags a.tag::text" will get texts of all matching tags.

TARGET_CONFIG = [
    {
        "url": "http://quotes.toscrape.com/",
        "name": "quotes_page_1",
        "selectors": {
            "quote_text": "div.quote span.text::text",
            "author": "div.quote small.author::text",
            "tags": "div.quote div.tags a.tag::text" # This selector will capture all tag texts into a list
        }
    },
    {
        "url": "http://quotes.toscrape.com/page/2/",
        "name": "quotes_page_2",
        "selectors": {
            "quote_text": "div.quote span.text::text",
            "author": "div.quote small.author::text",
            "tags": "div.quote div.tags a.tag::text"
        }
    }
    # Add more target configurations as needed for different pages or websites
]

# Define the desired output format ('csv' or 'json').
EXPORT_FORMAT = "json" # Can be "csv" or "json"

# Define the directory where output files will be saved.
# This directory will be created automatically if it does not exist.
OUTPUT_DIR = "output"

# Optional: Request headers to mimic a browser. This can help avoid being blocked by some websites.
HEADERS = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10