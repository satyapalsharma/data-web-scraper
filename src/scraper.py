import logging
import time
from typing import Any, Dict, List, Optional, Union

import requests
from bs4 import BeautifulSoup, Tag

# Assuming config.py exists and has necessary configurations
# This import allows the scraper to pick up global settings.
try:
    from config import SCRAPER_CONFIG
except ImportError:
    # Provide a default minimal configuration if config.py is not yet available
    # This is useful for initial development or testing.
    logging.warning("config.py not found or SCRAPER_CONFIG not defined. Using default scraper configuration.")
    SCRAPER_CONFIG = {
        "USER_AGENT": "Mozilla/5.0 (compatible; DataWebScraper/1.0; +http://your-project-url