from seleniumwire import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException, UnexpectedAlertPresentException, NoAlertPresentException
import time

def interceptor(request):
    """
    interceptor modifies the path of the intercepted HTTP request

    :param request: intercepted HTTP request
    :return: Nothing
    """
    request.create_response(
        status_code=200,
        headers={'Content-Type': 'text/html', 'Host' : 'example.com'},
        body='<html><body><a id="domxssscan" href="' + 'http://localhost/ex2.html' + '">Click</a></body></html>'
    )


chrome_options = webdriver.ChromeOptions()
chrome_options.add_argument("--no-sandbox")
chrome_options.add_argument("--disable-dev-shm-usage")
chrome_options.add_argument('--headless')
driver = webdriver.Chrome(options = chrome_options)

driver.request_interceptor = interceptor
driver.get("https://example.com")
driver.request_interceptor = None

driver.find_element(By.ID, "domxssscan").click()
driver.save_screenshot("referrer_test.png")