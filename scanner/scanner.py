"""
File: scanner.py
Assignment: Mini Project 2
Lanuguage: python3
Author: Sean Kells <spk3077@rit.edu>
Purpose: Scan web page for DOM-XSS vulnerabilities using Selenium
Running: python3 scanner.py <IP> <Port> <Scheme (HTTP/HTTPS>)
Example Run: python3 scanner.py localhost 80 http
"""
import sys
import re
import time

import seleniumwire

def check_input():
    """
    check_input checks for input errors

    :return: Nothing
    """
    # Check arguments are present
    if not len(sys.argv) == 4:
        print("There must be three arguments to script")
        print("EX: python3 scanner.py <IP> <Port> <Scheme>")
        print("EX: python3 scanner.py 127.0.0.1 80 http")
        exit(1)
    
    # Check <IP> Argument Format
    elif not sys.argv[1] == 'localhost' and not re.match(r'^[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}$', sys.argv[1]) \
        and not re.match(r'^([\w\-_]+(?:(?:\.[\w\-_]+)+))$', sys.argv[1]):
        print("The IP argument should be the format x.x.x.x or localhost")
        print("EX: python3 scanner.py <IP> <Port> <Scheme>")
        print("EX: python3 scanner.py 127.0.0.1 80 http")
        exit(1)

    # Check <Port> Argument Format
    elif not re.match(r'^[0-9]{1,5}$', sys.argv[2]):
        print("The port argument should be numeric")
        print("EX: python3 scanner.py <IP> <Port> <Scheme>")
        print("EX: python3 scanner.py 127.0.0.1 80 http")
        exit(1)

    # Check <Scheme> Argument Format
    elif not sys.argv[3] == "http" and not sys.argv[3] == "https":
        print("The scheme argument should be http or https")
        print("EX: python3 scanner.py <IP> <Port> <Scheme>")
        print("EX: python3 scanner.py 127.0.0.1 80 http")
        exit(1)



def main():
    """
    main is the primary intended Python script to run to execute entire server

    :return: Nothing
    """
    check_input()
    start_time = time.time()

    end_time = time.time()
    print("Finished successfully at %s!" % (str(end_time - start_time)),)
    

if __name__ == "__main__":
    main()
