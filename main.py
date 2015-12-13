import sys
import getpass
import os
import re
import bz2

try:
    from bs4 import BeautifulSoup
except ImportError:
    print ("Install BeautifulSoup")
    sys.exit(1)

try:
    import requests
except ImportError:
    print ("Install requests module")
    sys.exit(1)


def first_time_login():
    name = raw_input("Enter your spoj username: ")
    password = getpass.getpass()
    with file('.passd.txt', 'w') as f:
        f.write(bz2.compress(name) + "\n" + bz2.compress(password))
    return name,password


def start_session(login_url, username, password):
    print ('Verifying..')
    with requests.Session() as session:
        payload = {
                'login_user' : username,
                'password' : password,
                'submit': 'login',
                }
        r = session.post(login_url, data = payload)

        html = r.text
        html.encode('utf-8')
        soup = BeautifulSoup(html, 'html.parser')
        for auth in soup.find_all('h3'):
            if (auth.get_text() == 'Authentication failed!'):
                print ('Authentication Failed!')
                print ('Enter login credentials again!')
                name,p = first_time_login()
                start_session(url, name, p)
                break
        else:
            r = session.get('http://www.spoj.com/myaccount/')
            html = str(r.text)
            soup = BeautifulSoup(html, 'html.parser')

            read_submitted_problems(soup)
            read_todo_problems(soup)

            read_from_user()

def login_credentials(login_url):
    if (os.path.isfile('.passd.txt')):
        f = open('.passd.txt','r')
        username,password = f.readlines()
        username = bz2.decompress(username)
        password = bz2.decompress(password)
        f.close()
    else:
        username,password = first_time_login()

    start_session(login_url, username, password)


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

def show_problems():
    star()

    print '\t\t1. Classical\n\
                2. Challenge\n\
                3. Partial\n\
                4. Tutorial\n\
                5. Riddle\n\
                6. Basics\n\
                7. Problem by tags\n\
                8. Back\n\
                9. Exit'

    choice = int(raw_input())
    options = { 1 : classical_problems,
                2 : challenge_problems,
                3 : partial_problems,
                4 : tutorial_problems,
                5 : riddle_problems,
                6 : basic_problems,
                7 : problem_by_tags,
                8 : read_from_user,
              }
    if (choice >= 1 and choice <=8):
        options[choice]()
    elif (choice != 9):
        print ('Wrong choice! Enter Again.')
        show_problems()

    star()

def classical_problems():
    url = 'http://www.spoj.com/problems/classical/'
    pass

def challenge_problems():
    url = 'http://www.spoj.com/problems/challenge/'
    pass

def partial_problems():
    url = 'http://www.spoj.com/problems/partial/'
    pass

def tutorial_problems():
    url = 'http://www.spoj.com/problems/tutorial/'
    pass

def riddle_problems():
    url = 'http://www.spoj.com/problems/riddle/'
    pass

def basic_problems():
    url = 'http://www.spoj.com/problems/basics/'
    pass

def problem_by_tags():
    url = 'http://www.spoj.com/problems/tags'
    pass

def submit_solution():
    pass

def read_from_user():
    star()

    print '\t\t1. Show problems\n\
                2. Submit solution\n\
                3. Show submitted problems by the user\n\
                4. Download all solutions to submitted problems by user\n\
                5. Exit'

    choice = int(raw_input())
    if (choice == 1):
        show_problems()
    elif (choice == 2):
        submit_solution()
    elif (choice != 5):
        print ('Wrong choice! Enter Again.')
        read_from_user()

def star():
    print
    print '*'*100
    print

def main():
    login_url = "http://www.spoj.com/login"
    login_credentials(login_url)


if __name__ == '__main__':
    main()
