'''
If you are pasting this code from github, add the following files:
- diff.html
- html.txt
- renderhtml.txt
'''

#output https://twitter.com/RankSense/status/1286299845247086594

import difflib
from requests_html import HTMLSession
import re

def cleanhtml(raw_html):
  cleanr = re.compile('<.*?>')
  cleantext = re.sub(cleanr, '', raw_html)
  return cleantext

desktop_site = input("Enter the desktop version of the site: ")
mobile_site = input("Enter the mobile version of the site: ")

session = HTMLSession()

#grab the raw html
r_desktop = session.get(desktop_site)
reg_html_desktop = r_desktop.text

r_mobile = session.get(mobile_site)
reg_html_mobile = r_mobile.text

#grab the rendered HTML
try:
  r_desktop.html.render(timeout=40)
  render_html_desktop = r_desktop.html.html

  r_mobile.html.render(timeout=40)
  render_html_mobile = r_mobile.html.html 
except TimeoutError:
  print("Try increasing the timeout value")
  # "timeout=___"

render_html_desktop = cleanhtml(render_html_desktop)
render_html_mobile = cleanhtml(render_html_mobile)

with open('desktop_content.txt', 'w') as f:
  for line in render_html_desktop:
      f.write(line)

#write it to file
with open('mobile_content.txt', 'w') as f:
  for line in render_html_mobile:
    f.write(line)

#gather both HTML files to create the diff
fromfile = 'desktop_content.txt'
tofile = 'mobile_content.txt'
fromlines = open(fromfile, 'r').readlines()
tolines = open(tofile, 'r').readlines()

#creates the diff file
diff = difflib.HtmlDiff().make_file(fromlines,tolines,fromfile,tofile)

#write the diff file
with open('diff.html', 'w') as f:
  f.write(diff)

#confirmation message
print("Done!")
