import sys
import getpass
import os
import re

try:
    from bs4 import BeautifulSoup
except ImportError:
    print "Install BeautifulSoup"
    sys.exit(1)

try:
    import requests
except ImportError:
    print "Install requests module"
    sys.exit(1)


def first_time_login():
    name = raw_input("Enter your spoj username: ")
    password = getpass.getpass()
    with file('.passd.txt', 'w') as f:
        f.write(name + "\n" + password)
    return name,password


def start_session(url, username, password):
    print ('Verifying..')
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
            r = session.get('http://www.spoj.com/myaccount/')
            html = str(r.text)
            soup = BeautifulSoup(html, 'html.parser')

            read_submitted_problems(soup)
            read_todo_problems(soup)


def credentials(url):
    if (os.path.isfile('.passd.txt')):
        f = open('.passd.txt','r')
        username,password = f.readlines()
        username = username.strip()
        password = password.strip()
    else:
        username,password = first_time_login()

    start_session(url, username, password)


def read_submitted_problems(soup):
    tables = soup.find_all('table')

    global submitted_problems, submitted_problem_links
    submitted_problems,submitted_problem_links = [],[]

    for row in tables[0].find_all('tr'):
        for col in row.find_all('a'):
            submitted_problems.append(col.get_text())
            submitted_problem_links.append(col.get('href'))


def read_todo_problems(soup):
    tables = soup.find_all('table')

    global todo_problems, todo_problem_links
    todo_problems,todo_problem_links = [],[]

    for row in tables[1].find_all('tr'):
        for col in row.find_all('a'):
            todo_problems.append(col.get_text())
            todo_problem_links.append(col.get('href'))


def main():
    url = "http://www.spoj.com/login"
    credentials(url)


if __name__ == '__main__':
    main()
