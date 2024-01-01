import os
from pathlib import Path

# --- Project Paths ---
# Define the base directory of the project. This helps in resolving paths relative to the project root.
# __file__ is the current file (config.py), .resolve() gets its absolute path,
# .parent gets the directory of config.py, and .parent again gets the project root.
BASE_DIR = Path(__file__).resolve().parent.parent

# Define the directory where scraped data will be stored.
OUTPUT_DIR = BASE_DIR / "output"
# Ensure the output directory exists. If it doesn't, create it along with any necessary parent directories.
OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

# --- Scraping Configuration ---
# Default User-Agent string to mimic a web browser.
# It's crucial for avoiding detection as a bot and for receiving proper content.
# Loaded from environment variable USER_AGENT, with a robust default.
DEFAULT_USER_AGENT = os.getenv(
    "USER_AGENT",
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"
)

# Timeout for HTTP requests in seconds. Prevents requests from hanging indefinitely.
# Loaded from environment variable REQUEST_TIMEOUT_SECONDS, default to 10 seconds.
REQUEST_TIMEOUT_SECONDS = int(os.getenv("REQUEST_TIMEOUT_SECONDS", 10))

# Number of times to retry a failed HTTP