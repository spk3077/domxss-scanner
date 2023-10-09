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
import re

from vulnerability import Vulnerability
from payloads import PAYLOADS

from seleniumwire import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException, UnexpectedAlertPresentException, NoAlertPresentException


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
    # Breaks when certain alerts are triggered. Cannot accept or dismiss certain alerts: aa'><img src=/ onerror=alert(1)> <!--
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
        WebDriverWait(driver, 3).until(EC.alert_is_present())
        driver.switch_to.alert.dismiss()
        driver.switch_to.default_content()
        return True
    
    # For Selenium Bug with Persistent Alert
    except UnexpectedAlertPresentException:
        pass
        
    except TimeoutException:
        return False
    
    try:
        driver.switch_to.alert.accept()
        return True
    
    except NoAlertPresentException:
        return False


def form_input_scan(driver, url: str) -> set:
    """
    form_input_scan scans the specified URL using the specified driver for INPUT/FORM DOM XSS

    :param driver: browser object
    :param url: Target URL to assess
    :return: set of scan results
    """
    results: set = set()
    # Detect inputs and manipulate them if detected
    ## Inputs inside form
    for payload in PAYLOADS:
        for form in driver.find_elements(By.TAG_NAME, "form"):
            # FUTURE WORK: SUPPORT MORE INPUT TYPES, FORM-RELATED TAGS
            for input in form.find_elements(By.TAG_NAME, "input"):
                if input.get_attribute("type") != "submit":
                    input.send_keys(payload)
    
            form.submit()
            if has_alert(driver):
                results.add(Vulnerability("FORM", driver.current_url, payload, form))

            # If we get redirected return to original site
            driver.get(url)

    ## Inputs outside form
    for payload in PAYLOADS:
        for input_element in driver.find_elements(By.TAG_NAME, "input"):
            input_element.send_keys(payload)
            
            if has_alert(driver):
                results.add(Vulnerability("INPUT", driver.current_url, payload, input_element))

        # If we get redirected return to original site
        driver.get(url)
    
    return results


def query_scan(driver, url: str) -> set:
    """
    query_scan scans the specified URL using the specified driver for INPUT/FORM DOM XSS

    :param driver: browser object
    :param url: Target URL to assess
    :return: set of scan results
    """
    results: set = set()
    ## URL Parameter
    #### window.location.search | location.search
    exploit_url: str = ""
    for payload in PAYLOADS:
        if url.find("?") != -1: # ?
            walked_url: str = url
            while True:
                equal_index: int = walked_url.find("=")
                ampersand_index: int = walked_url.find("&")
                fragment_index: int = walked_url.find("#")
                if ampersand_index != -1:
                    exploit_url = url[:equal_index + 1] + payload + url[ampersand_index:]
                    walked_url = walked_url[ampersand_index + 1:]
                elif fragment_index != -1:
                    exploit_url = url[:equal_index + 1] + payload + url[fragment_index:]
                    break
                else:
                    exploit_url = url[:equal_index + 1] + payload
                    break

                driver.get(exploit_url)
                if has_alert():
                    results.add(Vulnerability("QUERY", exploit_url, payload))

        elif url.find("#") != -1: #
            exploit_url = url[:url.find("#")] + "?exploit=" + payload + url[url.find("#"):]
            driver.get(exploit_url)
            if has_alert():
                results.add(Vulnerability("QUERY", exploit_url, payload))

        else: # Neither ? or #
            exploit_url = url + "?exploit=" + payload
            driver.get(exploit_url)
            if has_alert(driver):
                results.add(Vulnerability("QUERY", exploit_url, payload))

    return results


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
        
    # Assess Manual Possibel Sources of DOM XSS
    results.add(form_input_scan(driver, url))

    # Assess Non-Manual Possible Sources of DOM XSS
    results.add(query_scan(driver, url))

    ## Cookie
    ### Replace existing cookie values
    driver.get(url)
    for payload in PAYLOADS:
        cookies_dict: dict = dict()
        for cookie in driver.get_cookies():
            cookies_dict['name'] = cookie['name']
            cookies_dict['value'] = payload
        
        driver.add_cookie(cookies_dict)
        driver.get(url)

        if has_alert(driver):
                results.add(Vulnerability("COOKIE", url, payload))

    ### Add new cookie value
    
    
    # webdriver.Chrome().add_cookie(cookies_dict)
    # driver.add_cookie({'name' : 'foo', 'value' : 'bar', 'path' : '/', 'secure' : True})



    # ll_cookies=self.driver.get_cookies();
    # cookies_dict = {}
    # for cookie in all_cookies:
    #     cookies_dict[cookie['name']] = cookie['value']
    # print(cookies_dict)

    # execute_script
    return results


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
