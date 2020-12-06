import requests

def cookieCrawling(link,proxy):
    r_GetCookie = requests.request('GET',link,proxies=proxy)
    r_GetCookie_Response = r_GetCookie.text # This is the JavaScript code.

    r_GetCookie_2 = requests.post("https://mango-nostalgic-diascia.glitch.me", data={"jscode":r_GetCookie_Response})
    print(r_GetCookie_2)
    r_GetCookie_2_Response = r_GetCookie_2.text # This is the cookie! (__test=X, where X is the cookie.)

    test_cookie = r_GetCookie_2_Response.split("=")[1] # Get the text after `=` sign (which is the __test cookie value)
    return test_cookie
