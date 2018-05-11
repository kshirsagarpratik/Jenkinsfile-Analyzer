''' The first step is to find and retrieve Jenkinsfile(s) from various open source repositories. We decided to use GitHub's REST API for our application. We are trying to access a jenkinsfile's raw content so that we can append it to one text file that contains all the jenkinsfiles' contents. This process will streamline parsing and generating results of analyses later on.

We are using a Jupyter Notebook from Anaconda with Python 3.6, we use the following packages to start off with our task. '''

import requests # Helps working with HTTP requests such as GitHub API.
import os # For performing tasks on shell.
import subprocess # For performing tasks on shell.
import logging # For creating log files

'''Configure the log file'''
LOG_FILENAME = 'course_proj.log'
logging.basicConfig(
    filename = LOG_FILENAME,
    level = logging.DEBUG,
    format = '%(asctime)s %(levelname)s %(message)s',
    filemode = 'w'
)

'''GitHub REST API at work with the Python REQUESTS package.

We ran a query that gives us all the files whose names match the string "jenkinsfiles", following proper convention.'''

repositories = requests.get('https://api.github.com/search/code?q=pipeline+NOT+node+in:file+filename:jenkinsfile+?page=1&per_page=100', auth = ('kshirsagarpratik', 'Chinku95'))

''' Iteratively retrieving the raw text content of all the jenkinsfiles returned by the API call and appending to a single textfile called "Jenkinsfile."'''

print('Attempting to retrieve jenkinsfile(s) from various GitHub repositories through it\'s REST API...')
logging.info('Attempting to retrieve jenkinsfile(s) from various GitHub repositories through it\'s REST API...')

number = 1 # iteratively store jenkinsfiles locally.
try:
    for repo in repositories.json()['items']:
        print (repo['url'])
        logging.info (repo['url'])
        jenkinsfile = requests.get(repo['url'], auth = ('kshirsagarpratik', 'Chinku95')) # Authentication for GitHub
        print(jenkinsfile)
        logging.info(jenkinsfile)
        jenkinsfile_content = requests.get(jenkinsfile.json()['download_url'], auth = ('kshirsagarpratik', 'Chinku95'))
        file_pointer = open('Jenkinsfile' + str(number) + '.txt', 'a+')
        file_pointer.write(jenkinsfile_content.text)
        file_pointer.close()
        number = number + 1
except Exception as e:
    print('Error occured in retrieving jenkinsfile(s)')
    logging.error('Error occured in retrieving jenkinsfile(s)')

# We can output the various steps and stages into a json file. In the end we can see if we can count how may files have build, how many have tests and so on.