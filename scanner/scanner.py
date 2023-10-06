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
import re
import time

from seleniumwire import webdriver
from selenium.webdriver.common.by import By

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


def scan_page(driver, url: str) -> dict:
    """
    scan_page scans the specified URL using the specified driver (browser) for DOM XSS (main func)

    :param driver: IP of Web Server
    :param port: Port of Web Server
    :return: dictionary of scan results
    """
    # Detect inputs and manipulate them if detected
    driver.get(url)
    input_elements: list = driver.find_elements(By.TAG_NAME, "input")
    print(input_elements)


    # Scan for Sources and manipulate them if detected

    # webdriver.Chrome().find_elements
    

    # execute_script

def print_output(driver_name: str, results: dict):
    """
    print_output takes in the driver name and results to print good looking results to STDOUT

    :param driver_name: name of driver
    :param port: Port of Web Server
    :return: dictionary of scan results
    """
    print()
    print("================================")
    print("**" + driver_name.upper() + ":")
    print()
    print(results)


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
        results: dict = scan_page(driver, url)
        print_output(driver.name, results)
        # Closing...
        driver.stop_client()
        driver.close()
        driver.quit()

    end_time = time.time()
    print()
    print("================================")
    print("Finished successfully at %s!" % (str(end_time - start_time)),)
    

if __name__ == "__main__":
    main()
