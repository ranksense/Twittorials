#!/usr/bin/env python
'''
Time different types of request

@author:    Jean-Christophe Chouinard. 
@role:      Sr. SEO Specialist at SEEK.com.au
@website:   jcchouinard.com
@LinkedIn:  linkedin.com/in/jeanchristophechouinard/ 
@Twitter:   twitter.com/@ChouinardJC
'''
from functools import wraps
import requests
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from time import time

url = 'https://www.jcchouinard.com/python-for-seo/' 

headers = {
    'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/86.0.4240.198 Safari/537.36'
}

def timing(f):
    ''' https://codereview.stackexchange.com/questions/169870/decorator-to-measure-execution-time-of-a-function
    '''
    @wraps(f)
    def wrapper(*args, **kwargs):
        start = time()
        result = f(*args, **kwargs)
        end = time()
        print(f'{f.__name__} elapsed time: {end-start}')
        return result
    return wrapper

@timing # Equivalent to timing(make_request(url))
def make_request(url):
    ''' Time a simple HTTP request
    '''
    try:
        r = requests.get(url, headers=headers)
    except requests.exceptions.RequestException as e: 
        raise SystemExit(e)
    html = r.text
    return html

@timing
def headless_chrome(url,headless=True):
    '''
    Run Selenium.
    url: full url that you want to extract
    headless: define if your want to see the browser opening or not.
    '''
    options = Options()
    options.headless = headless
    driver = webdriver.Chrome(options=options,executable_path='/usr/local/bin/chromedriver')
    driver.get(url)
    html = driver.page_source
    driver.quit()
    return html

if __name__ == '__main__': 
    source_html = make_request(url)
    rendered_html = headless_chrome(url,headless=True)