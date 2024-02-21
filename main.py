import json
import os
import sys
import re
import time
import requests
import random
import datetime
from icecream import ic
import bs4
import threading
from settings.settings import blue, white, green, \
    red, yellow, line, line2, logo, DEBUG, \
    session, ACCOUNT
from functions.checker import check
from settings.version import __check__, __clr__
from settings.br import get_header
from functions.ck import save_cookies_in_the_list, display_cookies, \
    save_cookies, clean_cookie, clear_cookies, clear_logs, \
    open_cookie_list, open_cookies
from functions.logger import log, log_error
from browser.browser import browser
from functions.soup import find_input_fields, find_url, \
    get_input_data, create_form, create_form_2fa, \
    get_page_title, get_title_dexcription, get_title_message

################ settings###################
__check__()
clr = __clr__()
header = get_header()
RUN = True


def check_approval(data):
    url = "https://m.facebook.com/login/approvals/approved_machine_check/"
    page = browser(url=url, data=data)

    try:
        # Try to parse the JSON-like response body
        # Remove the prefix "for (;;);"
        json_data = page.text.replace("for (;;);", "")

        # Parse the JSON-like response body
        response_json = json.loads(json_data)
        # Access specific values from the response
        is_approved = True if 'True' in str(response_json) else False
        # Print the values
        if DEBUG:
            print(f"is_approved: {is_approved}")

        if is_approved:
            return True
        else:
            return False
    except json.decoder.JSONDecodeError as e:
        # Handle the case where the response is not valid JSON
        if DEBUG:
            print(f"JSON Decode Error: {e}")
        return False


def pick():
    user_input = input("\033[1;92m╚═════\033[1;91m>>>\033[1;97m ")
    return str(user_input)


class Facebook:
    def __init__(self, account: str, password: str) -> None:
        clean_cookie()
        self.account = account
        self.password = password

    def handle_checkpoint(self):
        # Code to handle checkpoint scenarios
        print('\n\033[1;93m Your Account is in Checkpoint:')
        clean_cookie()
        sys.exit()
        # Additional actions if needed

    def handle_unknown_response(self):
        print(f"{red}\t\tInvalid response, maybe the script is not updated.\n\t\tPlease report it to the developer.{white}")
        clean_cookie()
        sys.exit()

    def Continue(self):
        global RUN
        page: requests.Response = self.page
        while RUN:
            action_url = find_url(page.text)
            data = get_input_data(page)
            title = get_page_title(page_text=page.text)
            data = check(title=title, data=data, page=page)
            page: requests.Response = browser(
                url=action_url, data=data, redirect=False, print_title=True)
            if "c_user" in page.cookies.get_dict():
                print(
                    f"\033[1;92m║ {green}Facebook account login succesfully.")
                print(65 * '\033[1;92m=')
                RUN=False
                display_cookies(account_name=ACCOUNT)
                input()
                main()
            time.sleep(4)

    def bg_check_approval(self, data, action_url):
        global RUN
        data['approvals_code'] = ""
        while RUN:
            if check_approval(data=data):
                page: requests.Response = browser(
                    url=action_url, data=data, redirect=False)
                if "c_user" in page.cookies.get_dict():
                    print(f"{green}Facebook account approve login succesfully.")
                    print(65 * '\033[1;92m=')
                    RUN=False
                    display_cookies(account_name=ACCOUNT)
                    input()
                    main()
            time.sleep(7)
        return

    def two_factor_mode(self):
        global RUN
        action_url, data = create_form_2fa(self.page)
        print(f"\033[1;92m║ {green}Enter login code to continue{white}")
        print(
            f"\033[1;92m║ {green}You can approve login by other device.{white}")
        while RUN:
            code = input(f"\033[1;92m║ {blue}input 6 digit code: {white}")
            if len(str(code)) > 5:
                break
            else:
                print(
                    f"\033[1;92m║ {red}Please enter login code to continue.{white}")
        if RUN == False:
            input()
            main()
        data['approvals_code'] = code
        self.page: requests.Response = browser(url=action_url, data=data)
        title = get_page_title(page_text=self.page.text)
        list_error = ["too many login attempts", "too many", "attemps"]
        if any(word.lower() in title.lower() for word in list_error):
            print(f"\033[1;92m║ {red}{title}")
            input(f"{yellow}Exit:")
            main()
        self.Continue()

    def login(self):
        global RUN
        list_error = ["log into facebook", "log into"]
        list_error_password = ["reset your password", "reset"]
        #### LOAD LOGIN PAGE######
        URL = 'https://m.facebook.com'
        page = browser(URL)
        data, url = create_form(response=page)
        while True:
            ## put email/pass in data dictionary##
            data['email'] = self.account
            data['pass'] = self.password
            # requests login
            self.page: requests.Response = browser(url, data=data)
            # getting page title
            title = get_page_title(page_text=self.page.text)
            print("\033[1;92m║ "+yellow+title)
            if any(word.lower() in title.lower() for word in list_error):
                print(
                    f"\033[1;92m║ {red}Maybe your password is not match or typo, \n\033[1;92m║ please input your correct password.")
                print("\033[1;92m║ email/number/username/etc:")
                self.account = pick()
                print("\033[1;92m║ \033[1;92mYour Password:")
                self.password = pick()
            elif any(word.lower() in title.lower() for word in list_error_password):
                print(
                    f"\033[1;92m║ {red}Maybe your password is not match or typo, \n\033[1;92m║ {red}please input your correct password.")
                print("\033[1;92m║ email/number/username/etc:")
                self.account = pick()
                print("\033[1;92m║ \033[1;92mYour Password:")
                self.password = pick()
            else:
                break
        if "c_user" in self.page.cookies.get_dict():
            print(f"\033[1;92m║ {green}Facebook account login succesfully.")
            print(65 * '\033[1;92m=')
            RUN=False
            display_cookies(account_name=ACCOUNT)
            input()
            main()

        if "checkpoint" in self.page.url and "approvals_code" in self.page.text:
            print('\033[1;92m║ \033[1;93m2FA auth required:')
            action_url, data = create_form_2fa(self.page)
            # Corrected line
            thread = threading.Thread(
                target=self.bg_check_approval, args=(data, action_url))
            thread1 = threading.Thread(target=self.two_factor_mode)
            thread1.start()
            thread.start()
        elif title == "Review Recent Login" or 'submit[Continue]' in self.page.text:
            self.Continue()
        elif "checkpoint_title" in self.page.text:
            self.handle_checkpoint()

        else:
            log_error(f"A new title has come please add this {white}{title} in check function.")
            self.handle_unknown_response()


def display_cookiefile(cookies):
    os.system(clr)
    print(logo)
    print(line)
    print("\033[1;92m║")
    ic(cookies)
    print("\033[1;92m║")
    print(line2)
    print(f"\n{cookies}")
    input(f"{yellow}Exit:")
    View_Cookies()


def View_Cookies():
    os.system(clr)
    print(logo)
    print(line)
    cookie_list = open_cookie_list()
    for i in range(len(cookie_list['cookies_list'])):
        to_display = cookie_list["cookies_list"][i]
        print(
            f"\033[1;92m║ {white}{str(i)}. \033[1;92mAccount: {to_display['account']}")
        print(
            f"\033[1;92m║ \033[1;92mDate Logged: {to_display['date_logged']}")
        print(line2)
    try:
        a = pick()
        if a == "":
            main()
        display_cookiefile(cookie_list["cookies_list"][int(a)]["cookies"])
    except Exception as e:
        log_error(e)
        input()
        View_Cookies()


def Generate_Cookies():
    global ACCOUNT, RUN
    os.system(clr)
    print(logo)
    print(line)
    print("\033[1;92m║ email/number/username/etc:")
    user = pick()
    print("\033[1;92m║ \033[1;92mYour Password:")
    userpass = pick()
    cookies = open_cookies()
    if "c_user" in cookies:
        clear_cookies()
    clear_logs()
    ACCOUNT = user
    login = Facebook(user, userpass)
    login.login()


def main():
    global RUN
    RUN = True
    os.system(clr)
    print(logo)
    print(line)
    print("\033[1;92m║ \033[1;91m1. \033[1;94m—> \033[1;92mLogin Generate Cookies")
    print("\033[1;92m║ \033[1;91m2. \033[1;94m—> \033[1;92mView Cookies")
    print("\033[1;92m║ \033[1;91m3. \033[1;94m—> \033[1;92mUpdate")
    print("\033[1;92m║ \033[1;91m0. \033[1;94m—> \033[1;93mExit")
    home_pick()


def home_pick():
    p = pick()
    if p == "1":
        Generate_Cookies()
        return
    if p == "2":
        View_Cookies()
        return
    elif p == "3":
        os.system("git pull")
        os.system("python3 main.py")

    elif p == "0":
        sys.exit()
    else:
        print("\033[1;92m║ \033[1;91minvalid input")
        home_pick()


if __name__ == "__main__":
    main()
