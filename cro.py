from pathlib import Path
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.service import Service
import csv
import time

# Set up the WebDriver path and service
driver_path = Path.home() / "Downloads/chromedriver/chromedriver"
service = Service(executable_path=str(driver_path))
driver = webdriver.Chrome(service=service)

# Define output CSV file path
output_path = Path("company_data.csv")

# Open the target website
driver.get("https://www.clinicaltrialsarena.com/company-a-z/")
time.sleep(2)

# Handle cookies prompt by accepting cookies
try:
    accept_cookies_button = WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable((By.XPATH, "//button[contains(text(), 'Accept')]"))
    )
    accept_cookies_button.click()
    time.sleep(1)
except Exception as e:
    print("Cookies acceptance button not found or already dismissed:", e)

# Open the CSV file in write mode
with output_path.open("w", newline="") as csvfile:
    csv_writer = csv.writer(csvfile)
    csv_writer.writerow(["Company Name", "Website"])  # Header row with only name and website

    try:
        # Find all company links
        companies = driver.find_elements(By.CSS_SELECTOR, "li.company-list-item a")
        print(f"Found {len(companies)} companies on the page.")

        # Loop through a few companies
        for i, company in enumerate(companies[:5]):  # Adjust limit as needed
            company_name = company.text
            company_link = company.get_attribute("href")
            print(f"\nProcessing company {i + 1}: {company_name}")

            # Go to the company's details page
            driver.get(company_link)
            time.sleep(2)

            # Attempt to click on contact details dropdown and get website
            try:
                contact_dropdown = WebDriverWait(driver, 10).until(
                    EC.element_to_be_clickable((By.CSS_SELECTOR, "div.contact-details-toggle"))
                )
                contact_dropdown.click()
                time.sleep(1)

                # Extract website only
                try:
                    website = driver.find_element(By.CSS_SELECTOR, "a.website-link").get_attribute("href")
                    print(f"Website: {website}")
                except Exception as e:
                    website = "Website not available"
                    print(f"Website not available: {e}")

            except Exception as e:
                website = "Contact details dropdown not available"
                print(f"Contact details dropdown not available: {e}")

            # Write the name and website to CSV
            csv_writer.writerow([company_name, website])
            print("Data written to CSV.")

            # Return to main list
            driver.back()
            time.sleep(2)

    finally:
        driver.quit()  # Close the browser
