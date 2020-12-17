from datetime import datetime
import os
import requests 

from bs4 import BeautifulSoup
from urllib.parse import urlparse

def create_project(directory):
    '''
    Create a project if it does not exist
    '''
    if not os.path.exists(directory):
        print('Create project: '+ directory)
        os.makedirs(directory)
    else:
        print(f'{directory} project exists')

def fetch_page(url,allow_redirects=True,timeout=3):
    '''
    Use requests to fetch URL
    '''
    print(f'Fetching {url}')
    try:
        r = requests.get(url,allow_redirects=allow_redirects,timeout=timeout)
    except requests.exceptions.ProxyError:
        r = 'ProxyError'
    except requests.exceptions.SSLError:
        r = 'SSLError'
    except requests.exceptions.Timeout:
        r = 'ConnectionTimeout'
    except requests.exceptions.TooManyRedirects:
        r = 'TooManyRedirects'
    except requests.exceptions.ConnectionError:
        r = 'ConnectionError'
    except requests.exceptions.HTTPError:
        r = 'HTTPError'
    except requests.exceptions.InvalidURL:
        r = 'InvalidURL'
    return r

def get_domain_name(url):
    return '{uri.scheme}://{uri.netloc}'.format(uri=urlparse(url))

def get_date():
    '''
    Get today's date as YYYY-MM-DD
    '''
    return datetime.today().strftime('%Y-%m-%d:%H:%M%S')

def get_domain_directory(start_url):
    '''
    Get Domain Name in the www_domain_com format
    1. Parse URL
    2. Get Domain
    3. Replace dots to make a usable folder path
    '''
    url = urlparse(start_url)               # Parse URL into components
    domain_name = url.netloc                # Get Domain (or network location)
    domain_name = domain_name.replace('.','_')# Replace . by _ to create usable folder
    domain_name = domain_name.split(':')[0]
    return domain_name

def get_canonical_from_html(response):
        '''
        Finds all the <link rel="canonical"> tags.
        It returns True when:
        - there is only one canonical tag;
        - The canonical matches with the page.
        
        It returns False when a page is not indexable or has an error:
        -There is more than one canonical;
        -There is no canonical.
        -Canonical is not self-referrential
        '''
        soup = BeautifulSoup(response.content, "lxml")
        canonicals = soup.find_all('link', {'rel': 'canonical'})
        canonical_tag = canonicals if canonicals else False 
        if canonical_tag is not False:
            if len(canonicals) == 1:
                canonical_link = canonical_tag[0]['href']
                if canonical_link == response.url:
                    return True, canonical_link
                else:
                    return False, canonical_link
            else:
                return False, 'Multiple Canonical Tags Found'
        else:
            return True, 'No Canonical Tag Found'