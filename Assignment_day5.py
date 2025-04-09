import requests
from bs4 import BeautifulSoup
import concurrent.futures
import os
import time

TARGET_URL = "https://www.example.com" 
OUTPUT_DIR = "threaded_downloads"
os.makedirs(OUTPUT_DIR, exist_ok=True)

def download_url(url):
    """Downloads the content of a URL."""
    try:
        response = requests.get(url, timeout=5)
        response.raise_for_status()
        return response.text, url
    except requests.exceptions.RequestException as e:
        print(f"Error downloading {url}: {e}")
        return None, url

def parse_links(html_content, base_url):
    """Parses HTML content and extracts all 'href' links."""
    soup = BeautifulSoup(html_content, 'html.parser')
    links = set()
    for a_tag in soup.find_all('a', href=True):
        link = a_tag['href']
        if link.startswith(('http://', 'https://')):
            links.add(link)
        elif link.startswith('/'):
            links.add(f"{base_url.rstrip('/')}{link}")
    return list(links)

def save_content(content, filename):
    """Saves the downloaded content to a file."""
    if content:
        filepath = os.path.join(OUTPUT_DIR, filename)
        with open(filepath, "w", encoding="utf-8") as f:
            f.write(content)
        print(f"Threaded: Downloaded and saved: {filename}")

def download_threaded_links(urls):
    """Downloads a list of URLs using threads."""
    results = []
    with concurrent.futures.ThreadPoolExecutor(max_workers=5) as executor:
        future_to_url = {executor.submit(download_url, url): url for url in urls}
        for future in concurrent.futures.as_completed(future_to_url):
            content, downloaded_url = future.result()
            if content:
                filename = downloaded_url.replace("://", "_").replace("/", "_") + "_threaded.html"
                save_content(content, filename)
            elif downloaded_url:
                print(f"Threaded: Failed to download {downloaded_url}")

if __name__ == "__main__":
    start_time = time.time()
    print(f"Threaded: Downloading and parsing links from: {TARGET_URL}")
    initial_html, base_url = download_url(TARGET_URL)

    if initial_html:
        links_to_download = parse_links(initial_html, base_url if base_url else TARGET_URL)
        print(f"Threaded: Found {len(links_to_download)} links to download.")

        thread_start_time = time.time()
        download_threaded_links(links_to_download)
        print(f"Threaded: Download of links finished in {time.time() - thread_start_time:.2f} seconds.")
    else:
        print(f"Threaded: Could not download the initial URL: {TARGET_URL}")

    print(f"Threaded: Total execution time: {time.time() - start_time:.2f} seconds.")
    print(f"Threaded: Downloaded pages saved in: {OUTPUT_DIR}")