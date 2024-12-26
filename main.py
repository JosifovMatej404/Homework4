from concurrent.futures import ThreadPoolExecutor, as_completed

from Scraper import SeleniumWorker

data = []
key_worker = SeleniumWorker()
keys = key_worker.fetch_company_keys()
while keys is None: continue
with ThreadPoolExecutor() as executor:
    # Submit tasks to the executor and collect futures
    worker = SeleniumWorker()
    futures = {executor.submit(worker.fetch_data_for_10_years_with_key(key)): key for key in keys}
    for future in as_completed(futures):
        try:
            result = future.result()  # Get the return value from process_item
            data.append(result)
        except Exception as e:
            print(f"Task raised an exception: {e}")

for i in range(len(keys)):
    print(keys[i] + "\n")
    print(data[i])
    print("\n")

