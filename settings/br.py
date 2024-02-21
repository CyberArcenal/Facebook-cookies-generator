from functions.logger import log, log_error
from settings.settings import DEBUG

def get_header():
      header = {'Connection': 'keep-alive', 'sec-ch-ua': '" Not A;Brand";v="99", "Chromium";v="101"', 'sec-ch-ua-mobile': '?0', 'User-Agent': 'Mozilla/5.0 (Mobile; rv:48.0; A405DL) Gecko/48.0 Firefox/48.0 KAIOS/2.5'}
      return header

def open_headers():
    try:
        header = {
            'User-Agent': 'Mozilla/5.0 (Mobile; rv:48.0; A405DL) Gecko/48.0 Firefox/48.0 KAIOS/2.5'}
        header['Referer'] = open("cookies/Referer.txt", "r").read()
    except IOError as e:
        if DEBUG:
            log_error(e)
        header = {
            'User-Agent': 'Mozilla/5.0 (Mobile; rv:48.0; A405DL) Gecko/48.0 Firefox/48.0 KAIOS/2.5'}
    return header

def save_Referer(page):
    with open("cookies/Referer.txt", "w") as f:
        f.write(str(page.url))
        f.close()
    return True