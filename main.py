import argparse
import logging
import requests
from bs4 import BeautifulSoup
import pandas as pd
import re
import os  # For checking file existence
import sys

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

def setup_argparse():
    """
    Sets up the argument parser for the script.

    Returns:
        argparse.ArgumentParser: The argument parser object.
    """
    parser = argparse.ArgumentParser(description='Scrapes OSINT sources for mentions of keywords or IOCs.')
    parser.add_argument('-k', '--keywords', nargs='+', help='List of keywords to search for.', required=False)
    parser.add_argument('-i', '--ioc_file', type=str, help='Path to a file containing IOCs (one per line).', required=False)
    parser.add_argument('-u', '--urls', nargs='+', help='List of URLs to scrape.', required=True)
    parser.add_argument('-o', '--output', type=str, help='Output CSV file path.', default='output.csv')
    parser.add_argument('--max_pages', type=int, default=1, help='Maximum number of pages to scrape per URL.  Useful for sites with pagination. Defaults to 1.')
    return parser

def read_iocs_from_file(ioc_file_path):
    """
    Reads IOCs from a file, one IOC per line.

    Args:
        ioc_file_path (str): Path to the IOC file.

    Returns:
        list: A list of IOCs.  Returns an empty list if the file doesn't exist or is empty.
    """
    # None, not an empty list, for a file that could not be read: an empty
    # list is also the right answer for a file that exists but holds no
    # IOCs, and main has to tell a typo in the path from that case.
    if not os.path.exists(ioc_file_path):
        logging.error(f"IOC file not found: {ioc_file_path}")
        return None

    try:
        with open(ioc_file_path, 'r') as f:
            iocs = [line.strip() for line in f if line.strip()] # Remove empty lines
        return iocs
    except Exception as e:
        logging.error(f"Error reading IOC file: {e}")
        return None


def _context_around(text, needle, case_insensitive=False):
    # The stored context used to be the first 500 characters of the page,
    # wherever the match happened to be, which told a reader nothing about
    # the match itself on any page longer than a paragraph.
    haystack = text.lower() if case_insensitive else text
    probe = needle.lower() if case_insensitive else needle
    index = haystack.find(probe)
    if index == -1:
        return text[:500]
    start = max(0, index - 100)
    end = index + len(needle) + 200
    return text[start:end]

def scrape_url(url, keywords, iocs, max_pages=1):
    """
    Scrapes a URL for keywords and IOCs.

    Args:
        url (str): The URL to scrape.
        keywords (list): A list of keywords to search for.
        iocs (list): A list of IOCs to search for.
        max_pages (int):  Maximum number of pages to scrape (for paginated sites)

    Returns:
        tuple: A pair (results, failed_fetches), where results is a list
        of dictionaries representing matches, and failed_fetches is the
        number of page fetches that failed for this URL.
    """
    results = []
    failed_fetches = 0
    try:
        for page_num in range(1, max_pages + 1):
            current_url = url
            if page_num > 1:
                # Attempt to handle pagination (very basic, might need customization per site)
                if "?" in url:
                    current_url = f"{url}&page={page_num}"
                else:
                    current_url = f"{url}?page={page_num}"

            logging.info(f"Scraping URL: {current_url}")
            try:
                response = requests.get(current_url, timeout=10)  # No timeout would let one slow site stall the whole run
                response.raise_for_status()  # Raise HTTPError for bad responses (4xx or 5xx)
            except requests.exceptions.RequestException as e:
                logging.error(f"Error fetching URL {current_url}: {e}")
                failed_fetches += 1
                continue # Skip to the next page of this URL if an error occurred

            soup = BeautifulSoup(response.content, 'html.parser')
            text_content = soup.get_text()

            if keywords:
                for keyword in keywords:
                    lowered = keyword.lower() # Case-insensitive search
                    if lowered in text_content.lower():
                        results.append({
                            'url': current_url,
                            'keyword': lowered,
                            'ioc': None,
                            'context': _context_around(text_content, keyword, case_insensitive=True)
                        })

            if iocs:
                for ioc in iocs:
                    if ioc in text_content:
                        results.append({
                            'url': current_url,
                            'keyword': None,
                            'ioc': ioc,
                            'context': _context_around(text_content, ioc)
                        })
    except Exception as e:
        logging.error(f"General scraping error for URL {url}: {e}")
        failed_fetches += 1

    return results, failed_fetches

def save_results_to_csv(results, output_file):
    """
    Saves the scraping results to a CSV file.

    Args:
        results (list): A list of dictionaries representing the scraping results.
        output_file (str): The path to the output CSV file.

    Returns:
        bool: True when the CSV was written, False when it could not be.
    """
    try:
        df = pd.DataFrame(results)
        df.to_csv(output_file, index=False)
        logging.info(f"Results saved to: {output_file}")
        return True
    except Exception as e:
        logging.error(f"Error saving results to CSV: {e}")
        return False


def main():
    """
    Main function of the script.
    """
    parser = setup_argparse()
    args = parser.parse_args()

    if args.max_pages < 1:
        logging.error("max_pages must be at least 1.")
        sys.exit(1)

    keywords = args.keywords if args.keywords else []
    iocs = []
    if args.ioc_file:
        iocs = read_iocs_from_file(args.ioc_file)
        if iocs is None:
            sys.exit(1)

    all_results = []
    total_fetches = 0
    failed_fetches = 0
    for url in args.urls:
        results, failed = scrape_url(url, keywords, iocs, args.max_pages)
        all_results.extend(results)
        total_fetches += args.max_pages
        failed_fetches += failed

    if not save_results_to_csv(all_results, args.output):
        sys.exit(1)

    if total_fetches and failed_fetches == total_fetches:
        logging.error(f"All {total_fetches} page fetch(es) failed: no named URL could be read.")
        sys.exit(1)
    if failed_fetches:
        logging.warning(f"Partial failure: {failed_fetches} of {total_fetches} page fetch(es) could not be fetched.")


if __name__ == "__main__":
    main()
