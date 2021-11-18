from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException, TimeoutException
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions
from selenium.webdriver.support.wait import WebDriverWait

from utility.common.env import Env
from webdriver_manager.chrome import ChromeDriverManager
import threading

driver = None
lock = threading.Lock()


class Chrome(object):
    @staticmethod
    def driver():
        global driver
        lock.acquire()
        if not driver:
            chrome_options = webdriver.ChromeOptions()
            chrome_options.add_argument('--incognito')
            driver = webdriver.Chrome(
                chrome_options=chrome_options, executable_path=ChromeDriverManager().install())
            driver.set_page_load_timeout(Env.page_load_timeout())
        lock.release()
        return driver

    @staticmethod
    def is_opened():
        global driver
        return driver is not None

    @staticmethod
    def quit():
        global driver
        lock.acquire()
        if driver:
            driver.quit()
            driver = None
        lock.release()

    @staticmethod
    def has_element_by_xpath(xpath):
        # 當下判斷元件是否存在
        try:
            Chrome.driver().find_element_by_xpath(xpath)
            return True

        except NoSuchElementException:
            return False

    @staticmethod
    def has_element_loaded_by_xpath(xpath, seconds=Env.element_load_timeout()):
        # 至多 N 秒內判斷元件是否存在
        try:
            Chrome.wait_element_loaded_by_xpath(xpath, seconds)
            return True

        except NoSuchElementException:
            return False

    @staticmethod
    def wait_element_loaded_by_xpath(xpath, seconds=Env.element_load_timeout()):
        try:
            return WebDriverWait(Chrome.driver(), seconds).until(
                expected_conditions.presence_of_element_located(
                    (By.XPATH, xpath))
            )

        except TimeoutException:
            raise NoSuchElementException(xpath)

    @staticmethod
    def wait_element_visible_by_xpath(xpath, seconds=Env.element_load_timeout()):
        try:
            return WebDriverWait(Chrome.driver(), seconds).until(
                expected_conditions.visibility_of_element_located(
                    (By.XPATH, xpath))
            )

        except TimeoutException:
            raise NoSuchElementException(xpath)

    @staticmethod
    def wait_element_contains_text_by_xpath(xpath, text, seconds=Env.element_load_timeout()):
        try:
            return WebDriverWait(Chrome.driver(), seconds).until(
                expected_conditions.text_to_be_present_in_element(
                    (By.XPATH, xpath), text)
            )

        except TimeoutException:
            raise NoSuchElementException(xpath)

    @staticmethod
    def wait_element_clickable_by_xpath(xpath, seconds=Env.element_load_timeout()):
        try:
            return WebDriverWait(Chrome.driver(), seconds).until(
                expected_conditions.element_to_be_clickable((By.XPATH, xpath))
            )

        except TimeoutException:
            raise NoSuchElementException(xpath)

    @staticmethod
    def element_send_keys_by_xpath(xpath, keys=None, seconds=Env.element_load_timeout()):
        Chrome.wait_element_clickable_by_xpath(xpath, seconds).click()
        Chrome.wait_element_clickable_by_xpath(
            xpath, seconds).send_keys(str(keys))
