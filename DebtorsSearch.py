from bs4 import BeautifulSoup
import requests
import psycopg2
from tqdm import tqdm
import random
import time
import cookiecrawler
import csv

# Параметры для бд
t_host = "127.0.0.1"
t_port = "5432"
t_dbname = "FedResParsing"
t_user = "postgres"
t_pw = "Vagexyo687"
db_conn = psycopg2.connect(host=t_host, port=t_port, dbname=t_dbname, user=t_user, password=t_pw)
db_cursor = db_conn.cursor()

# Параметры для POST запроса
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

# Параметры для прокси
username = 'lum-customer-hl_1bb7049f-zone-fedres_parser'
password = 'arens2gk6cd7'
port = 22225


# Рандомим новую сессию для прокси
def newSession():
    return random.random()


# Получаем новые прокси
def proxyBuilder():
    session_id = newSession()
    super_proxy_url = ('http://%s-country-ru-session-%s:%s@zproxy.lum-superproxy.io:%d' %
                       (username, session_id, password, port))
    proxy_handler = {
        'http': super_proxy_url,
        'https': super_proxy_url,
    }
    return proxy_handler


# Меняем страницу
def changePage(i):
    payload = "__EVENTTARGET=ctl00%24cphBody%24gvDebtors&__EVENTARGUMENT=Page%24"
    payload += str(i)
    payload += "&"
    return payload


# POST реквест для парсинга ссылок на объекты
def POSTrequest(payload):
    urlPart = "https://bankrot.fedresurs.ru"
    response = requests.request("POST", url, headers=headers, data=payload, proxies=proxyBuilder())
    soup = BeautifulSoup(response.text, features="html.parser")
    table = soup.find('table', 'bank')  # Берем нужную табличку
    table.find('tr', 'pager').decompose()  # Удаляем ненужное
    tr = table.find_all('tr')  # Ищем все тэги tr
    for item in tr:  # Находим нужные ссылки для дальнейшего парсинга
        if item.find('a'):
            linkPart = item.find('a')['href']
            link = urlPart + linkPart
            links.append(link)
        else:
            pass


# GET запрос для самих объектов
def GETrequest(link, cookie, proxy):
    payload = {}
    response = requests.request("GET", link, cookies=cookie, data=payload, proxies=proxy)
    data = dataParse(response)
    data.append(link)
    return data


# Собираем нужные данные
def dataParse(response):
    data = []
    soup = BeautifulSoup(response.text, features="html.parser")
    table = soup.find('table', 'au')  # Берем нужную табличку
    table.find('tr', id='ctl00_cphBody_trFullName').decompose()
    table.find('tr', id="ctl00_cphBody_trOkopf").decompose()
    tr = table.find_all('span')
    for item in tr:
        if table.find('span', id="ctl00_cphBody_diffEgrulShortName"):
           table.find('span', id="ctl00_cphBody_diffEgrulShortName").decompose()
        elif table.find('span', id="ctl00_cphBody_diffEgrulInn"):
           table.find('span', id="ctl00_cphBody_diffEgrulInn").decompose()
        #if table.find('span', 'diff-sign pointer'):
        #    table.find_all('span', 'diff-sign pointer').decompose()
        else:
            data.append(str(item.text))
    return data


# Передача данных в БД
def dataExport(data):
    s = ""
    s += "INSERT INTO tbl_debstors"
    s += "("
    s += "name,address,phone,region,category_name,id_inn,id_ogrn,id_okpo,link"
    s += ") VALUES ("
    s += "%s,%s,%s,%s,%s,%s,%s,%s,%s"
    s += ")"
    try:
        db_cursor.execute(s, data)
        db_conn.commit()
    except Exception:
        #pass
        uploaderrors+=1
    else:
        pass


links = []
dataSet = []
data = []
errors = 1
uploaderrors=0
changedata = True

for i in tqdm(range(50), desc="Парсим ссылки..."):
    payload = changePage(i + 1)
    link = POSTrequest(payload)
#Во время парсинга в случае высокой нагрузки даем серверу немного передохнуть, но не сбавляем общий темп
for i in tqdm(range(len(links)), desc="Парсим данные..."):  # range(len(links)
    if changedata == True:
        proxy = proxyBuilder()
        cookie = {"bankrotcookie": cookiecrawler.cookieCrawling(links[i], proxy)}
        changedata = False
    try:
        data = GETrequest(links[i], cookie, proxy)
    except Exception:
        time.sleep(5)
        errors += 1
        proxy = proxyBuilder()
        cookie = {"bankrotcookie": cookiecrawler.cookieCrawling(links[i], proxy)}
        try:
            data = GETrequest(links[i], cookie, proxy)
        except Exception:
            time.sleep(10)
            errors += 1
            proxy = proxyBuilder()
            cookie = {"bankrotcookie": cookiecrawler.cookieCrawling(links[i], proxy)}
            try:
                data = GETrequest(links[i], cookie, proxy)
            except Exception:
                time.sleep(60)
                errors += 1
                proxy = proxyBuilder()
                cookie = {"bankrotcookie": cookiecrawler.cookieCrawling(links[i], proxy)}
                try:
                    data = GETrequest(links[i], cookie, proxy)
                except Exception:
                    time.sleep(120)
                    errors += 1
                    proxy = proxyBuilder()
                    cookie = {"bankrotcookie": cookiecrawler.cookieCrawling(links[i], proxy)}
                    data = GETrequest(links[i], cookie, proxy)
                    dataExport(data)
                else:
                    dataExport(data)
            else:
                dataExport(data)
        else:
            dataExport(data)
    else:
        dataExport(data)
    finally:
        f = open("DebstorSearchBackup.csv", "w+")
        f.close()
        with open("DebstorSearchBackup.csv", 'a') as outcsv:
            writer = csv.writer(outcsv, delimiter=',', quotechar='|', quoting=csv.QUOTE_MINIMAL, lineterminator='\n')
            #for item in dataSet:
            writer.writerow([data[0], data[1], data[2], data[3], data[4], data[5], data[6], data[7], data[8]])

try:
    #for i in tqdm(range(len(dataSet)), desc="Отправляем данные..."):
    #    dataExport(dataSet[i])
    pass
except Exception:
    print('Произошли проблемы с выгрузкой данных в БД. Обработанные данные были записаны в DebstorSearchBackup.csv')
else:
    print("Парсинг прошел успешно!\nКоличество подмен ip и cookie: ", errors,"Количество ошибок при записи: ",uploaderrors)
finally:
    db_cursor.close()
    db_conn.close()
    m = input('Нажмите Enter для выхода :)')

# with open('ya.html', 'w', encoding='utf-8') as output_file:
#  output_file.write(response.text)
