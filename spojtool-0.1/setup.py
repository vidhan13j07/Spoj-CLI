from setuptools import setup

setup ( name = 'spojtool',
        version = '1.0',
        description = 'View and submit solutions to the www.spoj.com using commandline',
        url = 'https://github.com/vidhan13j07/Spoj-toolkit',
        author = 'Vidhan Jain',
        author_email = 'vidhanj1307@gmail.com',
        license = 'MIT',
        packages = ['spojtool'],
        scripts = ['bin/spojtool'],
        install_requires = [ 'BeautifulSoup4' ],
        zip_safe= False)
