from utility import web_driver


if __name__ == "__main__":
    web_driver.Chrome.driver().get("http://www.google.com")