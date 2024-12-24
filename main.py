from Scraper import SeleniumWorker

worker = SeleniumWorker()
worker.fetch_data_with_dates_and_key("01.01.2023", "31.12.2023", "alkb")
print(obj.text + "\n" for obj in worker.web_objects)