import os

from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager

from fixture.realitka import RealitkaHelper
from fixture.step import StepHelper

class Application:

    def __init__(self):
        chrome_options = webdriver.ChromeOptions()
        chrome_options.binary_location = os.environ.get("GOOGLE_CHROME_BIN")
        # chrome_options.add_argument("--incognito")
        # chrome_options.add_argument("--headless")
        # chrome_options.add_extension("/Users/oleksandr.korsun/Desktop/ext_dir/1.zip")
        chrome_options.add_argument("--disable-dev-shm-usage")
        chrome_options.add_argument("--no-sandbox")
        chrome_options.add_argument("--disable-notifications")
        chrome_options.add_argument("user-agent='User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/81.0.4044.113 Safari/537.36'")
        self.wd = webdriver.Chrome(ChromeDriverManager().install(), chrome_options=chrome_options)
        self.wd.get_window_size('1920,1080')

        self.step = StepHelper(self)
        self.realitka = RealitkaHelper(self)

    def destroy(self):
        self.wd.quit()