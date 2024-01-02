import argparse
import logging
import sys
import os

# Local project imports
import config
from src.scraper import Scraper, ScraperError
from src.exporter import Exporter, ExporterError
from src.utils import setup_logging # Assuming setup_logging is defined in src/utils.py

# Initialize logger for main.py
logger = logging.getLogger(__name__)

def main():
    """
    Main function to orchestrate the web scraping and data export process.
    It handles argument parsing, configuration loading, scraping, and exporting.
    """
    # 1. Setup Logging
    # Configure the root logger based on project standards.
    # This function should be defined in src/utils.py to keep main.py clean.
    setup_logging()

    # 2. Argument Parsing
    # Define command-line arguments to allow overriding default configuration.
    parser = argparse.ArgumentParser(
        description="Scrape structured data from websites and export to CSV or JSON.",
        formatter_class=argparse.ArgumentDefaultsHelpFormatter
    )
    parser.add_argument(
        "-u", "--url",
        help="Override the target URL(s) specified in config. If provided, this argument "
             "will replace the list of URLs in config.py with this single URL for scraping."
    )
    parser.add_argument(
        "-f", "--output-format",
        choices=["csv", "json"],
        help="Override the output format (csv or json) specified in config.py."
    )
    parser.add_argument(
        "-o", "--output-file",
        help="Override the output file path. Default is based on config.py."
    )
    parser.add_argument(
        "-v", "--verbose",
        action="store_true",
        help="Enable verbose logging (DEBUG level) for more detailed output."
    )

    args = parser.parse_args()

    # 3. Load Configuration
    # Start with the default configuration loaded from config.py.
    app_config = config.get_config()

    # Override configuration with command-line arguments if provided.
    if args.url:
        # If a single URL is provided via CLI, replace the list in config with it.
        app_config['urls'] = [args.url]
        logger.info(f"Overriding URL(s) with CLI argument: '{args.url}'")
    if args.output_