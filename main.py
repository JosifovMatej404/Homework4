from Data.db_functions import delete_data_for_unfinished_companies
from PipeFilterSystem import PipeFilterSystem, CompanyFilter, CodeFilter
import signal
import sys
import atexit


def cleanup_and_exit(signum = None, frame = None):
    """
    Cleanup logic when the application is stopping.
    """
    print("Cleaning up before exiting...")
    delete_data_for_unfinished_companies()  # Call the cleanup function

atexit.register(cleanup_and_exit)

# Register the signal handlers
signal.signal(signal.SIGINT, cleanup_and_exit)  # Handle Ctrl+C
signal.signal(signal.SIGTERM, cleanup_and_exit)  # Handle termination signal




code_filter = CodeFilter()
company_filter = CompanyFilter(code_filter)
pipe_filter = PipeFilterSystem([code_filter, company_filter])

pipe_filter.filter_data()



#pool_size = min(32, os.cpu_count() + 4)
#webdriver_pool = WebDriverPool(pool_size, set_driver_options())
#
#data = []
#key_worker = SeleniumWorker(webdriver_pool)
#keys = key_worker.fetch_company_keys()
#
#while keys is None: continue
#
#with ThreadPoolExecutor() as main_executor:
#    worker = SeleniumWorker(webdriver_pool)
#    main_futures = [main_executor.submit(worker.fetch_data_for_10_years_with_key(key)) for key in keys]
#    for future in as_completed(main_futures):
#        future.result()  # Wait for main tasks to complete
#webdriver_pool.close_all()
