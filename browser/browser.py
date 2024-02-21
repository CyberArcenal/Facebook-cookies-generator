import sys
import time

from functions.logger import log, log_error
from functions.ck import open_cookie_list, open_cookies, save_cookies
from settings.br import open_headers, save_Referer
from settings.settings import DEBUG, session, red, green, blue, yellow
from functions.soup import print_page_title, _print_page__


def wait():
    a = ["..\..", "..|..", "../..", "..\..", "..|..", "../.."]
    for i in a:
        sys.stdout.write(f"\033[1000D\033[1;92m{i}")
        sys.stdout.flush()
        time.sleep(1)


def log_page(page: str):
    try:
        with open("logs/log_browser.html", 'a') as f:
            top = "====================PAGE START====================\n"
            bot = "====================PAGE BOTTOM=====================\n\n"
            f.write(f"{top}\n{str(page.text)}\n{bot}")
            f.close()
    except:
        pass
    return


def log_data(data: dict):
    try:
        with open("logs/log_data.txt", 'a') as f:
            f.write(str(data)+"\n")
        f.close()
    except:
        pass
    return


def browser(url, data=None, redirect=True, print_page=False, print_title=False):
    while True:
        try:
            # cookies
            cookies = open_cookies()
            # header
            header = open_headers()
            # requests
            if not data:
                if DEBUG:
                    log(f"Browser get method {url}")
                page = session.get(url, headers=header,
                                   cookies=cookies, allow_redirects=redirect)
            else:
                if DEBUG:
                    log(f"Browser post method {url} data = {data}")
                page = session.post(
                    url, headers=header, data=data, cookies=cookies, allow_redirects=redirect)
            # log
            if DEBUG:
                log(f"Browser response url {page.url}")
            # function
            log_page(page=page)
            log_data(data=data)
            if print_page:
                _print_page__(page_text=page.text, pritie=True)
            if print_title:
                print_page_title(page_text=page.text)

            if save_cookies(cookies, page) and save_Referer(page):
                return page
        except Exception as e:
            # log_error(e)
            wait()
            log("\n\033[1;92m║ reconnecting..")
