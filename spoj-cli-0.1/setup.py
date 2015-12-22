from setuptools import setup

setup ( name = 'spoj-cli',
        version = '1.1',
        description = 'View and submit solutions to the www.spoj.com using commandline',
        url = 'https://github.com/vidhan13j07/Spoj-toolkit',
        author = 'Vidhan Jain',
        author_email = 'vidhanj1307@gmail.com',
        license = 'MIT',
        packages = ['spoj-cli'],
        scripts = ['bin/spoj-cli'],
        install_requires = [ 'BeautifulSoup4', 'requests'],
        zip_safe= False)
