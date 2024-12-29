from concurrent.futures import ThreadPoolExecutor, as_completed
from selenium import webdriver
from selenium.common import TimeoutException
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from datetime import datetime
from Models import Company, CompanyData
from Data.db_functions import add_company_object, insert_company_data_object, update_last_update_by_code


def set_driver_options():
    # Set up Chrome options for headless mode
    options = Options()
    options.headless = True
    options.add_argument("--headless")
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-gpu")
    options.add_argument("--disable-dev-shm-usage")
    options.add_argument("disable-infobars")  # Disable infobars
    options.add_argument("--disable-extensions")  # Disable extensions
    options.add_argument("--disable-popup-blocking")
    options.add_argument("--log-level=3")
    return options

def get_current_date():
    return datetime.now().strftime("%d.%m.%y")

#NOT ASYNC

class SeleniumWorker:
    def __init__(self, driver_pool):
        self.web_objects = []
        self.options = set_driver_options()
        self.data = []
        self.driver_pool = driver_pool

    def create_driver_and_set_url(self, key):
        # Initialize WebDriver each time to ensure a fresh instance
        new_driver = self.driver_pool.get_driver()
        url = f"https://www.mse.mk/mk/stats/symbolhistory/{key}"
        new_driver.get(url)
        return new_driver

    def create_issuer_driver_and_set_url(self):
        new_driver = self.driver_pool.get_driver()
        url = f"https://www.mse.mk/mk/issuers/free-market"
        new_driver.get(url)
        return new_driver

    def fetch_company_keys(self):
        driver = self.create_issuer_driver_and_set_url()
        today = get_current_date()
        first_column_data = driver.execute_script("""
            let rows = document.querySelectorAll('table tr');  // Select all table rows
            return Array.from(rows).map(row => {
                let firstCell = row.querySelector('td');  // Get the first <td> in the row
                return firstCell ? firstCell.textContent.trim() : null;  // Return text if exists
            }).filter(cell => cell !== null);  // Remove null entries
        """)
        print("Filled company keys to database.")
        self.driver_pool.release_driver(driver)
        return first_column_data

    def fetch_data_since_last_date(self, last_date, key):
        return self.fetch_data_with_dates_and_key(last_date, get_current_date(), key)

    def fetch_data_for_company(self, company):
        year = datetime.now().year

        def process_item(index):
            return self.fetch_data_with_dates_and_key(f"01.01.{year - 10 + index}", f"31.12.{year - 10 + index}", company.code)

        def process_this_year():
            return self.fetch_data_since_last_date(company.last_update, company.code)

        with ThreadPoolExecutor(max_workers=10) as executor:
            # Submit tasks to the executor and collect futures

            futures = None

            if company.last_update == "None":
                futures = {executor.submit(process_item, index): index for index in range(10)}

            executor.submit(process_this_year)

            if futures is None: return

            for future in as_completed(futures):
                try:
                    future.result()
                    print("Data loaded for " + company.code + "!")
                except Exception as e:
                    print(f"Task raised an exception: {e}")
                finally:
                    executor.shutdown(wait=True)

            update_last_update_by_code(company.code, get_current_date())


    def fetch_data_for_10_years_with_key(self, key):
        year = datetime.now().year
        data = []

        def process_item(index):
            return self.fetch_data_with_dates_and_key(f"01.01.{year - 10 + index}", f"31.12.{year - 10 + index}", key)

        with ThreadPoolExecutor(max_workers=10) as executor:
            # Submit tasks to the executor and collect futures
            futures = {executor.submit(process_item, index): index for index in range(10)}

            for future in as_completed(futures):
                try:
                    future.result()
                    print("Data loaded for " + key + "!")
                    executor.shutdown()
                except Exception as e:
                    print(f"Task raised an exception: {e}")
        return data

    def convert_str_to_float(self, string):
        return 0 if string is None else float(string.replace(".", "").replace(",", ".") if string != '' else 0)

    def fetch_data_with_dates_and_key(self, start_date, end_date, key):
        driver = self.create_driver_and_set_url(key)
        try:
            #driver.delete_all_cookies()  # Clear cookies after setting the URL

            # Wait until input elements are interactable
            WebDriverWait(driver, 2).until(
                EC.element_to_be_clickable((By.NAME, "FromDate"))
            )
            WebDriverWait(driver, 2).until(
                EC.element_to_be_clickable((By.NAME, "ToDate"))
            )

            # Set the start and end dates
            input_element1 = driver.find_element(By.NAME, "FromDate")
            input_element1.clear()
            input_element1.send_keys(start_date)

            input_element2 = driver.find_element(By.NAME, "ToDate")
            input_element2.clear()
            input_element2.send_keys(end_date)

            # Locate and trigger the button click
            button = WebDriverWait(driver, 2).until(
                EC.element_to_be_clickable((By.CLASS_NAME, "btn-primary-sm"))
            )
            driver.execute_script("arguments[0].click();", button)

            table_data = driver.execute_script("""
                let cells = document.querySelectorAll('td');
                return Array.from(cells).map(cell => cell.textContent.trim());
            """)

            if table_data is None: return

            for i in range(0, len(table_data), 9):
                company = CompanyData(key, table_data[i],
                                      self.convert_str_to_float(table_data[i + 1]),
                                      self.convert_str_to_float(table_data[i + 2]),
                                      self.convert_str_to_float(table_data[i + 3]),
                                      self.convert_str_to_float(table_data[i + 4]),
                                      self.convert_str_to_float(table_data[i + 5]),
                                      self.convert_str_to_float(table_data[i + 6]),
                                      self.convert_str_to_float(table_data[i + 7]),
                                      self.convert_str_to_float(table_data[i + 8]))
                insert_company_data_object(company)
        except TimeoutException as e:
            return
        finally:
            self.driver_pool.release_driver(driver)