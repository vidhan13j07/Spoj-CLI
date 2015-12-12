import sys
import getpass

try:
    import requests
except ImportError:
    print "Install requests"
    sys.exit(1)

url = "http://www.spoj.com/login"
username = raw_input("Enter Spoj username: ")
password = getpass.getpass()

session = requests.session()

login_data = {
        'login_user' : username,
        'password' : password,
        'submit': 'login',
        }

r = session.post(url, data = login_data)
