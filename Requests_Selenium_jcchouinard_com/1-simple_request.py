#!/usr/bin/env python
'''
Simple HTTP Get Request

@author:    Jean-Christophe Chouinard. 
@role:      Sr. SEO Specialist at SEEK.com.au
@website:   jcchouinard.com
@LinkedIn:  linkedin.com/in/jeanchristophechouinard/ 
@Twitter:   twitter.com/@ChouinardJC

$ pip install requests
'''
import requests

url = 'https://www.jcchouinard.com/python-for-seo/' 

headers = {
    'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/86.0.4240.198 Safari/537.36'
}

try:
    r = requests.get(url, headers=headers)
except requests.exceptions.RequestException as e: 
    raise SystemExit(e)

print(r.text)
print(r.url)
print(r.status_code)
