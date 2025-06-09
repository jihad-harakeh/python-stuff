# This script scrapes the current top 10 Lichess players in Blitz, Rapid, and Classical formats
# using requests and BeautifulSoup, and prints their usernames and ratings.

import requests
from bs4 import BeautifulSoup
import re

resp=requests.get('https://lichess.org/player').text
soup=BeautifulSoup(resp,'lxml')

match=soup.find_all('section',class_='user-top')


for m1 in match:
    if m1.a.text=='Blitz':
        blitz=m1
        break
print('         Top 10 Blitz players         ')
for player in blitz.find_all('li'):
    user=player.text
    print('username: ',re.findall(r'\w+(?=\d{4})',user)[0],'-','rating: ',re.findall(r'\d{4}\b',user)[0])


print('\n'*2)
for m2 in match:
    if m2.a.text=='Rapid':
        rapid=m2
        break
print('         Top 10 Rapid players         ')
for player in rapid.find_all('li'):
    user=player.text
    print('username: ',re.findall(r'\w+(?=\d{4})',user)[0],'-','rating: ',re.findall(r'\d{4}\b',user)[0])


print('\n'*2)
for m3 in match:
    if m3.a.text=='Classical':
        classical=m3
        break
print('         Top 10 Classical players         ')
for player in classical.find_all('li'):
    user=player.text
    print('username: ',re.findall(r'\w+(?=\d{4})',user)[0],'-','rating: ',re.findall(r'\d{4}\b',user)[0])
