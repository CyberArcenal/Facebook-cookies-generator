import requests
#############################COLOR#############################
blue = "\033[1;96m"
white = "\033[1;97m"
green = "\033[1;92m"
red = "\033[1;91m"
yellow = "\033[1;93m"
line = ("\033[1;92m╔═"+57*"\033[1;92m═")
line2 = ("\033[1;92m║"+58*"\033[1;92m═")
############################LOGO###############################
logo = blue+"""▄▄▄             █           █
█▄▄ ▀▀█ █▀▀ ███ █▀█ █▀█ █▀█ █▄▀
█   ███ █▄▄ █▄▄ █▄█ █▄█ █▄█ █▀▄"""+white
###############################################################
session = requests.Session()
DEBUG = False
ACCOUNT = ""
