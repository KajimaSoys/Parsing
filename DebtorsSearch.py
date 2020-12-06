from bs4 import BeautifulSoup
import requests
import psycopg2
from tqdm import tqdm
import random
import time
import cookiecrawler

t_host = "127.0.0.1"
t_port = "5432"
t_dbname = "FedResParsing"
t_user = "postgres"
t_pw = "Vagexyo687"
db_conn = psycopg2.connect( host = t_host , port=t_port , dbname = t_dbname , user = t_user , password = t_pw )
db_cursor = db_conn.cursor( )

url = "https://bankrot.fedresurs.ru/DebtorsSearch.aspx"
headers = {
  'authority': 'bankrot.fedresurs.ru',
  'cache-control': 'no-cache',
  'x-requested-with': 'XMLHttpRequest',
  'x-microsoftajax': 'Delta=true',
  'user-agent': 'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/87.0.4280.88 Safari/537.36',
  'content-type': 'application/x-www-form-urlencoded; charset=UTF-8',
  'accept': '*/*',
  'origin': 'https://bankrot.fedresurs.ru',
  'sec-fetch-site': 'same-origin',
  'sec-fetch-mode': 'cors',
  'sec-fetch-dest': 'empty',
  'referer': 'https://bankrot.fedresurs.ru/DebtorsSearch.aspx',
  'accept-language': 'ru-RU,ru;q=0.9,en-US;q=0.8,en;q=0.7',
  'cookie': '_ym_uid=160641223615957864; _ym_d=1606412236; bankrotcookie=6a0272eeb725e4f44a31ed445a2c267b; ASP.NET_SessionId=p4blqqghm0dnzfyhmygu55wk; _ym_visorc=w; _ym_isad=1; debtorsearch=typeofsearch=Organizations&orgname=&orgaddress=&orgregionid=&orgogrn=&orginn=&orgokpo=&OrgCategory=&prslastname=&prsfirstname=&prsmiddlename=&prsaddress=&prsregionid=&prsinn=&prsogrn=&prssnils=&PrsCategory=&pagenumber=1; debtorsearch=typeofsearch=Organizations&orgname=&orgaddress=&orgregionid=&orgogrn=&orginn=&orgokpo=&OrgCategory=&prslastname=&prsfirstname=&prsmiddlename=&prsaddress=&prsregionid=&prsinn=&prsogrn=&prssnils=&PrsCategory=&pagenumber=20'
}

#proxy_params
username = 'lum-customer-hl_1bb7049f-zone-fedres_parser'
password = 'arens2gk6cd7'
port = 22225

def newSession():
    return random.random()

def proxyBuilder():
    session_id = newSession()
    super_proxy_url = ('http://%s-country-ru-session-%s:%s@zproxy.lum-superproxy.io:%d' %
        (username, session_id, password, port))
    proxy_handler ={
        'http': super_proxy_url,
        'https': super_proxy_url,
    }
    return proxy_handler

def changePage(i):
    payload="__EVENTTARGET=ctl00%24cphBody%24gvDebtors&__EVENTARGUMENT=Page%24"
    payload += str(i)
    payload += "&"
    return payload

def POSTrequest(payload):
    urlPart="https://bankrot.fedresurs.ru"
    response = requests.request("POST", url, headers=headers, data=payload,proxies=proxyBuilder())
    soup = BeautifulSoup(response.text, features="html.parser")
    table=soup.find('table','bank') #Берем нужную табличку
    table.find('tr', 'pager').decompose() #Удаляем ненужное
    tr=table.find_all('tr') #Ищем все тэги tr
    for item in tr: #Находим нужные ссылки для дальнейшего парсинга
            if item.find('a'):
                linkPart=item.find('a')['href']   
                link=urlPart+linkPart
                links.append(link)
            else:
                pass

def GETrequest(link):
    if changedata==True:
        proxy=proxyBuilder()
        cookie={"bankrotcookie":cookiecrawler.cookieCrawling(link,proxy)}
        changedata==False
    payload={}
    response = requests.request("GET", link, cookies=cookie, data=payload,proxies=proxy)
    #with open('ya.html', 'w', encoding='utf-8') as output_file:
    #    output_file.write(response.text)
    try:
        data=dataParse(response)
        data.append(link)
    except Exception:
        print('Ошибка')
        changedata==True
        GETrequest(link)
    else:
        return data
    
    

def dataParse(response):
    data=[]
    soup = BeautifulSoup(response.text, features="html.parser")
    table=soup.find('table','au') #Берем нужную табличку
    table.find('tr', id='ctl00_cphBody_trFullName').decompose()
    table.find('tr', id="ctl00_cphBody_trOkopf").decompose()
    tr=table.find_all('span')
    for item in tr:
        if table.find('span', id="ctl00_cphBody_diffEgrulShortName"):
            table.find('span', id="ctl00_cphBody_diffEgrulShortName").decompose()
        else:
            data.append(str(item.text))
    return data

def dataExport(data):
    s = ""
    s += "INSERT INTO tbl_debstors"
    s += "("
    s += "name,address,phone,region,category_name,id_inn,id_ogrn,id_okpo,link"
    s += ") VALUES ("
    s += "%s,%s,%s,%s,%s,%s,%s,%s,%s"
    s += ")"
    db_cursor.execute(s, data)
    db_conn.commit()

links=[]
dataSet=[]
data=[]
changedata=True
for i in tqdm(range(5), desc="Парсим ссылки..."):
    payload=changePage(i+1)
    link=POSTrequest(payload)

for i in tqdm(range(27),desc="Парсим данные..."):#range(len(links)
    data=GETrequest(links[i])
    print('сработало')

try:

    #    dataExport(data)
    pass
except Exception:
    print('Произошли проблемы с выгрузкой данных в БД. Скорее всего было отправлено слишком много запросов на fedresurs.ru и парсер не смог считать необходимые данные. Повторите попытку позднее!')
else:
    print("Парсинг прошел успешно!")
finally:
    db_cursor.close()
    db_conn.close()
    m=input('Нажмите Enter для выхода :)')

#with open('ya.html', 'w', encoding='utf-8') as output_file:
#  output_file.write(response.text)
