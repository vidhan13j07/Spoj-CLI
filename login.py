import sys
import getpass
import os
import re
from bs4 import BeautifulSoup

try:
    import requests
except ImportError:
    print "Install requests"
    sys.exit(1)

def first_time_login():
    name = raw_input("Enter your spoj username: ")
    password = getpass.getpass()
    with file('passd.txt', 'w') as f:
        f.write(name + "\n" + password)
    return name,password

def start_session(url, username, password):
    print ('Verifing..')
    with requests.Session() as session:
        payload = {
            'login_user' : username,
            'password' : password,
            'submit': 'login',
        }
        r = session.post(url, data = payload)

        html = r.text
        html.encode('utf-8')
        soup = BeautifulSoup(html, 'html.parser')
        for auth in soup.find_all('h3'):
            if (auth.get_text() == 'Authentication failed!'):
                print ('Authentication Failed!')
                print ('Enter login credentials!')
                name,p = first_time_login()
                start_session(url, name, p)
                break
        else:
            print ('Authentication Passed!')


def credentials(url):
    if (os.path.isfile('passd.txt')):
        f = open('passd.txt','r')
        username,password = f.readlines()
        username = username.strip()
        password = password.strip()
    else:
        username,password = first_time_login()

    start_session(url, username, password)

def main():
    url = "http://www.spoj.com/login"
    credentials(url)


if __name__ == '__main__':
    main()
