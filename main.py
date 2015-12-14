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

if (sys.version_info > (3,0)):
    raw_input = input

def first_time_login():
    name = raw_input("Enter your spoj username: ")
    password = getpass.getpass()
    # When the user logins for the first time, his username and password gets stored in the file in encrypted format.
    compressed = bz2.compress((name + ',' + password).encode('utf-8'))
    with open('.passd.txt', 'wb') as f:
        f.write(compressed)
    return name,password


def start_session(login_url, username, password):
    print ('Verifying....')
    global session
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
        with open('.passd.txt','rb') as f:
            username,password = bz2.decompress(f.read()).decode('utf-8').split(',')
    else:
        username,password = first_time_login()

    start_session(login_url, username, password)

def read_submitted_problems(soup):
    tables = soup.find_all('table')

    global submitted_problems
    submitted_problems = []

    for row in tables[0].find_all('tr'):
        for col in row.find_all('a'):
            if (col.get_text()):
                submitted_problems.append((col.get_text(), col.get('href')))

def read_todo_problems(soup):
    tables = soup.find_all('table')

    global todo_problems
    todo_problems = []

    for row in tables[1].find_all('tr'):
        for col in row.find_all('a'):
            if (col.get_text()):
                todo_problems.append((col.get_text(), col.get('href')))

def show_problems():
    star()

    print ('\t\t1. Classical\n\
                2. Challenge\n\
                3. Partial\n\
                4. Tutorial\n\
                5. Riddle\n\
                6. Basics\n\
                7. Problem by tags\n\
                8. Back\n\
                9. Exit')

    choice = int(raw_input())

    star()

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

def classical_problems():
    url1 = url + '/problems/classical/'
    pass

def challenge_problems():
    url1 = url + '/problems/challenge/'
    pass

def partial_problems():
    url1 = url + '/problems/partial/'
    pass

def tutorial_problems():
    url1 = url + '/problems/tutorial/'
    pass

def riddle_problems():
    url1 = url + '/problems/riddle/'
    pass

def basic_problems():
    url1 = url + '/problems/basics/'
    pass

def problem_by_tags():
    tags_url = url + '/problems/tags'
    r = session.get(tags_url)
    html = str(r.text)
    soup = BeautifulSoup(html, 'html.parser')

    rows = soup.find('table').find('tbody').find_all('tr')

    tags = []   #tags is list of tuples in format (tag name, count of problems, tag link)

    for columns in rows:
        col = columns.find_all('td')
        cnt = int(col[1].get_text())
        if (cnt > 0):
            link = col[0].find('a')
            tags.append((link.get_text(), cnt, link.get('href')))

    print ('{:<40}||{:^50}||{:>40}\n\n'.format('INDEX', 'TAGS', 'PROBLEMS'))
    display2(tags)

def display(tup):
    for index,p in enumerate(tup):
        print ('{:<30}||{:>30}\n'.format(index+1, p[0]))
    star()

def display2(tup):
    for index,p in enumerate(tup):
        print ('{:<40}||{:^50}||{:>40}\n'.format(index+1 ,p[0] ,p[1]))
    star()

def submit_solution():
    pass

def read_from_user():
    star()

    print ('\t\t1. Show problems\n\
                2. Submit solution\n\
                3. Show submitted problems by the user\n\
                4. Show todo problems\n\
                5. Download all solutions to submitted problems by user\n\
                6. Exit')

    choice = int(raw_input())
    if (choice == 1):
        show_problems()
    elif (choice == 2):
        submit_solution()
    elif (choice == 3):
        star()
        print ('\n{:<30}||{:>30}\n'.format("INDEX", "PROBLEM"))
        display(submitted_problems)
    elif (choice == 4):
        star()
        print ('\n{:<30}{:>30}\n'.format("INDEX", "PROBLEM"))
        display(todo_problems)
    elif (choice != 6):
        print ('Wrong choice! Enter Again.')
        read_from_user()

def star():
    print ('\n' + '*'*150 + '\n')

def main():
    global url
    url = "http://www.spoj.com"
    login_url = "http://www.spoj.com/login"
    login_credentials(login_url)


if __name__ == '__main__':
    main()
