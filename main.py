import argparse
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.chrome.options import Options
from bs4 import BeautifulSoup
import time
import csv
from webdriver_manager.chrome import ChromeDriverManager

# List to store reviews
reviews = []

def scrape_reviews_to_csv(url, output_file):
    print(f"Started scraping reviews for {url}")
    chrome_options = Options()
    chrome_options.add_argument("--headless")
    driver = webdriver.Chrome(options=chrome_options, service=Service(ChromeDriverManager().install()))
    try:
        driver.get(url)
        driver.maximize_window()
        time.sleep(1)

        # Accept all cookies
        try:
            AcceptAll = driver.find_element("xpath", '//button[@aria-label="Accept all"]')
            AcceptAll.click()
            time.sleep(1)
        except Exception as e:
            print("No 'Accept all' button found or could not click it:", e)

        # Navigate to the Reviews section
        reviews_button = driver.find_element("xpath", "//button[@role='tab' and contains(@aria-label, 'Reviews') and @data-tab-index='1']")
        reviews_button.click()
        time.sleep(1)

        # Scroll down and adjust zoom
        element = driver.find_element(By.XPATH, "//*[@id='QA0Szd']/div/div/div[1]/div[2]/div/div[1]/div/div/div[2]")
        actions = ActionChains(driver)
        actions.move_to_element(element).perform()
        element.send_keys(Keys.PAGE_DOWN)
        driver.execute_script("document.body.style.zoom = '20%'")

        # Get total reviews count
        Total_reviews_soup = BeautifulSoup(driver.page_source, 'html.parser')
        Total_reviews_tag = Total_reviews_soup.find(class_="jANrlb")
        Total_star = Total_reviews_tag.find(class_="fontDisplayLarge").text
        Total_reviews = Total_reviews_tag.find(class_="fontBodySmall").text.split(" ")[0]

        # Scrape reviews
        htmlTags = set()
        unchanged_iterations = 0

        while int(len(htmlTags)) < int(Total_reviews):
            previous_length = len(htmlTags)
            for i in range(3):
                element.send_keys(Keys.PAGE_DOWN)
            time.sleep(1)
            page_source = driver.page_source
            soup = BeautifulSoup(page_source, 'html.parser')
            main = soup.find_all(class_="jJc9Ad")
            for i in main:
                htmlTags.add(i)
            if len(htmlTags) == previous_length:
                unchanged_iterations += 1
            else:
                unchanged_iterations = 0

            if unchanged_iterations > 5:
                print("Breaking loop: No new reviews found in the last 5 iterations.")
                break

        list_of_tags = list(htmlTags)

        for tag in list_of_tags:
            line = []
            Name = tag.find(class_="d4r55")
            Reviewer = Name.text if Name is not None else ""
            
            reviewTime = tag.find(class_="rsqaWe")
            Review_time = reviewTime.text if reviewTime is not None else ""
            
            Snippet = tag.find(class_="wiI7pd")
            snippet = Snippet.text if Snippet is not None else ""
            
            RatingTag = tag.find(class_="kvMYJc")
            Rating = RatingTag['aria-label'].split()[0] if RatingTag is not None else ""

            reviews.append([Total_star, Total_reviews, Reviewer, Review_time, Rating, snippet])

        # Save reviews to CSV
        print(f"{len(htmlTags)} of {Total_reviews} reviews scraped successfully.")
    finally:
        driver.quit()

    headers = ['Avg Rating', 'Total Reviews', 'Name', 'Time', 'Rating', 'Text']

    with open(output_file, 'w', newline='', encoding='utf-8') as csv_file:
        csv_writer = csv.writer(csv_file)
        csv_writer.writerow(headers)
        for row in reviews:
            csv_writer.writerow(row)

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Google Map Reviews Extractor')
    parser.add_argument('--place', type=str, required=True, help='URL of the place on Google Maps')
    parser.add_argument('--output', type=str, default='review_data.csv', help='Output CSV file name')
    args = parser.parse_args()

    scrape_reviews_to_csv(args.place, args.output)
