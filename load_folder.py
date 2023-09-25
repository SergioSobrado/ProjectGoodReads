import os
import redis
from bs4 import BeautifulSoup
import re
# https://github.com/redis/redis-py

r = redis.Redis(host='localhost', port=6379, db=0)


def load_folder(path):
    files = os.listdir(path)
    print(files)
    for file in files:
        match = re.match(r'^book(\d+).html$', file)
        if match:
            with open(path + file) as f:
                html = f.read()
                book_id = match.group(1)
                search(book_id, html)
                r.set(book_id, html)
            print(match.group(0), book_id)

def search(book_id, html):
    soup = BeautifulSoup(html, 'html.parser')
    tag = str(soup.p)
    palabras = tag.split()
    for pal in palabras:
        r.sadd("Lea"+book_id, pal)

load_folder('html/books/')
