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
                r.set(match.group(1), html)
            print(match.group(0), match.group(1))


load_folder('html/books/')

def search(path):
    files = os.listdir(path)
    for file in files:
        match = re.match(r'^book(\d+).html$', file)
        if match:
            with open(path + file, 'r') as f:
                html = f.read()
                soup = BeautifulSoup(html, 'html.parser')
                tag = str(soup.p)
                palabras = tag.split()
                for pal in palabras:
                    r.sadd("Lea"+match.group(1), pal)
search('html/books/')

