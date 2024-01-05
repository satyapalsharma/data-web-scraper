import logging
import os
import time
import random
import functools
from urllib.parse import urlparse, urljoin
from typing import Optional, Callable, Tuple, Type, Any

# Import project-specific configuration
try:
    import config
except ImportError:
    # Fallback for environments where config.py might not be directly in the path
    # or for testing purposes. In production, config.py should always be available.
    class ConfigFallback:
        LOG_FILE = "scraper.log"
        USER_AGENTS = [
            "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36",
            "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36",
            "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:89.0) Gecko/20100101 Firefox/89.0",
            "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/14.1.1 Safari/605.1.15",
        ]
        # Add other necessary config defaults if they are used in utils
        # For example, if a default output directory is needed here:
        # OUTPUT_DIR = "output"
    config = ConfigFallback()

# Define a custom exception for retry mechanism if needed, or use existing ones
class MaxRetriesExceededError(Exception):
    """Custom exception raised when a function exceeds its maximum retry attempts."""
    pass

def setup_logging(log_level: int = logging.INFO) -> None:
    """
    Configures the logging system for the application.

    Logs messages to both the console and a file specified in config.py.
    The log file is rotated daily and compressed.

    Args:
        log_level (int): The minimum level of messages to log (e.g., logging.INFO, logging.DEBUG).
    """
    log_file_path = config.LOG_FILE
    log_directory = os.path.dirname(log_file_path)

    # Ensure the log directory exists
    if log_directory and not os.path.exists(log_directory):
        os.makedirs(log_directory, exist_ok=True)

    # Basic configuration for the root logger
    logging.basicConfig(
        level=log_level,
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
        handlers=[
            # Console handler
            logging.StreamHandler(),
            # File handler with daily rotation
            logging.handlers.TimedRotatingFileHandler(
                filename=log_file_path,
                when='midnight',
                interval=1,
                backupCount=7,  # Keep 7 days of logs
                encoding='utf-8'
            )
        ]
    )
    logging.getLogger(__name__).info(f"Logging configured. Log file: {log_file_path}")

def ensure_directory_exists(path: str) -> None:
    """
    Ensures that a directory exists. If it doesn't, it creates it.

    Args:
        path (str): The path to the directory.
    """
    if not os.path.exists(path):
        try:
            os.makedirs(path, exist_ok=True)
            logging.getLogger(__name__).info(f"Created directory: {path}")
        except OSError as e:
            logging.getLogger(__name__).error(f"Error creating directory {path}: {e}")
            raise # Re-raise the exception as it's a critical failure

def normalize_url(url: str, base_url: Optional[str] = None) -> Optional[str]:
    """
    Normalizes a URL by ensuring it has a scheme and resolving relative paths.

    Args:
        url (str): The URL to normalize.
        base_url (Optional[str]): An optional base URL to resolve relative URLs against.

    Returns:
        Optional[str]: The normalized URL, or None if the URL is invalid after normalization.
    """
    if not url:
        return None

    # If a base_url is provided, resolve relative URLs
    if base_url:
        url = urljoin(base_url, url)

    parsed_url = urlparse(url)

    # Ensure the URL has a scheme (e.g., http, https)
    if not parsed_url.scheme:
        # Default to https if no scheme is present, or if it's a common case like "//example.com"
        if url.startswith('//'):
            url = 'https:' + url
        else:
            url = 'https://' + url # Or 'http://' depending on common use case

        parsed_url = urlparse(url) # Re-parse after adding scheme

    # Basic validation: must have a scheme and a network location
    if not parsed_url.scheme or not parsed_url.netloc:
        logging.getLogger(__name__).warning(f"Invalid URL after normalization: {url}")
        return None

    # Reconstruct the URL to ensure consistency (e.g., removing default ports)
    # This also handles cases like 'example.com' becoming 'https://example.com'
    normalized = parsed_url.geturl()
    return normalized

def get_random_user_agent() -> str:
    """
    Returns a random user-agent string from the configured list.

    Returns:
        str: A randomly selected user-agent string.
    """
    if not config.USER_AGENTS:
        logging.getLogger(__name__).warning("No user agents configured. Using a default fallback.")
        return "Mozilla/5.0 (compatible; Googlebot/2.1; +http://www.google.com/bot.html)"
    return random.choice(config.USER_AGENTS)

def retry_on_exception(
    retries: int = 3,
    delay: float = 1.0,
    backoff_factor: float = 2.0,
    exceptions: Tuple[Type[Exception], ...] = (Exception,),
    logger: Optional[logging.Logger] = None
) -> Callable:
    """
    A decorator that retries a function call if specified exceptions occur.

    Args:
        retries (int): The maximum number of times to retry the function.
        delay (float): The initial delay in seconds between retries.
        backoff_factor (float): Factor by which the delay will increase each time.
                                (e.g., delay, delay * backoff_factor, delay * backoff_factor^2, ...)
        exceptions (Tuple[Type[Exception], ...]): A tuple of exception types to catch and retry on.
        logger (Optional[logging.Logger]): A logger instance to use for logging retry attempts.
                                           If None, a default logger will be used.

    Returns:
        Callable: A decorator that can be applied to functions.
    """
    if logger is None:
        logger = logging.getLogger(__name__)

    def decorator(func: Callable) -> Callable:
        @functools.wraps(func)
        def wrapper(*args: Any, **kwargs: Any) -> Any:
            _retries = retries
            _delay = delay
            while _retries > 0:
                try:
                    return func(*args, **kwargs)
                except exceptions as e:
                    _retries -= 1
                    if _retries == 0:
                        logger.error(f"Function '{func.__name__}' failed after {retries} attempts. Last error: {e}")
                        raise MaxRetriesExceededError(
                            f"Function '{func.__name__}' failed after {retries} attempts."
                        ) from e
                    logger.warning(
                        f"Function '{func.__name__}' failed with {type(e).__name__}. "
                        f"Retrying in {_delay:.2f} seconds... ({_retries} attempts left)"
                    )
                    time.sleep(_delay)
                    _delay *= backoff_factor
            # This part should ideally not be reached if MaxRetriesExceededError is always raised
            # but included for completeness.
            raise MaxRetriesExceededError(f"Function '{func.__name__}' failed without reaching max retries logic.")
        return wrapper
    return decorator

# Initialize logging when the module is imported
setup_logging()