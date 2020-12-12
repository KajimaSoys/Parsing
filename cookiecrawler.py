import requests
import time

def cookieCrawling(link,proxy):
    r_GetCookie = requests.request('GET',link,proxies=proxy)
    r_GetCookie_Response = r_GetCookie.text #Парсим js код
    try:
        r_GetCookie_2 = requests.post("https://mango-nostalgic-diascia.glitch.me", data={"jscode":r_GetCookie_Response})#Отправляем код на сервер для обработки
            
        r_GetCookie_2_Response = r_GetCookie_2.text # Нужные нам куки

        test_cookie = r_GetCookie_2_Response.split("=")[1] #Удаляем ненужную часть строки
    except Exception:
        time.sleep(3)
        r_GetCookie_2 = requests.post("https://mango-nostalgic-diascia.glitch.me", data={"jscode":r_GetCookie_Response})#Отправляем код на сервер для обработки
            
        r_GetCookie_2_Response = r_GetCookie_2.text # Нужные нам куки

        test_cookie = r_GetCookie_2_Response.split("=")[1] #Удаляем ненужную часть строки
        return test_cookie
    else:
        return test_cookie

    
