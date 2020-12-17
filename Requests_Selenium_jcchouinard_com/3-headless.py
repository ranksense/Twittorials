#!/usr/bin/env python
'''
Run Selenium in headless Chrome

@author:    Jean-Christophe Chouinard. 
@role:      Sr. SEO Specialist at SEEK.com.au
@website:   jcchouinard.com
@LinkedIn:  linkedin.com/in/jeanchristophechouinard/ 
@Twitter:   twitter.com/@ChouinardJC
'''
import time

from selenium import webdriver
from selenium.webdriver.chrome.options import Options

url = 'https://www.jcchouinard.com/python-for-seo/' 

options = Options()
options.headless = True
# options.add_argument("--window-size=1920,1200")
driver = webdriver.Chrome(options=options,executable_path='/usr/local/bin/chromedriver')

driver.get(url)
time.sleep(3)
t = driver.title
print(f'Title: {t}')

driver.quit()