import threading
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By


def set_driver_options():
    # Set up Chrome options for headless mode
    options = Options()
    options.add_argument("--headless")
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-gpu")
    options.add_argument("--disable-dev-shm-usage")
    options.add_argument("disable-infobars")  # Disable infobars
    options.add_argument("--disable-extensions")  # Disable extensions
    return options


class SeleniumWorker:
    def __init__(self):
        self.web_objects = []
        self.driver = None
        self.options = set_driver_options()
        self.data = []

    def set_driver_url(self, key):
        # Initialize WebDriver each time to ensure a fresh instance

        self.driver = webdriver.Chrome(options=self.options)
        url = f"https://www.mse.mk/mk/stats/symbolhistory/{key}"
        self.driver.get(url)

    def fetch_data_with_dates_and_key(self, start_date, end_date, key):
        def task():
            try:
                self.set_driver_url(key)
                self.driver.delete_all_cookies()  # Clear cookies after setting the URL

                print("Waiting for date inputs to load...")

                # Wait until input elements are interactable
                WebDriverWait(self.driver, 20).until(
                    EC.element_to_be_clickable((By.NAME, "FromDate"))
                )
                WebDriverWait(self.driver, 20).until(
                    EC.element_to_be_clickable((By.NAME, "ToDate"))
                )

                # Set the start and end dates
                input_element1 = self.driver.find_element(By.NAME, "FromDate")
                input_element1.clear()
                input_element1.send_keys(start_date)

                input_element2 = self.driver.find_element(By.NAME, "ToDate")
                input_element2.clear()
                input_element2.send_keys(end_date)

                print("Triggering data fetch...")
                # Locate and trigger the button click
                button = WebDriverWait(self.driver, 20).until(
                    EC.element_to_be_clickable((By.CLASS_NAME, "btn-primary-sm"))
                )
                self.driver.execute_script("arguments[0].click();", button)

                print("Waiting for data to load...")
                # Wait for the data table to load
                WebDriverWait(self.driver, 10).until(
                    EC.presence_of_all_elements_located((By.TAG_NAME, "td"))
                )

                # Get page source after data is fully loaded
                local_objects = self.driver.find_elements(By.TAG_NAME, "td")
                self.web_objects.extend(local_objects)
                print("Data loaded successfully!")

            except Exception as e:
                print(f"An error occurred: {e}")
                self.driver.quit()

            finally:
                if self.driver:
                    self.driver.quit()  # Ensure the driver is properly closed

        # Run the task in a separate thread
        thread = threading.Thread(target=task)
        thread.start()
        thread.join()  # Wait for the thread to finish before returning data
