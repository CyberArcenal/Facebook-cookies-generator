import sys, os
from .settings import green, blue
def __check__():
      if sys.version_info[0] != 3:
            os.system('clear')
            print(logo)
            print(blue+65 * '\033[1;92m=')
            print(green+'''\t\tREQUIRED PYTHON 3.x\n\t\tinstall and try: python3 main.py\n''')
            print(blue+65 * '\033[1;92m=')
            sys.exit()
def __clr__():
      if sys.platform == "linux" or sys.platform == "linux2":
            clr = "clear"
      elif sys.platform == "win32" or sys.platform == "cygwin" or sys.platform == "msys":
            clr = "cls"
      return clr