#! python3
# -*- coding: utf-8 -*-

# ncodeWebScraper.py - Given a WebNovel, scan through each chapter for a keyword
# and return the chapters with the keyword

# Issues: Cannot get this to work with window consoles
# Not sure if this applies to other OSs
# Tested to work in IDLE environment

import bs4 as bs
import requests
import re
import sys
from multiprocessing.dummy import Pool as ThreadPool

# Returns the url if the term is found within its text
def term_in_chapter(url):
    global searchTerm
    global pRegex
    r = requests.get(url)
    soup = bs.BeautifulSoup(r.content, 'lxml')
    for paragraph in soup.find_all('p'):
        if paragraph.br:
            continue
        if 'id' in paragraph.attrs:
            if pRegex.search(paragraph.get('id')):
                if searchTerm in paragraph.text:
                    return url
    return None

# Get User Inputs
print('Enter WebNovel ID:')
wnID = input()

print('Enter Search Term:')
searchTerm = input()

# Init Variables
base = 'https://ncode.syosetu.com'
pRegex = re.compile(r'L\d+')
wnURL = base + '/' + wnID
chstr = '/' + re.escape(wnID) + r'/\d+'
chapterRegex = re.compile(chstr)
chapters = []

# Get Chapter Links
r = requests.get(wnURL)

# Check for Invalid Web Novel
if r.status_code == 404:
    print('Invalid Web Novel or Couldn\'t be found')
    sys.exit()
    
soup = bs.BeautifulSoup(r.content, 'lxml')
for link in soup.find_all('a'):
    if chapterRegex.search(link.get('href')):
        chapters.append(base + link.get('href'))

# Create Threads
pool = ThreadPool(8)
results = pool.map(term_in_chapter, chapters)

# Close Threads
pool.close()
pool.join()

# Print Results
print('Found Chapters: ')
for chapter in chapters:
    if chapter:
        print(chapter)
