# domxss-scanner
Selenium Python Project to Scan for DOM XSS vulnerabilities on a site.  Includes Tests!

## Prerequisites
The script assumes you are running the web server on the latest Ubuntu version
Run and install the necessary dependencies below:

    # Clone GitHub
    git clone https://github.com/spk3077/domxss-scanner

    # Enter Local Repository
    cd domxss-scanner

    # Install requirements
    pip install -r requirements.txt


## Script Parameters
python3 scanner.py SITE

    **SITE**
    The URL for the target webpage


## Running Scanner

    # Enter scanner directory
    cd scanner/

    # Execute Selenium Script
    python3 scanner.py https://www.rit.edu


## Running Tests

    # Enter tests directory
    cd tests/

    # Run Docker-Compose
    docker-compose up


### The Tests
Pictures of Exploitation for each test

EX1:
![Alt text](images/ex1.png?raw=true "EX1")

EX2:
![Alt text](images/ex2.png?raw=true "EX2")

EX3:
![Alt text](images/ex3.png?raw=true "EX3")

EX4:
![Alt text](images/ex4.png?raw=true "EX4")

EX5:
![Alt text](images/ex5.png?raw=true "EX5")
