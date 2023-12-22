import requests
import re
import os
from bs4 import BeautifulSoup

url = input("Insert Url:")

url_pattern = re.compile(r'https?://\S+')
if not url_pattern.match(url):
    print("Invalid URL format. Exiting...")
    exit()

headers = {'User-Agent': "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebkit/537.36 (KHTML, like Gecko) Chrome/42.0.2311.135 Safari/537.36 Edge/12.246"}

r = requests.get(url=url, headers=headers)
soup = BeautifulSoup(r.content, 'html.parser')
title_tag = soup.title.contents[0].string
match = re.search(r'Komik (.*?) - Komiku', title_tag)
if match:
    title = match.group(1)
    folder_path = './{}'.format(title)
    os.mkdir(folder_path)
else:
    print("Couldn't find title from tag")
    exit()

section = soup.find(id="Baca_Komik")
images = section.find_all('img')


for img in images:
    src = img['src']
    alt= img['alt']
    filename= '{}/{}.jpg'.format(folder_path, alt)
    manga = requests.get(src,headers)
    if manga.status_code != 200:
       print('Error getting {}'.format(filename))
    else:
       with open(filename, 'wb') as f:
            noop = f.write(manga.content)
            print('Save {}'.format(filename))
