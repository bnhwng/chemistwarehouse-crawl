from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.firefox.service import Service
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.common.action_chains import ActionChains
import time
import random
import csv

# Set up Firefox WebDriver
service = Service('/opt/homebrew/bin/geckodriver')  # Update with your path to geckodriver
options = Options()
options.headless = True  # Set to True if you don't want the browser window to be visible

# Start the Firefox WebDriver
driver = webdriver.Firefox(service=service, options=options)

# Open the Chemist Warehouse website
url = 'https://www.chemistwarehouse.com.au/shop-online/587/swisse'
driver.get(url)

# Add a wait to ensure the page loads fully (use WebDriverWait for better reliability)
time.sleep(5)  # Adjust as necessary for loading time

# Example: Locate and extract product details (adjust selectors as needed)
def scrape_products():
    products = driver.find_elements(By.CLASS_NAME, "product")
    data = []

    for product in products:
        try:
            name = product.find_element(By.CLASS_NAME, "product__title").text
            price = product.find_element(By.CLASS_NAME, "product__price-current").text

            data.append({
                "Name": name,
                "Price": price,
            })
        except Exception as e:
            print(f"Error scraping product: {e}")

    return data

def scrape_multiple_pages(pages=3):
    all_data = []
    for page in range(1, pages + 1):
        print(f"Scraping page {page}...")
        all_data.extend(scrape_products())

        # Scroll to the bottom of the page to load more content
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        time.sleep(random.uniform(3, 6))  # Random delay

        # Click next button
        try:
            next_button = driver.find_element(By.CLASS_NAME, "pager__button--next")
            next_button.click()
            time.sleep(random.uniform(3, 5))  # Random delay
        except Exception as e:
            print("No more pages to scrape.")
            break

    return all_data

def save_to_csv(data, filename="chemist_warehouse_products.csv"):
    if not data:
        print("No data to save.")
        return

    keys = data[0].keys()
    with open(filename, "w", newline="", encoding="utf-8") as file:
        writer = csv.DictWriter(file, fieldnames=keys)
        writer.writeheader()
        writer.writerows(data)

# Main execution
try:
    data = scrape_multiple_pages(pages=5)
    save_to_csv(data)
    print("Scraping completed. Data saved to 'chemist_warehouse_products.csv'.")
finally:
    driver.quit()
