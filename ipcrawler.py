from bs4 import BeautifulSoup
import requests
import time
from tqdm import tqdm
import cookiecrawler

import sys
#import urllib.request
import random
username = 'lum-customer-hl_1bb7049f-zone-fedres_parser'
password = 'arens2gk6cd7'
port = 22225
def newses():
    #session_id = random.random()
    return random.random()

for i in range(1):
    session_id = newses()
    super_proxy_url = ('http://%s-country-ru-session-%s:%s@zproxy.lum-superproxy.io:%d' %
        (username, session_id, password, port))
    proxy_handler ={
        'http': super_proxy_url,
        'https': super_proxy_url,
    }
    #opener = urllib.request.build_opener(proxy_handler)
    #opener.addheaders = [('user-agent', 'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/87.0.4280.88 Safari/537.36')]

    #print('Performing request')
    #print(opener.open('http://checkip.dyndns.org').read())
    #ip=opener.open('http://checkip.dyndns.org').read()
    #soup = BeautifulSoup(ip, 'html.parser')
    #print(soup.find('body').text)
#with open('ya.html', 'w', encoding='utf-8') as output_file:
#  output_file.write(opener.open('http://checkip.dyndns.org').read())

url='https://bankrot.fedresurs.ru/OrganizationCard.aspx?ID=19CEEEDBF9A29BB97624A246AB000EA8'
bankrotcookie=cookiecrawler.cookieCrawling(url,proxy_handler)
response= requests.request('GET',url,cookies={'bankrotcookie':bankrotcookie},proxies=proxy_handler)
soup = BeautifulSoup(response.text, 'html.parser')  
with open('ya.html', 'w', encoding='utf-8') as output_file:
  output_file.write(response.text)
print(response.text)
