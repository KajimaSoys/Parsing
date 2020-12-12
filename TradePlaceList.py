from bs4 import BeautifulSoup
import requests
import psycopg2
from tqdm import tqdm
import random
import cookiecrawler
import time
import csv

#db_params
t_host = "127.0.0.1"
t_port = "5432"
t_dbname = "FedResParsing"
t_user = "postgres"
t_pw = ""#password
db_conn = psycopg2.connect( host = t_host , port=t_port , dbname = t_dbname , user = t_user , password = t_pw )
db_cursor = db_conn.cursor( )


#req_params
url = "https://bankrot.fedresurs.ru/tradeplacelist.aspx"
headersPOST = {
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
  'referer': 'https://bankrot.fedresurs.ru/TradePlaceList.aspx',
  'accept-language': 'ru-RU,ru;q=0.9,en-US;q=0.8,en;q=0.7',
  'cookie': '_ym_uid=160641223615957864; _ym_d=1606412236; ASP.NET_SessionId=p4blqqghm0dnzfyhmygu55wk; _ym_isad=1; debtorsearch=typeofsearch=Organizations&orgname=robots&orgaddress=&orgregionid=&orgogrn=&orginn=&orgokpo=&OrgCategory=&prslastname=&prsfirstname=&prsmiddlename=&prsaddress=&prsregionid=&prsinn=&prsogrn=&prssnils=&PrsCategory=&pagenumber=0; bankrotcookie=6a0272eeb725e4f44a31ed445a2c267b; _ym_visorc=w; TradePlaceList=Name=&Site=&PageIndex=2&SroTradePlaceId=&SroEtpNameKey=; debtorsearch=typeofsearch=Organizations&orgname=&orgaddress=&orgregionid=&orgogrn=&orginn=&orgokpo=&OrgCategory=&prslastname=&prsfirstname=&prsmiddlename=&prsaddress=&prsregionid=&prsinn=&prsogrn=&prssnils=&PrsCategory=&pagenumber=20; TradePlaceList=Name=&Site=&PageIndex=1&SroTradePlaceId=&SroEtpNameKey='
}

#proxy_params
username = 'lum-customer-hl_1bb7049f-zone-fedres_parser'
password = ''#password
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
    src="__EVENTTARGET=ctl00%24cphBody%24TradePlaceList1%24gvTradePlace&__EVENTARGUMENT=Page%241&"
    temp=list(src)
    temp[86]=str(i)
    payload="".join(temp)    
    return payload

def POSTrequest(payload):
    urlPart="https://bankrot.fedresurs.ru"
    response = requests.request("POST", url, headers=headersPOST, data=payload,proxies=proxyBuilder())
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

def GETrequest(link,cookie, proxy):
    payload={}
    response = requests.request("GET", link, cookies=cookie, data=payload, proxies=proxy)
    data=dataParse(response)
    data.append(link)
    return data
    
def dataParse(response):
    data=[]
    soup = BeautifulSoup(response.text, features="html.parser")
    table=soup.find_all('table','au') #Берем нужную табличку
    for item in table:
        if item.find('tr', id='ctl00_cphBody_trTrades'):
            item.find('tr', id='ctl00_cphBody_trTrades').decompose()
        tr=item.find_all('tr')
        for k in tr:
                if k.find('a'):
                    if k.find('a',id='ctl00_cphBody_aSroEtp'):
                        textTemp=k.find('span')
                        data.append(textTemp.text)
                    else:
                        linkTemp=item.find('a')['href']
                        data.append(linkTemp)
                elif k.find('b'):
                    textTemp=k.find('b')
                    data.append(textTemp.text)
    for i in range(len(data)):
        data[i]=data[i].replace('\r\n\t\t\t\t\t','')
        data[i]=data[i].replace('\r\n\t\t\t\t','')
    return data 

def dataExport(data):
    s = ""
    s += "INSERT INTO tbl_tradelist"
    s += "("
    s += "company_name,web,sro_etp,date_of_admission,date_of_elemination,etp_name,address,id_inn,id_ogrn,link"
    s += ") VALUES ("
    s += "%s,%s,%s,%s,%s,%s,%s,%s,%s,%s"
    s += ")"
    db_cursor.execute(s, data)
    db_conn.commit()
                    
links=[]
dataSet=[]
data=[]
errors = 1
changedata = True

for i in tqdm(range(4), desc="Парсим ссылки..."):
    payload=changePage(i+1)
    POSTrequest(payload)

for i in tqdm(range(len(links)),desc="Парсим данные..."):#len(links)
    if changedata == True:
        proxy = proxyBuilder()
        cookie = {"bankrotcookie": cookiecrawler.cookieCrawling(links[i], proxy)}
        changedata = False
    try:
        data = GETrequest(links[i], cookie, proxy)
        dataExport(data)
    except Exception:
        time.sleep(5)
        errors += 1
        proxy = proxyBuilder()
        cookie = {"bankrotcookie": cookiecrawler.cookieCrawling(links[i], proxy)}
        try:
            data = GETrequest(links[i], cookie, proxy)
            dataExport(data)
        except Exception:
            time.sleep(10)
            errors += 1
            proxy = proxyBuilder()
            cookie = {"bankrotcookie": cookiecrawler.cookieCrawling(links[i], proxy)}
            try:
                data = GETrequest(links[i], cookie, proxy)
                dataExport(data)
            except Exception:
                time.sleep(60)
                errors += 1
                proxy = proxyBuilder()
                cookie = {"bankrotcookie": cookiecrawler.cookieCrawling(links[i], proxy)}
                try:
                    data = GETrequest(links[i], cookie, proxy)
                    dataExport(data)
                except Exception:
                    time.sleep(120)
                    errors += 1
                    proxy = proxyBuilder()
                    cookie = {"bankrotcookie": cookiecrawler.cookieCrawling(links[i], proxy)}
                    data = GETrequest(links[i], cookie, proxy)
                    dataExport(data)

    #finally:
        #f = open("TradePlaceList.csv", "w+")
        #f.close()
        #with open("TradePlaceList.csv", 'a') as outcsv:
            #writer = csv.writer(outcsv, delimiter=',', quotechar='|', quoting=csv.QUOTE_MINIMAL, lineterminator='\n')
            #for item in dataSet:
            #writer.writerow([data[0], data[1], data[2], data[3], data[4], data[5], data[6], data[7], data[8],data[9]])


try:
    #for i in tqdm(range(len(dataSet)),desc="Отправляем данные..."):
        #dataExport(dataSet[i])
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
