import os
from concurrent.futures import ThreadPoolExecutor, as_completed
from Scraper import SeleniumWorker
from Scraper import WebDriverPool
from Scraper.selenium_scraper import set_driver_options



pool_size = min(32, os.cpu_count() + 4)
webdriver_pool = WebDriverPool(pool_size, set_driver_options())

data = []
key_worker = SeleniumWorker(webdriver_pool)
keys = key_worker.fetch_company_keys()

while keys is None: continue

with ThreadPoolExecutor() as main_executor:
    worker = SeleniumWorker(webdriver_pool)
    main_futures = [main_executor.submit(worker.fetch_data_for_10_years_with_key(key)) for key in keys]
    for future in as_completed(main_futures):
        future.result()  # Wait for main tasks to complete
webdriver_pool.close_all()

