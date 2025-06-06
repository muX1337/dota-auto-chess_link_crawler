import requests
from bs4 import BeautifulSoup
import urllib.parse
import csv

# Base URL for the Steam changelog pages
BASE_URL = "https://steamcommunity.com/sharedfiles/filedetails/changelog/1613886175?p="

# Function to extract and decode Google Docs links with titles
def extract_google_docs_links():
    google_docs_data = []  # Store (title, link) pairs

    for page in range(1, 92):  # Loop through pages 1 to 91
        url = f"{BASE_URL}{page}"
        response = requests.get(url)

        if response.status_code != 200:
            print(f"⚠️ Failed to fetch page {page}")
            continue

        soup = BeautifulSoup(response.text, "html.parser")

        # Find all <a> tags with the class "bb_link"
        for link in soup.find_all("a", class_="bb_link"):
            href = link.get("href", "")
            title = link.text.strip()  # Extract the title (e.g., "Rebalance Patch")

            # Ensure it's a Steam redirector link
            if "steamcommunity.com/linkfilter/?" in href:
                # Extract the actual Google Docs URL
                decoded_url = urllib.parse.unquote(href.split("u=")[-1])

                if "docs.google.com" in decoded_url:
                    google_docs_data.append((title, decoded_url))
                    print(f"✅ Found: {title} -> {decoded_url}")

    return google_docs_data

# Run the crawler
google_links_with_titles = extract_google_docs_links()

# Save results to both .txt and .csv files
with open("google_docs_links.txt", "w", encoding="utf-8") as txt_file, \
     open("google_docs_links.csv", "w", newline='', encoding="utf-8") as csv_file:

    # Write plain text version
    for title, link in google_links_with_titles:
        txt_file.write(f"{title}: {link}\n")
        
    # Write CSV version
    writer = csv.writer(csv_file)
    writer.writerow(["Title", "Link"])  # Header row
    writer.writerows(google_links_with_titles)

print("\n✅ Export complete! Files saved as 'google_docs_links.txt' and 'google_docs_links.csv'")
