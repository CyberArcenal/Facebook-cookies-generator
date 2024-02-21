import json
import bs4
import sys
from requests import Response
from .logger import log, log_error
from settings.settings import DEBUG
from settings.settings import green, yellow
from typing import List

def find_input_fields(html):
    return bs4.BeautifulSoup(html, "html.parser", parse_only=bs4.SoupStrainer("input"))

def find_url(page):
    try:
        soup = bs4.BeautifulSoup(page, "html.parser")
        url = soup.find("form").get("action")
        return (f"https://m.facebook.com:443{url}")
    except AttributeError as e:
        log_error(e)
        # a = input(f"{yellow}Show error page?[y/n]")
        # if a == 'y':
        #     log_error(page)
        sys.exit()

def get_input_data(page):
    soup_data = find_input_fields(page.text)
    data = dict(
        (elem["name"], elem["value"])
        for elem in soup_data
        if elem.has_attr("value") and elem.has_attr("name")
    )
    return data

def create_form_2fa(page):
    action_url = find_url(page.text)
    data = get_input_data(page)
    data['submit[Continue]'] = "continue"
    if 'submit[logout-button-with-confirm]' in data:
        del data['submit[logout-button-with-confirm]']
    return action_url, data


def create_form(response:Response)->List:
    action_url = find_url(response.text)
    data = get_input_data(page=response)
    data["login"] = "Log in"
    if "sign_up" in data:
        del (data["sign_up"])
    return data, action_url

def get_page_title(page_text):
    try:
        s = bs4.BeautifulSoup(page_text, "html.parser")
        title = s.title.text.strip()
        return title
    except Exception as e:
        log_error(e)
        return "none"

def get_title_message(page):
    try:
        soup = bs4.BeautifulSoup(page.text, 'html.parser')
        title_div = soup.select_one('div#checkpoint_title')
        title_msg = title_div.get_text(strip=True)
    except Exception as e:
        if DEBUG:
            log_error(e)
        title_msg = None
    return title_msg

def get_title_dexcription(page):
    try:
        soup = bs4.BeautifulSoup(page.text, 'html.parser')
        div_element = soup.select_one('form.checkpoint div._50f4')
        text_div = div_element.select_one('div.y.z div')
        title_dexcription = text_div.get_text(strip=True)
    except Exception as e:
        if DEBUG:
            log_error(e)
        title_dexcription = None
    return title_dexcription

def print_page_title(page_text: str)->None:
      try:
            s = bs4.BeautifulSoup(page_text, "html.parser")
            title_text = s.title.text.strip()
            print(f"\033[1;92m║ {yellow}{title_text}")
      except Exception as e:
            #log_error(e)
            pass

def _print_page__(page_text: str, pritie: bool=False)->None:
    try:
        s = bs4.BeautifulSoup(page_text, "html.parser")
        
        if pritie:
                print(s.prettify())
        else:
                print(page_text)
    except Exception as e:
        #log_error(e)
        pass