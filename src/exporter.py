import csv
import json
import logging
from typing import List, Dict, Any, Optional

# Configure logging for the exporter module.
# In a production application, logging configuration would typically be centralized
# in `main.py` or `config.py`. This setup ensures that if this module is used
# independently, it still provides useful log output.
logger = logging.getLogger(__name__)
if not logger.handlers:
    logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')


def export_to_csv(
    data: List[Dict[str, Any]],
    filepath: str,
    fieldnames: Optional[List[str]] = None
) -> bool:
    """
    Exports a list of dictionaries to a CSV file.

    Each dictionary is treated as a row, and its keys are used as column headers.
    If `fieldnames` is not provided, it infers them from the keys of the first
    dictionary in the `data` list.

    Args:
        data: A list of dictionaries, where each dictionary represents a row.
              All dictionaries should ideally have consistent keys for best CSV output.
              If a dictionary has keys not in `fieldnames`, they will be ignored.
              If a dictionary is missing keys present in `fieldnames`, those cells
              will be left empty.
        filepath: The full path to the output CSV file (e.g., "output/scraped_data.csv").
        fieldnames: An optional list of strings specifying the CSV header order.
                    If None, fieldnames are inferred from the keys of the first
                    dictionary in the data list.

    Returns:
        True if the export was successful, False otherwise.
    """
    if not data:
        logger.warning(f"No data provided to export to CSV: '{filepath}'. Skipping export.")
        return False

    if fieldnames is None:
        # Infer fieldnames from the keys of the first dictionary.
        # This assumes the first dictionary is representative of the data structure.
        fieldnames = list(data[0].keys())
        logger.debug(f"Inferred CSV fieldnames: {fieldnames}")

    try:
        # 'w' mode for writing, 'newline=''' to prevent extra blank rows on Windows,
        # 'encoding='utf-8'' for broad character support.
        with open(filepath, 'w', newline='', encoding='utf-8') as csvfile:
            # DictWriter maps dictionaries to CSV rows using fieldnames as headers.
            writer = csv.DictWriter(csvfile, fieldnames=fieldnames)

            writer.writeheader()  # Write the header row based on fieldnames
            writer.writerows(data)  # Write all data rows

        logger.info(f"Successfully exported {len(data)} items to CSV: '{filepath}'")
        return True
    except IOError as e:
        logger.error(f"Error writing to CSV file '{filepath}': {e}")
        return False
    except Exception as e:
        # Catch any other unexpected errors during the export process.
        logger.error(f"An unexpected error occurred during CSV export to '{filepath}': {e}")
        return False


def export_to_json(
    data: List[Dict[str, Any]],
    filepath: str,
    indent: Optional[int] = 4
) -> bool:
    """
    Exports a list of dictionaries to a JSON file.

    Args:
        data: A list of dictionaries to be exported.
        filepath: The full path to the output JSON file (e.g., "output/scraped_data.json").
        indent: The indentation level for pretty-printing the JSON output.
                Set to None for the most compact JSON output (no indentation).

    Returns:
        True if the export was successful, False otherwise.
    """
    if not data:
        logger.warning(f"No data provided to export to JSON: '{filepath}'. Skipping export.")
        return False

    try:
        # 'w' mode for writing, 'encoding='utf-8'' for broad character support.
        with open(filepath, 'w', encoding='utf-8') as jsonfile:
            # json.dump writes the Python object `data` to the file `jsonfile`.
            # `indent` makes the output human-readable.
            # `ensure_ascii=False` allows non-ASCII characters to be written directly
            # instead of being escaped, making the JSON more readable and often smaller.
            json.dump(data, jsonfile, indent=indent, ensure_ascii=False)

        logger.info(f"Successfully exported {len(data)} items to JSON: '{filepath}'")
        return True
    except IOError as e:
        logger.error(f"Error writing to JSON file '{filepath}': {e}")
        return False
    except Exception as e:
        # Catch any other unexpected errors during the export process.
        logger.error(f"An unexpected error occurred during JSON export to '{filepath}': {e}")
        return False


# Example usage (for testing purposes, typically moved to `main.py` or a dedicated test file)
if __name__ == "__main__":
    # Sample data mimicking scraped results
    sample_scraped_data = [
        {"product_name": "Laptop Pro X", "price": 1200.50, "currency": "USD", "in_stock": True, "category": "Electronics"},
        {"product_name": "Mechanical Keyboard", "price": 85.00, "currency": "USD", "in_stock": False, "category": "Accessories"},
        {"product_name": "Wireless Mouse", "price": 25.99, "currency": "USD", "in_stock": True, "rating": 4.5}, # Missing 'category', added 'rating'
        {"product_name": "USB-C Hub", "price": 49.99, "currency": "USD", "in_stock": True, "category": "Accessories"}
    ]

    output_dir = "output"
    import os
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)
        logger.info(f"Created output directory: {output_dir}")

    print("\n--- Testing CSV Export ---")
    csv_filepath_inferred = os.path.join(output_dir, "scraped_data_inferred.csv")
    print(f"Exporting to: {csv_filepath_inferred}")
    export_to_csv(sample_scraped_data, csv_filepath_inferred)

    csv_filepath_specified = os.path.join(output_dir, "scraped_data_specified.csv")
    print(f"Exporting to: {csv_filepath_specified} (with specified fieldnames)")
    # Demonstrate specifying fieldnames, which can reorder or exclude columns
    export_to_csv(sample_scraped_data, csv_filepath_specified,
                  fieldnames=["product_name", "category", "price", "in_stock"])

    csv_filepath_empty = os.path.join(output_dir, "scraped_data_empty.csv")
    print(f"Exporting empty data to: {csv_filepath_empty}")
    export_to_csv([], csv_filepath_empty)

    print("\n--- Testing JSON Export ---")
    json_filepath_pretty = os.path.join(output_dir, "sc