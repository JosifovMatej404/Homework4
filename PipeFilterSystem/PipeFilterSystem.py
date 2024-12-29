import os
from concurrent.futures import ThreadPoolExecutor, as_completed

from Data.db_functions import get_last_update_for_all_companies, add_company_object, update_last_update_by_code
from Models import Company
from Scraper import SeleniumWorker, WebDriverPool
from Scraper.selenium_scraper import set_driver_options, get_current_date


class PipeFilterSystem:
    def __init__(self, filters):
        self.pipe = Pipe(filters)

    def filter_data(self):
        return self.pipe.start_flow()


class Filter:
    def process_data(self, pool_size, webdriver_pool):
        return []


class CodeFilter(Filter):
    def __init__(self):
        self.keys = None

    def process_data(self, pool_size, webdriver_pool):
        key_worker = SeleniumWorker(webdriver_pool)
        companies = get_last_update_for_all_companies()
        self.keys = key_worker.fetch_company_keys()

        if not companies:
            print("No companies found in database, fetching from web...")
            for key in self.keys:
                company = Company(key, "None")
                add_company_object(company)
        else:
            print(str(len(companies)) + " companies found in database")

        for company in companies:
            if company.last_update == get_current_date():
                if company.code in self.keys: self.keys.remove(company.code)

        print(str(len(self.keys)) + " companies are going to be updated...")
        return self.keys

class CompanyFilter(Filter):
    def __init__(self, code_filter):
        self.code_filter = code_filter

    def process_data(self, pool_size, webdriver_pool):
        while get_last_update_for_all_companies() is None: continue
        with ThreadPoolExecutor() as main_executor:
            worker = SeleniumWorker(webdriver_pool)
            main_futures = [main_executor.submit(worker.fetch_data_for_company(company)) for company in get_last_update_for_all_companies()]
            for future in as_completed(main_futures):

                continue
        webdriver_pool.close_all()
        return ['Data is stored']

class Pipe:
    def __init__(self, filters):
        self.filters = filters
        self.pool_size = min(32, os.cpu_count() + 4)
        self.webdriver_pool = WebDriverPool(self.pool_size, set_driver_options())

    def start_flow(self):
        for _filter in self.filters:
            _filter.process_data(self.pool_size, self.webdriver_pool)