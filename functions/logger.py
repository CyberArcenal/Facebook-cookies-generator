from settings.settings import blue, white, green,\
    red, yellow
import datetime

def log(msg):
    current_time = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    print(f"\033[1;92m║ {green}{current_time}: {msg}{white}")
    return


def log_error(msg):
    current_time = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    print(f"\033[1;92m║ {red}{current_time}: {msg}{white}")
    return