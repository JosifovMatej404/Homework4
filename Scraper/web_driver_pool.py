from selenium import webdriver
import queue

class WebDriverPool:
    def __init__(self, size, driver_options):
        self.size = size
        self.driver_options = driver_options
        self.pool = queue.Queue(maxsize=size)
        self._initialize_pool()

    def _initialize_pool(self):
        for _ in range(self.size):
            driver = webdriver.Chrome(options=self.driver_options)
            self.pool.put(driver)

    def get_driver(self):
        try:
            return self.pool.get()  # Wait for up to 5 seconds for a driver
        except queue.Empty:
            raise Exception("No available driver in the pool. Please wait or increase the pool size.")

    def release_driver(self, driver):
        if driver:
            self.pool.put(driver)

    def close_all(self):
        while not self.pool.empty():
            driver = self.pool.get()
            driver.quit()