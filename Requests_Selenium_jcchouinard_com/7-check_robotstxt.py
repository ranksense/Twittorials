#!/usr/bin/env python
'''
Check robots.txt file and save a version every time it changes.
https://www.jcchouinard.com/alert-robots-txt-changes-to-slack-using-python/

@author:    Jean-Christophe Chouinard. 
@role:      Sr. SEO Specialist at SEEK.com.au
@website:   jcchouinard.com
@LinkedIn:  linkedin.com/in/jeanchristophechouinard/ 
@Twitter:   twitter.com/@ChouinardJC

What it does:
Fetch Robots.txt. 
Read each line in the file. 
Save the file with the date. 
If a robots.txt file exists from a previous extraction, check if the file has changed. 
If it has changed, save a new version and send an Alert. 
This way, you don’t need to save a file every day, only when it changes.
'''

from datetime import datetime
import easygui # for sending msg
import requests # for sending msg
import os
import time

from functions import create_project, fetch_page, get_date, get_domain_directory

# robotstxt = 'http://127.0.0.1:5000/robots.txt'
robotstxt = 'https://www.jcchouinard.com/robots.txt'

def main(url,filename='robots.txt'):
    '''
    Combine all functions
    Get domain name from url
    Create project with domain name if not exist
    Look for existing saved robots.txt
    Fetch robots.txt url
    Compare robots.txt with last saved version
    If changed.
    Output the new robots.txt with date timestamp
    '''
    path = os.getcwd()
    site = get_domain_directory(robotstxt) # Check if project exists
    output = path + '/output/' + site + '/'
    create_project(output)
    output_files = get_files(output)
    r = fetch_page(url)
    compare_robots(output, output_files,r)

def get_files(directory):
    ''' List all files in output folder.
    '''
    output_files = os.listdir(directory)
    output_files.sort()
    return output_files

def get_latest_robotstxt(output_files):
    ''' Get only files containting robots.txt in name
    Get last saved robots.txt file.
    '''
    robots_txt = 'robots.txt'
    files = []
    for filename in output_files:
        if robots_txt in filename:
            files.append(filename)
    return files[-1]

def read_robotstxt(filename):
    ''' Read robots.txt
    '''
    if os.path.isfile(filename):
        with open(filename,'r') as f:
            txt = f.read()
    return txt

def write_robotstxt(file, output, filename='robots.txt'):
    ''' Write robots.txt to file using date as id.
    '''
    filename = get_date() + '-' + filename
    filename = output + filename
    with open(filename,'w') as f:
        f.write(file)

def compare_robots(output,output_files,r):
    '''
    Compare previous robots to actual robots.
    If different. Save File.
    '''
    new_robotstxt = r.text.replace('\r', '') # Get rid of carriage return 

    if output_files:
        robots_filename = get_latest_robotstxt(output_files) 
        filename = output + robots_filename
        last_robotstxt = read_robotstxt(filename)
        last_robotstxt = last_robotstxt.replace('\r', '')
        if new_robotstxt != last_robotstxt:
            print('Robots.txt was modified')
            write_robotstxt(new_robotstxt, output)
            message = f'The Robots.txt was changed for {filename}'
            print(message)
            # Instead of print:
            # easygui.msgbox(f'The Robots.txt was changed for {filename}', title="simple gui")
            # requests.post('https://hooks.slack.com/services/XXXXXXXXXXX',json={'text':message}, verify=False)
            # https://www.jcchouinard.com/slack-api/
        else:
            print('No Change to Robots.txt')
    else:
        print('No Existing Robots.txt. Saving one.')
        write_robotstxt(r.text, output)

if __name__ == '__main__':
    main(robotstxt)
