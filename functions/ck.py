import datetime
import json
import os
from settings.settings import green, yellow
from requests import Response
from icecream import ic
from .logger import log, log_error


def save_cookies_in_the_list(cookies: dict, account_name: str):
    current_time = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    try:
        with open("cookies/cookiesList.json", "r") as file:
            data = json.load(file)
    except FileNotFoundError:
        data = {"cookies_list": []}

    entry = {
        "account": str(account_name),
        "cookies": cookies,
        "date_logged": str(current_time)
    }

    data['cookies_list'].append(entry)

    with open('cookies/cookiesList.json', 'w') as f:
        json.dump(data, f, indent=4)

    return True


def save_cookies(cookies: dict, header: Response):
    try:
        os.mkdir("cookies")
    except OSError:
        pass
    for i in header.cookies:
        cookies[i.name] = i.value
    with open("cookies/cookies.json", "w") as cf:
        json.dump(cookies, cf, indent=4)
    return True


def clean_cookie():
    try:
        cf = json.loads(open("cookies/cookies.json", "r").read())
    except Exception as e:
        return
    if "checkpoint" in cf:
        del cf["checkpoint"]

    with open("cookies/cookies.json", "w") as cookie:
        json.dump(cf, cookie, indent=4)
    return


def display_cookies(account_name: str):
    clean_cookie()
    with open("cookies/cookies.json", "r") as c:
        cookies = json.loads(c.read())
        ic(cookies)
        save_cookies_in_the_list(cookies=cookies, account_name=account_name)
    print(f"{yellow}You can open cookies in {green}cookies/cookies.json{green}\nor you can open view cookies to display list of cookies.")


def clear_cookies():
    cookies_file = "cookies/cookies.json"
    try:
        os.remove(cookies_file)
        log(f"Deleted: {cookies_file}")
    except FileNotFoundError:
        log(f"File not found: {cookies_file}")
    return


def clear_logs():
    log_data_file = "logs/log_data.txt"
    log_browser_file = "logs/log_browser.html"
    try:
        os.remove(log_data_file)
        log(f"Deleted: {log_data_file}")
    except FileNotFoundError:
        log(f"File not found: {log_data_file}")

    try:
        os.remove(log_browser_file)
        log(f"Deleted: {log_browser_file}")
    except FileNotFoundError:
        log(f"File not found: {log_browser_file}")
    return


def open_cookies():
    try:
        cf = open("cookies/cookies.json", "r").read()
        cookies: dict = json.loads(cf)
        if "c_user" in cookies:
            pass
    except IOError:
        cookies = {"m_pixel_ratio": "3", "locale": "en_US"}
    return cookies


def open_cookie_list():
    try:
        cf = open("cookies/cookiesList.json", "r").read()
        cookies: dict = json.loads(cf)
    except IOError:
        cookies = {"cookies_list": []}
    return cookies


def merge(a: dict, b: dict):
    for i in b.keys():
        a[i] = b[i]
    return a

# def clear_cookies():
#     os.remove("cookies/cookies.json")
#     try:
#         os.remove("logs/log_data.txt")
#         os.remove("logs/log_browser.txt")
#     except:
#         pass
#     return
