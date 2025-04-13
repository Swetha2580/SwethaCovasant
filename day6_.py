import asyncio
import aiohttp
from bs4 import BeautifulSoup
import os
from urllib.parse import urljoin, urlparse

async def download_url(session, url, output_dir):
    """Downloads the content of a URL and saves it to a file."""
    try:
        async with session.get(url) as response:
            if response.status == 200:
                content = await response.text()
                parsed_url = urlparse(url)
                filename = os.path.join(output_dir, os.path.basename(parsed_url.path) or 'index.html')
                if not os.path.exists(output_dir):
                    os.makedirs(output_dir)
                with open(filename, 'w', encoding='utf-8') as f:
                    f.write(content)
                print(f"Downloaded: {url} -> {filename}")
                return content, url
            else:
                print(f"Failed to download {url}, status: {response.status}")
                return None, url
    except aiohttp.ClientError as e:
        print(f"Error downloading {url}: {e}")
        return None, url
    except Exception as e:
        print(f"An unexpected error occurred while downloading {url}: {e}")
        return None, url

async def parse_and_download_links(session, start_url, output_dir):
    """Downloads the content of a URL, parses it for links, and downloads those links."""
    content, base_url = await download_url(session, start_url, output_dir)
    if content:
        soup = BeautifulSoup(content, 'html.parser')
        links = soup.find_all('a', href=True)
        download_tasks = []
        for link in links:
            href = link['href']
            absolute_url = urljoin(base_url, href)
            
            parsed_link = urlparse(absolute_url)
            parsed_start = urlparse(start_url)
            if parsed_link.scheme in ('http', 'https'):
                
                download_tasks.append(download_url(session, absolute_url, os.path.join(output_dir, parsed_start.netloc)))
               
            else:
                print(f"Skipping non-HTTP/HTTPS link: {absolute_url}")

        if download_tasks:
            print(f"\nFound {len(download_tasks)} links on {start_url}. Downloading...")
            await asyncio.gather(*download_tasks)
            print(f"\nFinished downloading links from {start_url}.")
        else:
            print(f"\nNo HTTP/HTTPS links found on {start_url}.")

async def main(start_url, output_base_dir):
    """Main function to initiate the download and parsing process."""
    async with aiohttp.ClientSession() as session:
        parsed_start_url = urlparse(start_url)
        output_dir = os.path.join(output_base_dir, parsed_start_url.netloc or 'downloaded_site')
        await parse_and_download_links(session, start_url, output_dir)

if __name__ == "__main__":
    target_url = input("Enter the URL to start with: ")
    output_directory = "downloaded_pages"

    asyncio.run(main(target_url, output_directory))
    print(f"\nProcess completed. Downloaded content and links are in the '{output_directory}' directory.")