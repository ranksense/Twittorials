import difflib
#from bs4 import BeautifulSoup
#import requests
from requests_html import HTMLSession
#import urllib.request
#from requests_html import AsyncHTMLSession

user_input = input("Enter a URL to generate the diff: ")

session = HTMLSession()

#grab the rendered HTML
r = session.get(user_input)
r.html.render(timeout=40)
#render_html = r.text
render_html = r.html.html

#write it to file
with open('renderhtml.txt', 'w') as f:
  for line in render_html:
    f.write(line)

#grab the raw html
r = session.get(user_input)
reg_html = r.text

#write it to file
with open('html.txt', 'w') as f:
  for line in reg_html:
      f.write(line)

#create the diff file
fromfile = 'html.txt'
tofile = 'renderhtml.txt'
fromlines = open(fromfile, 'U').readlines()
tolines = open(tofile, 'U').readlines()

diff = difflib.HtmlDiff().make_file(fromlines,tolines,fromfile,tofile)

#write the diff file
with open('diff.html', 'w') as f:
    f.write(diff)

print("Done!")
