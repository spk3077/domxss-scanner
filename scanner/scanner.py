"""
File: scanner.py
Assignment: Mini Project 2
Lanuguage: python3
Author: Sean Kells <spk3077@rit.edu>
Purpose: Scan web page for DOM-XSS vulnerabilities using Selenium
Running: python3 scanner.py <WEBSITE>
Example Run: python3 scanner.py http://www.rit.edu/
"""
import sys
import time

from vulnerability import Vulnerability
from payloads import PAYLOADS

from seleniumwire import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException

def check_input():
    """
    check_input checks for input errors

    :return: Nothing
    """
    if len(sys.argv) != 2:
        print("Requires one URI parameter")
        print("EX: python3 scanner.py https://www.rit.edu/")
        exit(1)
    elif len(sys.argv[1]) < 5 and "http://" != sys.argv[1][0:7] and "https://" != sys.argv[1][0:8]:
        print("Must be a http/https URI input")
        print("EX: python3 scanner.py https://www.rit.edu/")
        exit(1)


def get_drivers() -> set:
    """
    get_drivers return set of drivers properly configured

    :return: Set of Drivers
    """
    drivers: set = set()

    # Chrome
    chrome_options = webdriver.ChromeOptions()
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--disable-dev-shm-usage")
    chrome_options.add_argument('--headless')
    drivers.add(webdriver.Chrome(options = chrome_options))

    # FireFox
    fire_options = webdriver.FirefoxOptions()
    fire_options.binary_location = "./drivers/firefox"
    fire_options.add_argument('--headless')
    drivers.add(webdriver.Firefox(options = fire_options))

    # Edge
    edge_options = webdriver.EdgeOptions()
    edge_options.add_argument('--headless')
    drivers.add(webdriver.Edge(options = edge_options))

    # Safari
    # Safari unfortunately doesn't work well with this version of Selenium

    return drivers

def has_alert(driver) -> bool:
    """
    has_alert detects if an alert is present on the webpage

    :param driver: browser object
    :return: boolean True if alert present, False if alert missing
    """
    try:
        WebDriverWait(driver, 2.5).until(EC.alert_is_present())
        return True
        
    except TimeoutException:
        return False


def scan_page(driver, url: str) -> set:
    """
    scan_page scans the specified URL using the specified driver (browser) for DOM XSS (main func)

    :param driver: browser object
    :param url: Target URL to assess
    :return: set of scan results
    """
    results: set = set()
    driver.get(url)

    # Check if Alert is already present
    if has_alert(driver):
        print("Alert already present on assessed site")
        return
        
    # Detect inputs and manipulate them if detected
    ## Inputs inside form
    found_inputs: set = set()
    for form in driver.find_elements(By.TAG_NAME, "form"):
        # FUTURE WORK: SUPPORT MORE INPUT TYPES, FORM-RELATED TAGS
        for input in form.find_elements(By.TAG_NAME, "input"):
            for payload in PAYLOADS:
                input.send_keys(payload + Keys.RETURN)
                found_inputs.add(input)
        
        form.submit()
        if has_alert():
            results.add(Vulnerability("FORM", form.current_url, form))

        # If we get redirected return to original site
        if form.current_url != url:
            driver.get(url)

    ## Inputs outside form
    input_elements: list = form.find_elements(By.TAG_NAME, "input")
    for input_element in input_elements:
        if input_element not in found_inputs:
            for payload in PAYLOADS:
                input_element.send_keys(payload + Keys.RETURN)
        
                if has_alert():
                    results.add(Vulnerability("INPUT", input_element.current_url, input_element))

                # If we get redirected return to original site
                if input_element.current_url != url:
                    driver.get(url)


    # Scan for Sources and manipulate them if detected


    

    # execute_script


def print_output(results: set):
    """
    print_output takes in the driver name and results to print good looking results to STDOUT

    :param driver_name: name of driver
    :param port: Port of Web Server
    :return: set of scan results
    """
    for result in results:
        print("-------")
        print(result)


def main():
    """
    main is the primary intended Python script to run to execute entire server

    :return: Nothing
    """
    check_input()
    drivers: set = get_drivers()
    start_time = time.time()

    url: str = sys.argv[1]
    for driver in drivers:
        print()
        print("================================")
        print("**" + driver.name.upper() + ":")
        results: set = scan_page(driver, url)
        print_output(results)

        # Closing...
        driver.stop_client()
        driver.close()
        driver.quit()

    end_time = time.time()
    print()
    print("================================")
    print()
    print("Finished successfully at %s!" % (str(end_time - start_time)),)
    

if __name__ == "__main__":
    main()
