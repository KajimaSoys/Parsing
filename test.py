from bs4 import BeautifulSoup
import requests

url = "https://bankrot.fedresurs.ru/tradeplacelist.aspx"
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
      'referer': 'https://bankrot.fedresurs.ru/tradeplacelist.aspx',
      'accept-language': 'ru-RU,ru;q=0.9,en-US;q=0.8,en;q=0.7',
      'cookie': '_ym_uid=160641223615957864; _ym_d=1606412236; ASP.NET_SessionId=vd20xsxon2fqd5heuihutb45; _ym_isad=1; fedresurscookie=78d6e3b1475786b29bdbc09c2ad7f2bf; bankrotcookie=6a0272eeb725e4f44a31ed445a2c267b; _ym_visorc=w; TradePlaceList=Name=&Site=&PageIndex=1&SroTradePlaceId=&SroEtpNameKey=; ASP.NET_SessionId=vd20xsxon2fqd5heuihutb45; metrika_enabled=1; TradePlaceList=Name=&Site=&PageIndex=1&SroTradePlaceId=&SroEtpNameKey='
    }

def changePage(i):
    src="__EVENTTARGET=ctl00%24cphBody%24TradePlaceList1%24gvTradePlace&__EVENTARGUMENT=Page%241&__VIEWSTATE=%2FwEPDwUJNDcwMTU1MDkwD2QWAmYPZBYEZg8UKwACFCsAAw8WAh4XRW5hYmxlQWpheFNraW5SZW5kZXJpbmdoZGRkZGQCAw9kFgwCBA9kFgICBg8PFgIfAGhkZAIJDw8WAh4LTmF2aWdhdGVVcmwFH2h0dHBzOi8vZmVkcmVzdXJzLnJ1L21vbml0b3JpbmdkZAILDw8WAh8BBRhodHRwOi8vd3d3LmZlZHJlc3Vycy5ydS9kZAIaD2QWAmYPFgIeC18hSXRlbUNvdW50AgMWBmYPZBYCZg8VAwowMy4xMi4yMDIwPmh0dHBzOi8vZmVkcmVzdXJzLnJ1L25ld3MvMjU2NDA1N2EtOWYxMy00NmU3LWEzZDItZjA3Y2ZiYjFjM2U1sAHQmtC%2B0LvQuNGH0LXRgdGC0LLQviDQsdCw0L3QutGA0L7RgtGB0YLQsiDQsiDQodCo0JAg0YPQv9Cw0LvQviDQtNC%2BINC80LjQvdC40LzRg9C80LAg0LfQsCAxNCDQu9C10YIg0LIg0YHQstGP0LfQuCDRgSDQvdC40LfQutC40Lwg0YfQuNGB0LvQvtC8INC70LjRh9C90YvRhSDQsdCw0L3QutGA0L7RgtGB0YLQsmQCAQ9kFgJmDxUDCjAzLjEyLjIwMjA%2BaHR0cHM6Ly9mZWRyZXN1cnMucnUvbmV3cy80YTY5YjBiYi01MTM1LTRhMGQtOGYwNS01N2QwNWNiODIzMGOQAdCf0L7Qv9GA0LDQstC60Lgg0LIg0J3QmiDQoNCkINC%2BINGA0LXQs9GD0LvQuNGA0L7QstCw0L3QuNC4INC%2B0L%2FQtdGA0LDRhtC40Lkg0YEg0YbQuNGE0YDQvtCy0L7QuSDQstCw0LvRjtGC0L7QuSDQstC90LXRgdC10L3RiyDQsiDQk9C%2B0YHQtNGD0LzRg2QCAg9kFgJmDxUDCjAzLjEyLjIwMjA%2BaHR0cHM6Ly9mZWRyZXN1cnMucnUvbmV3cy81NTA0NWRkYy1kNjM2LTQwZjMtOGVlYS1kZDhiMWNjZmQzMDj6AdCS0KEg0YDQsNGB0YHQvNC%2B0YLRgNC40YIg0YHQv9C%2B0YAg0L4g0L3QtdC00LXQudGB0YLQstC40YLQtdC70YzQvdC%2B0YHRgtC4INGB0LTQtdC70LrQuCDQv9C%2BINGD0LLQtdC70LjRh9C10L3QuNGOINC60LDQv9C40YLQsNC70LAg0L7QsdGJ0LXRgdGC0LLQsCDRgSDRg9GH0LDRgdGC0LjQtdC8INCx0LDQvdC60YDQvtGC0LAgLSDQn9CRIMKr0J7Qu9C10LLQuNC90YHQutC40LksINCR0YPRjtC60Y%2FQvSDQuCDQv9Cw0YDRgtC90LXRgNGLwrtkAhsPZBYCAgEPFgIfAgIHFg5mD2QWAmYPFQIVaHR0cDovL2thZC5hcmJpdHIucnUvMNCa0LDRgNGC0L7RgtC10LrQsCDQsNGA0LHQuNGC0YDQsNC20L3Ri9GFINC00LXQu2QCAQ9kFgJmDxUCQGh0dHA6Ly93d3cuZWNvbm9teS5nb3YucnUvbWluZWMvYWN0aXZpdHkvc2VjdGlvbnMvQ29ycE1hbmFnbWVudC8v0JzQuNC90Y3QutC%2B0L3QvtC80YDQsNC30LLQuNGC0LjRjyDQoNC%2B0YHRgdC40LhkAgIPZBYCZg8VAhVodHRwOi8vZWdydWwubmFsb2cucnUW0JXQk9Cg0K7QmyDQpNCd0KEg0KDQpGQCAw9kFgJmDxUCJWh0dHA6Ly90ZXN0LmZlZHJlc3Vycy5ydS9kZWZhdWx0LmFzcHgo0KLQtdGB0YLQvtCy0LDRjyDQstC10YDRgdC40Y8g0JXQpNCg0KHQkWQCBA9kFgJmDxUCHmh0dHA6Ly90ZXN0LWZhY3RzLmludGVyZmF4LnJ1LyzQotC10YHRgtC%2B0LLQsNGPINCy0LXRgNGB0LjRjyDQldCk0KDQodCU0K7Qm2QCBQ9kFgJmDxUCJSAgaHR0cDovL2ZvcnVtLWZlZHJlc3Vycy5pbnRlcmZheC5ydS8y0KTQvtGA0YPQvCDQpNC10LTQtdGA0LDQu9GM0L3Ri9GFINGA0LXQtdGB0YLRgNC%2B0LJkAgYPZBYCZg8VAi5odHRwOi8vYmFua3JvdC5mZWRyZXN1cnMucnUvSGVscC9GQVFfRUZSU0IucGRmNNCn0LDRgdGC0L4g0LfQsNC00LDQstCw0LXQvNGL0LUg0LLQvtC%2F0YDQvtGB0YsgKEZBUSlkAh0PZBYCAgEPZBYCZg9kFgICAQ9kFgICAQ9kFgICAQ9kFgZmDw8WAh4EVGV4dGUWAh4Hb25jbGljawU%2FT3Blbk1vZGFsV2luZG93X2N0bDAwX2NwaEJvZHlfVHJhZGVQbGFjZUxpc3QxX21zU3JvVHJhZGVQbGFjZSgpZAIBDw9kFgIfBAU%2FT3Blbk1vZGFsV2luZG93X2N0bDAwX2NwaEJvZHlfVHJhZGVQbGFjZUxpc3QxX21zU3JvVHJhZGVQbGFjZSgpZAICDw9kFgIfBAU1Q2xlYXJfY3RsMDBfY3BoQm9keV9UcmFkZVBsYWNlTGlzdDFfbXNTcm9UcmFkZVBsYWNlKClkGAIFHl9fQ29udHJvbHNSZXF1aXJlUG9zdEJhY2tLZXlfXxYJBRZjdGwwMCRyYWRXaW5kb3dNYW5hZ2VyBSljdGwwMCRQcml2YXRlT2ZmaWNlMSRpYlByaXZhdGVPZmZpY2VFbnRlcgUhY3RsMDAkUHJpdmF0ZU9mZmljZTEkY2JSZW1lbWJlck1lBSBjdGwwMCRQcml2YXRlT2ZmaWNlMSRSYWRUb29sVGlwMQUfY3RsMDAkUHJpdmF0ZU9mZmljZTEkaWJ0UmVzdG9yZQUiY3RsMDAkRGVidG9yU2VhcmNoMSRpYkRlYnRvclNlYXJjaAUnY3RsMDAkY3BoQm9keSRUcmFkZVBsYWNlTGlzdDEkYnRuU2VhcmNoBShjdGwwMCRjcGhCb2R5JFRyYWRlUGxhY2VMaXN0MSRpYlNyb0NsZWFyBSpjdGwwMCRjcGhCb2R5JFRyYWRlUGxhY2VMaXN0MSRjYlRyYWRlUGxhY2UFKmN0bDAwJGNwaEJvZHkkVHJhZGVQbGFjZUxpc3QxJGd2VHJhZGVQbGFjZQ88KwAMAgICAQgCBGSlULAelL4Pgb4vXsyO%2F91q1e9tjw%3D%3D&__VIEWSTATEGENERATOR=808E3FD5&__ASYNCPOST=true&"
    temp=list(src)
    temp[86]=str(i)
    payload="".join(temp)    
    return payload

def POSTrequest(payload):
    urlPart="https://bankrot.fedresurs.ru"
    response = requests.request("POST", url, headers=headers, data=payload)
    soup = BeautifulSoup(response.text, features="html.parser")
    table=soup.find('table','bank') #Берем нужную табличку
    table.find('tr', 'pager').decompose() #Удаляем ненужное
    tr=table.find_all('tr') #Ищем все тэги tr
    #print(tr)

    for item in tr: #Находим нужные ссылки для дальнейшего парсинга
            if item.find('a'):
                linkPart=item.find('a')['href']   
                link=urlPart+linkPart
                links.append(link)
            else:
                pass

def GETrequest(link):
    payload={}
    response = requests.request("GET", link, headers=headers, data=payload)
    with open('ya.html', 'w', encoding='utf-8') as output_file:
        output_file.write(response.text)
    data=dataParse(response)
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

                    
links=[]
dataSet=[]
data=[]
for i in range(4):
    payload=changePage(i+1)
    POSTrequest(payload)
#GETrequest(links[1])
for i in range(10):
    data=GETrequest(links[i])
    dataSet.append(data)
print(dataSet)
#with open('ya.html', 'w', encoding='utf-8') as output_file:
#  output_file.write(response.text)
