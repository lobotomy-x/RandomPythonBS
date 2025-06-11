from playwright.sync_api import sync_playwright
from bs4 import BeautifulSoup
from lxml import etree
from json import dump, load


def fetch_forum_content(url):
    with sync_playwright() as p:
        browser = p.chromium.launch()  # Or p.firefox.launch() or p.webkit.launch()
        page = browser.new_page()

        try:
            print(f"Navigating to {url}...")
            page.goto(url, wait_until="networkidle")  # Wait until network is idle

            print("Page loaded. Attempting to get content...")
            # You can now access the fully rendered HTML
            content = page.content()

            print("Content fetched successfully.")
            return content

        except Exception as e:
            print(f"An error occurred: {e}")
            return None

        finally:
            browser.close()


# The URL of the forum topic you want to fetch
forum_url = "https://cs.rin.ru/forum/viewtopic.php?t=100672"

html_content = fetch_forum_content(forum_url)

if html_content:
    print("--- Fetched HTML Content (partial) ---")
    # Print a portion of the content to verify
    print(html_content[:1000])
    print("--- End of partial content ---")

    # Now you can use a library like BeautifulSoup to parse the 'html_content'
    # and extract the specific information you need from the rendered page.
    # Example (install beautifulsoup4: pip install beautifulsoup4):
    # from bs4 import BeautifulSoup
    # soup = BeautifulSoup(html_content, 'html.parser')
    # Find the elements containing the forum posts (you'll need to inspect the page's structure)
    # post_elements = soup.select('.postbody') # Replace '.postbody' with the actual selector
    # for post in post_elements:
    #     print(post.get_text())

else:
    print("Failed to fetch content.")

soup = BeautifulSoup(html_content, "html.parser")
post_elements = soup.select(".postbody")
from pprint import pprint

keys = {}
for post in post_elements:
    list_items = post.find_all("li")
    for i in range(len(list_items) - 1):
        current_item = list_items[i]
        next_item = current_item.next_sibling
        if next_item and next_item.name == "li":
            line = current_item.get_text()
            for word in (words := line.split()):
                if word.startswith("0x") and len(word) == 66:
                    aes = word
                    game = line.split("0x")[0].replace("\u00a0", "")
                    keys[str(game)] = aes
with open("aes.json", "w") as f:
    dump(keys, f)
pprint(keys)
