#! python
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

print(sys.stdout.encoding)
foundChapters = []
base = 'https://ncode.syosetu.com'
pRegex = re.compile(r'L\d+')
print('Enter WebNovel ID:')
wnID = input()
# wnID = 'n8559fc'
print('WebNovel ID is: ' + wnID)
wnURL = base + '/' + wnID
chstr = '/' + re.escape(wnID) + r'/\d+'
chapterRegex = re.compile(chstr)
print('Enter Search Term:')
searchTerm = input()
# searchTerm = '「婚約を破棄、ということでよろしいでしょうか？　」'
# print(type(searchTerm))
print('Search Term is: ' + searchTerm)

r = requests.get(wnURL)
soup = bs.BeautifulSoup(r.content, 'lxml')
for link in soup.find_all('a'):
    if chapterRegex.search(link.get('href')):
        chapter = link.get('href')
        print('Searching: ' + chapter)
        cr = requests.get(base + chapter)
        csoup = bs.BeautifulSoup(cr.content, 'lxml')
        for paragraph in csoup.find_all('p'):
            if paragraph.br:
                continue
            if 'id' in paragraph.attrs:
                if pRegex.search(paragraph.get('id')):
                    # print(paragraph.get('id'))
                    # print(paragraph.text)
                    # print(paragraph.text.encode(
                    #     sys.stdout.encoding, errors='replace'))
                    if searchTerm in paragraph.text:
                        # print('FOUND MATCH')
                        foundChapters.append(chapter)
                        break

# print(foundChapters)
print('Found Chapters: ')
for chapter in foundChapters:
    print(chapter)
