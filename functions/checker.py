from bs4 import BeautifulSoup
from requests import Response
from settings.settings import red, white, blue
from .logger import log, log_error
import sys

remember_browser_language = ["Tandaan ang Browser", "Remember browser"]
review_recent_login_language = ["Review Recent Login"]

def check(title: str, data: dict, page: Response):
      soup:BeautifulSoup = BeautifulSoup(page.text, 'html.parser')   
      if 'name_action_selected' not in data and 'submit[This was me]' not in data and 'submit[Continue]' not in data:
            try:data['submit[Continue]'] = 'Continue'
            except:pass
            
      if any(title.lower() in word.lower() for word in remember_browser_language) or "save_device" in page.text:
            data=remember_browser(data=data, soup=soup)
            
      elif 'submit[This was me]' in page.text or any(title.lower() in word.lower() for word in review_recent_login_language):
            data = review_recent_login(data=data, soup=soup)
            
      elif title == "Enter login code to continue" or "approvals_code" in page.text:
            data = two_factor(data=data, soup=soup)
            
      else:
            log_error(f"A new title has come please add this {white}{title} in check function.")
            sys.exit()
      return data

def two_factor(data: dict, soup: BeautifulSoup) -> dict:
      while True:
            code = input(f"{blue}input 6 digit code: {white}")
            if len(str(code)) > 5:
                break
            else:
                print(f"{red}Please enter login code to continue.{white}")
      data['approvals_code'] = code
      return data

def remember_browser(data: dict, soup: BeautifulSoup) -> dict:
      save_device_button = soup.find('input', {'name': 'name_action_selected'})
      continue_button = soup.find('input', {'name': 'submit[Continue]'})
      if 'name_action_selected' not in data and save_device_button:
            data['name_action_selected'] = "save_device"
      if 'submit[Continue]' not in data and continue_button:
            data['submit[Continue]'] = 'Continue'
      return data
      
def review_recent_login(data: dict, soup: BeautifulSoup)-> dict:
      continue_button = soup.find('input', {'name': 'submit[Continue]'})
      this_was_me_button = soup.find('input', {'name': 'submit[This was me]'})
      if 'submit[This was me]' not in data and this_was_me_button:  
            data['submit[This was me]'] = "This was me"
      if 'submit[Continue]' not in data and continue_button:
            data['submit[Continue]'] = 'Continue'
      if 'submit[logout-button-with-confirm]' in data:
            del data['submit[logout-button-with-confirm]']
      try:del data["submit[This wasn't me]"]
      except:pass
      return data