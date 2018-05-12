
import requests # Helps working with HTTP requests such as GitHub API.
import os # For performing tasks on shell.
import logging # For creating log files
import re

'''Configure the log file'''
LOG_FILENAME = 'course_proj.log'
logging.basicConfig(
    filename = LOG_FILENAME,
    level = logging.DEBUG,
    format = '%(asctime)s %(levelname)s %(message)s',
    filemode = 'w'
)

def jenkinsfile_query(keyword, page_number): # to retrieve list of jenkinsfiles and their URLs.
    # print('Attempting to retrieve jenkinsfile(s) from various GitHub repositories through it\'s REST API...')
    logging.info('Attempting to retrieve jenkinsfile(s) from various GitHub repositories through it\'s REST API... Keyword = ' + keyword + ' Page Number = ' + str(page_number))
    try:
        repositories = requests.get('https://api.github.com/search/code?q=' + keyword + '+in:file+filename:jenkinsfile+?page=' + str(page_number) + '&per_page=100', auth = ('kshirsagarpratik', 'Chinku95'))
        return repositories
    except Exception as e:
        print('Error while hitting GitHub REST API for keyword = ' + keyword + ' and page number = ' + str(page_number))
        logging.error('Error while hitting GitHub REST API for keyword = ' + keyword + ' and page number = ' + str(page_number))

def contents_query(repo_url): # to retrieve contents of specific Jenkinsfile.
    logging.info('Attempting to retrieve contents of Jenkinsfile at URL = ' + repo_url)
    try:
        jenkinsfile = requests.get(repo_url, auth = ('kshirsagarpratik', 'Chinku95')) # Authentication for GitHub
        print(jenkinsfile)
        logging.info(jenkinsfile)
        jenkinsfile_content = requests.get(jenkinsfile.json()['download_url'], auth = ('kshirsagarpratik', 'Chinku95'))
        return jenkinsfile_content
    except Exception as e:
        print('Error while retrieve contents of Jenkinsfile at URL = ' + repo_url)
        logging.error('Error while retrieve contents of Jenkinsfile at URL = ' + repo_url)

def readyFile(jenkinsfile_content): # to create the jenkinsfile parseable in txt format.
    logging.info('Attempting to create a txt jenkinsfile for given Jenkinsfile')
    try:
        file_pointer = open('Jenkinsfile.txt', 'w+')
        file_pointer.write(jenkinsfile_content.text)
        file_pointer.close()
        file_pointer = open('Jenkinsfile.txt', 'r')
        file_content = file_pointer.readlines()
        file_pointer.close()
        os.remove('Jenkinsfile.txt') # delete txt file after use.
        return file_content
    except Exception as e:
        print('Error while storing content of Jenkinsfile in txt.')
        logging.error('Error while storing content of Jenkinsfile in txt.')

# def exception_handling(): # try to find the % of jenkinsfiles that exhibit exception handling.
#     number = 1 # to iterate over the jenkinsfiles.
#     try_occurences = 0 # measure the occurence of exception handling in jenkinsfiles.
#     for page_number in range(1,10): # We are aiming to retrieve ~1000 Jenkinsfiles that are available on GitHub, as every page has max 100 results.
#         repositories = jenkinsfile_query('try', page_number)
#         try:
#
#             for repo in repositories.json()['items']:
#                 print(repo['url'])
#                 logging.info(repo['url'])
#                 jenkinsfile_content = contents_query(repo['url'])
#                 file_content = readyFile(jenkinsfile_content)
#                 for line in file_content:
#                     if re.search(r'\btry\b\s*\{', line): # using regex to find the occurence of a 'try' block
#                         try_occurences = try_occurences + 1 # increment count of total jenkinsfiles that have 'try' blocks.
#                         break
#                 number = number + 1
#
#         except Exception as e:
#             print('Error occurred in finding out which files have exception handling')
#             logging.error('Error occurred while finding out the jenkinsfiles that have exception handling')
#
#     print('We found error handling mechanism present in ' + str(try_occurences) + ' Jenkinsfiles')
#     logging.info('We found error handling mechanism present in ' + str(try_occurences) + ' Jenkinsfiles')
#     print('We were able to retrieve ' + str(number - 1) + ' such Jenkinsfiles.')
#     logging.info('We were able to retrieve ' + str(number - 1) + ' such Jenkinsfiles.')
#
#     percent_exception_handling = try_occurences / (number - 1)
#     return  percent_exception_handling # return as a decimal fraction.
#
# # eh = exception_handling()
# # print(eh)
#
def docker():
    number = 1
    count_docker = 0
    count_dockerfile = 0

    # \bdocker\b\s*\{
    # \bdockerfile\b\s*\{

    for page_number in range(1,10): # We are aiming to retrieve ~1000 Jenkinsfiles that are available on GitHub, as every page has max 100 results.
        repositories = jenkinsfile_query('docker', page_number)
        try:

            for repo in repositories.json()['items']:
                print(repo['url'])
                logging.info(repo['url'])
                jenkinsfile_content = contents_query(repo['url'])
                file_content = readyFile(jenkinsfile_content)

                for line in file_content:
                    if re.search(r'\bdocker\b\s*\{', line): # using regex to find the occurence of keyword 'docker'.
                        count_docker = count_docker + 1 # increment count of total jenkinsfiles that use 'docker' in some way.

                    if re.search(r'\bdockerfile\b\s*\{', line): # using regex to find the occurence of keyword 'dockerfile'.
                        count_dockerfile = count_dockerfile + 1 # increment count of total jenkinsfiles that use 'dockerfile' in any way.

                number = number + 1

        except Exception as e:
            print('Error occurred in finding out what % of jenkins pipelines use docker.')
            logging.error('Error occurred while finding out what % of jenkins pipelines use docker.')

    ''' Generate percentage of occurrences, actually a fraction'''
    percent_docker = count_docker / (number - 1)
    percent_dockerfile = count_dockerfile / (number - 1)
    percent_total = percent_docker + percent_dockerfile

    docker_dictionary = {'docker' : percent_docker, 'dockerfile' : percent_dockerfile, 'total' : percent_total}
    return docker_dictionary

docker_stats = docker()
print(docker_stats)


# def popular_agent(): # Find the most popular kind of agent in jenkinsfiles.
#
#     none_count = 0
#     node_count = 0
#     any_count = 0
#     label_count = 0
#     docker_count = 0
#     dockerfile_count = 0
#     number = 1
#
#     for page_number in range(1,10): # We are aiming to retrieve ~1000 Jenkinsfiles that are available on GitHub, as every page has max 100 results.
#         repositories = jenkinsfile_query('agent', page_number)
#         try:
#
#             for repo in repositories.json()['items']:
#                 print(repo['url'])
#                 logging.info(repo['url'])
#                 jenkinsfile_content = contents_query(repo['url'])
#                 file_content = readyFile(jenkinsfile_content)
#
#                 for line in file_content:
#
#                     if re.search(r'\bagent\b\s*\bnone\b', line): # using regex to find the occurence of an agent of type 'none'.
#                         none_count = none_count + 1 # increment count of total jenkinsfiles that have an agent of type 'none'.
#
#                     if re.search(r'\bagent\b\s*\bany\b', line): # using regex to find the occurence of an agent of type 'any'.
#                         any_count = any_count + 1 # increment count of total jenkinsfiles that have an agent of type 'any'.
#
#                     if re.search(r'\bagent\b\s*\{\s*\blabel\b', line): # using regex to find the occurence of an agent of type 'label'.
#                         label_count = label_count + 1 # increment count of total jenkinsfiles that have an agent of type 'label'.
#
#                     if re.search(r'\bagent\b\s*\{\s*\bnode\b', line): # using regex to find the occurence of an agent of type 'node'.
#                         node_count = node_count + 1 # increment count of total jenkinsfiles that have an agent of type 'node'.
#
#                     if re.search(r'\bagent\b\s*\{\s*\bdocker\b', line): # using regex to find the occurence of an agent of type 'docker'.
#                         docker_count = docker_count + 1 # increment count of total jenkinsfiles that have an agent of type 'docker'.
#
#                     if re.search(r'\bagent\b\s*\{\s*\bdockerfile\b', line): # using regex to find the occurence of an agent of type 'dockerfile'.
#                         dockerfile_count = dockerfile_count + 1 # increment count of total jenkinsfiles that have an agent of type 'dockerfile'.
#
#
#                 number = number + 1
#
#         except Exception as e:
#             print('Error occurred in finding out which kinds of agent are the most popular.')
#             logging.error('Error occurred while finding out the most popular kind of agent.')
#
#     ''' Generate percentage of occurrences, actually a fraction'''
#     percent_any = any_count / (number - 1)
#     percent_node = node_count / (number - 1)
#     percent_none = none_count / (number - 1)
#     percent_label = label_count / (number - 1)
#     percent_docker = docker_count / (number - 1)
#     percent_dockerfile = dockerfile_count / (number - 1)
#
#     agent_dictionary = {'any' : percent_any, 'node' : percent_node, 'none' : percent_none, 'label' : percent_label, 'docker' : percent_docker, 'dockerfile' : percent_dockerfile}
#     return agent_dictionary
#
# agent = popular_agent()
# print(agent)

# def global_agent():

# most used docker image
