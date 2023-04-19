import time

from selenium.common.exceptions import NoSuchElementException
from selenium.common.exceptions import TimeoutException
from selenium.webdriver import ActionChains
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait


# Class for steps abstract methods.


class StepHelper:

    def __init__(self, app):
        self.app = app
        self.wd = self.app.wd

    def get_how(self, locator):
        if locator.startswith("//"):
            how = By.XPATH
        else:
            how = By.CSS_SELECTOR
        return how

    def specified_element_is_present(self, locator, time=3):
        try:
            WebDriverWait(self.wd, time).until(
                EC.presence_of_element_located((self.get_how(locator), locator)))
        except NoSuchElementException:
            return False
        except TimeoutException:
            return False
        return True

    def click_on_element(self, locator, scrollInToView = False):
        WebDriverWait(self.wd, 10).until(
            EC.visibility_of_element_located((self.get_how(locator), locator)))
        element = WebDriverWait(self.wd, 10).until(
            EC.element_to_be_clickable((self.get_how(locator), locator))
        )
        if scrollInToView:
            self.wd.execute_script("arguments[0].scrollIntoView({ behavior: 'smooth', block: 'nearest', inline: 'start' });", element)
            time.sleep(2)
        ActionChains(self.wd).move_to_element(element).pause(0.5).click().perform()

    def input_text(self, locator, text):
        element = WebDriverWait(self.wd, 10).until(
            EC.visibility_of_element_located((self.get_how(locator), locator)))
        element.click()
        element.clear()
        element.send_keys(text)

    def get_list_of_elements(self, locator):
        by = self.get_how(locator)
        WebDriverWait(self.wd, 10).until(
            EC.presence_of_all_elements_located((self.get_how(locator), locator)))
        return self.wd.find_elements(by=by, value=locator)

    def get_element_text(self, locator, scrollInToView = False):
        element = WebDriverWait(self.wd, 10).until(
            EC.visibility_of_element_located((self.get_how(locator), locator)))
        if scrollInToView:
            self.wd.execute_script("arguments[0].scrollIntoView({ behavior: 'smooth', block: 'nearest', inline: 'start' });", element)
            time.sleep(2)
        return element.text

    def specified_element_is_not_present(self, locator, waitingTime=3):
        time.sleep(1)
        WebDriverWait(self.wd, waitingTime).until(
            EC.invisibility_of_element_located((self.get_how(locator), locator)))

    def wait_for_element(self, locator):
        element = WebDriverWait(self.wd, 10).until(
            EC.visibility_of_element_located((self.get_how(locator), locator)))
        return element

    def jsXpathClick (self, locator):
        time.sleep(2)
        b = self.wd.find_element(By.XPATH, locator)
        self.wd.execute_script("arguments[0].click();", b)