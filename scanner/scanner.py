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

import seleniumwire

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
