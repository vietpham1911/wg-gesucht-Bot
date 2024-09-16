import time
import re
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

# ChromeDriver path and URL
CHROME_DRIVER_PATH = "/usr/bin/chromedriver"
URL = "https://www.wg-gesucht.de/1-zimmer-wohnungen-in-Tuebingen.127.1.1.0.html"

def init_driver():
    """Initialize the Chrome WebDriver with fullscreen mode."""
    chrome_options = Options()
    chrome_options.add_argument("--start-fullscreen")
    service = Service(CHROME_DRIVER_PATH)
    return webdriver.Chrome(service=service, options=chrome_options)

def click_save_button(driver):
    """Click the save button if it exists."""
    try:
        save_button = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.CSS_SELECTOR, "a.cmpboxbtn.cmpboxbtnsave"))
        )
        save_button.click()
        print("Save button clicked.")
    except Exception as e:
        print(f"Save button not found or not clickable: {e}")

def process_listing(driver, listing):
    """Process each listing by clicking the link and sending a message."""
    try:
        detail_link = listing.find_element(By.CSS_SELECTOR, "a[href*='/1-zimmer-wohnungen-in-Tuebingen-']")
        detail_link.click()
        print("Listing clicked.")

        # Wait for the detail page to load
        WebDriverWait(driver, 10).until(EC.presence_of_element_located(
            (By.XPATH, '/html/body/div[3]/div[1]/div[3]/div[2]/div[3]/div[3]/div/a')
        ))

        message_button = driver.find_element(By.XPATH, '/html/body/div[3]/div[1]/div[3]/div[2]/div[3]/div[3]/div/a')
        message_button.click()
        print("Message button clicked.")

        WebDriverWait(driver, 3).until(EC.staleness_of(message_button))  # Wait until button action completes
        driver.back()  # Go back to the main page
        print("Returned to the main page.")

    except Exception as e:
        print(f"Error processing listing: {e}")

def main():
    """Main script to scrape and interact with WG-Gesucht listings."""
    driver = init_driver()

    while True:
        driver.get(URL)
        WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.CSS_SELECTOR, "div.wgg_card")))

        click_save_button(driver)

        listings = driver.find_elements(By.CSS_SELECTOR, "div.wgg_card")
        for listing in listings:
            process_listing(driver, listing)
            break  # Reload the page every 5 minutes after processing one listing

        time.sleep(300)  # Wait for 5 minutes before reloading the page

if __name__ == "__main__":
    main()
