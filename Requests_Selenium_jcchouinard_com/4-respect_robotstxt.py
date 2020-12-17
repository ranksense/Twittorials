#!/usr/bin/env python
'''
Check Robots.txt before Fetching a page

@author:    Jean-Christophe Chouinard. 
@role:      Sr. SEO Specialist at SEEK.com.au
@website:   jcchouinard.com
@LinkedIn:  linkedin.com/in/jeanchristophechouinard/ 
@Twitter:   twitter.com/@ChouinardJC

What it does:
Check base URL given,
Get the robots.txt url from the base url
Fetch Robots.txt and check if URL is allowed
If it is allowed, run Selenium and print Title of the page
'''
from reppy.robots import Robots
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from termcolor import colored

from functions import get_domain_name

domain = 'https://www.jcchouinard.com/'

uris = [
    'python-for-seo',
    'wp-content',
    'learn-selenium-python-seo-automation',
    'learn-git-and-github',
    'python-automation-with-cron-on-mac',
    'google-search-console-api',
    'chrome-devtools-commands-for-seo',
    'how-to-use-reddit-api-with-python'
    ]

urls = [domain + uri for uri in uris] # combine domain to URL

def get_robots_url(url):
    '''
    Convert URL to get the /robots.txt url
    '''
    domain_url = get_domain_name(url)
    robots_url = domain_url + '/robots.txt'
    return robots_url

def robot_parser(url):
    '''
    Parse the Robots.txt.
    Send True if it is allowed to crawl
    '''
    robotstxt = get_robots_url(url)
    parser = Robots.fetch(robotstxt)
    validation = parser.allowed(url, '*')
    return validation

def get_title(url,headless=True):
    '''
    Run Selenium.
    Print Title.
    url: full url that you want to extract
    headless: define if your want to see the browser opening or not.
    '''
    print(colored(f'Opening {url}','green')) # make it fancy
    options = Options()
    options.headless = headless
    driver = webdriver.Chrome(options=options,executable_path='/usr/local/bin/chromedriver')
    driver.get(url)
    t = driver.title
    print(f'Title: {t}')
    driver.quit()

def run_selenium(url):
    '''
    Check if robots.txt allows.
    If it does, run print_title()
    Else. Tell the user it is blocked
    '''
    validation = robot_parser(url)
    if validation:
        get_title(url)
    else:
        print(colored(f'{url} is blocked by robots.txt','red'))

for url in urls:
    run_selenium(url)
print('Done')
    
