# from chatbot import Chat, register_call
# import requests
# import json

# @register_call("GetAccountDetails")
# def get_account_details(session, query):
#     try:
#         response = requests.get(
#             "https://api.finkraft.com/account/details",
#             params={"account_id": query}
#         )
#         data = response.json()
#         return f"Account Name: {data['account_name']}, Balance: {data['balance']}"
#     except Exception as e:
#         return f"Error fetching account details: {str(e)}"

# first_question = "Hi, how can I help you?"
# Chat("examples/Example.template").converse(first_question)

import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin
import time
import re

def scrape_website(url):
    response = requests.get(url)
    if response.status_code == 200:
        soup = BeautifulSoup(response.content, 'lxml')
        return soup
    else:
        print(f"Failed to retrieve {url}")
        return None

def extract_text(soup):
    text = soup.get_text()
    # Remove excessive whitespace
    text = re.sub(r'\s+', ' ', text)
    text = text.strip()
    # Re-add newlines for readability at appropriate places
    formatted_text = re.sub(r'(?<=[.!?]) +', '\n\n', text)
    return formatted_text

def extract_anchor_urls(soup, base_url):
    anchor_tags = soup.find_all('a', href=True)
    urls = [urljoin(base_url, tag['href']) for tag in anchor_tags]
    return urls

def save_to_txt(data, filename):
    with open(filename, 'w', encoding='utf-8') as file:
        file.write(data)

def main():
    base_urls = [
        "https://finkraft.ai/",
        "https://in.linkedin.com/company/finkraft-ai"
    ]

    all_scraped_data = ""

    for base_url in base_urls:
        # Scrape the base URL
        soup = scrape_website(base_url)
        if soup:
            all_scraped_data += f"Data from {base_url}:\n\n"
            all_scraped_data += extract_text(soup) + "\n\n"

            # Extract and scrape all anchor URLs
            anchor_urls = extract_anchor_urls(soup, base_url)
            for anchor_url in anchor_urls:
                print(f"Scraping {anchor_url}")
                anchor_soup = scrape_website(anchor_url)
                if anchor_soup:
                    all_scraped_data += f"Data from {anchor_url}:\n\n"
                    all_scraped_data += extract_text(anchor_soup) + "\n\n"
                # Pause to avoid overwhelming the server
                time.sleep(1)

    # Save all scraped data to a txt file
    save_to_txt(all_scraped_data, "all_website_data.txt")
    print("Scraping completed.")

if __name__ == "__main__":
    main()
