import requests # Helps working with HTTP requests such as GitHub API.
import os # For performing tasks on shell.
import logging # For creating log files
import re
from collections import defaultdict
import math


def jenkinsfile_query(keyword, page_number): # to retrieve list of jenkinsfiles and their URLs.
    # print('Attempting to retrieve jenkinsfile(s) from various GitHub repositories through it\'s REST API...')
    logging.info('Attempting to retrieve jenkinsfile(s) from various GitHub repositories through it\'s REST API... Keyword = ' + keyword + ' Page Number = ' + str(page_number))
    try:
        repositories = requests.get('https://api.github.com/search/code?q=' + keyword + '+in:file+filename:jenkinsfile+?page=' + str(page_number) + '&per_page=100', auth = ('sphalt', 'outlook<3Traveller'))
        return repositories
    except Exception as e:
        print('Error while hitting GitHub REST API for keyword = ' + keyword + ' and page number = ' + str(page_number))
        logging.error('Error while hitting GitHub REST API for keyword = ' + keyword + ' and page number = ' + str(page_number))


def contents_query(repo_url): # to retrieve contents of specific Jenkinsfile.
    logging.info('Attempting to retrieve contents of Jenkinsfile at URL = ' + repo_url)
    try:
        jenkinsfile = requests.get(repo_url, auth = ('sphalt', 'outlook<3Traveller')) # Authentication for GitHub
        print(jenkinsfile)
        logging.info(jenkinsfile)
        jenkinsfile_content = requests.get(jenkinsfile.json()['download_url'], auth = ('sphalt', 'outlook<3Traveller'))
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


def exception_handling(): # try to find the % of jenkinsfiles that exhibit exception handling.
    logging.info('Analyzing Jenkinsfiles for exception handling')
    number = 1 # to iterate over the jenkinsfiles.
    try_occurences = 0 # measure the occurence of exception handling in jenkinsfiles.
    for page_number in range(1,10): # We are aiming to retrieve ~1000 Jenkinsfiles that are available on GitHub, as every page has max 100 results.
        repositories = jenkinsfile_query('try', page_number)
        try:

            for repo in repositories.json()['items']:
                print(repo['url'])
                logging.info(repo['url'])
                jenkinsfile_content = contents_query(repo['url'])
                file_content = readyFile(jenkinsfile_content)
                for line in file_content:
                    if re.search(r'\btry\b\s*\{', line): # using regex to find the occurence of a 'try' block
                        try_occurences = try_occurences + 1 # increment count of total jenkinsfiles that have 'try' blocks.
                        break
                number = number + 1

        except Exception as e:
            print('Error occurred in finding out which files have exception handling')
            logging.error('Error occurred while finding out the jenkinsfiles that have exception handling')
            logging.error(e)

    print('We found error handling mechanism present in ' + str(try_occurences) + ' Jenkinsfiles')
    logging.info('We found error handling mechanism present in ' + str(try_occurences) + ' Jenkinsfiles')
    print('We were able to retrieve ' + str(number - 1) + ' such Jenkinsfiles.')
    logging.info('We were able to retrieve ' + str(number - 1) + ' such Jenkinsfiles.')

    percent_exception_handling = try_occurences / (number - 1)
    result = {'percent_exception_handling': percent_exception_handling,
              'files_with_exception_handling': try_occurences,
              'total_files': number - 1}
    return  result # return as a decimal fraction.


def docker():
    logging.info('Analyzing Jenkinsfiles...')
    number = 1
    count_docker = 0
    count_dockerfile = 0

    # \bdocker\b\s*\{
    # \bdockerfile\b\s*\{

    for page_number in range(1, 10): # We are aiming to retrieve ~1000 Jenkinsfiles that are available on GitHub, as every page has max 100 results.
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
            logging.error(e)

    ''' Generate percentage of occurrences, actually a fraction'''
    try:
        percent_docker = count_docker / (number - 1)
        percent_dockerfile = count_dockerfile / (number - 1)
        percent_total = percent_docker + percent_dockerfile

        docker_dictionary = {'docker' : percent_docker, 'dockerfile' : percent_dockerfile, 'total' : percent_total}
    except Exception as e:
        logging.error(e)
        docker_dictionary = {}

    return docker_dictionary


def popular_agent(): # Find the most popular kind of agent in jenkinsfiles.
    logging.info('Analyzing Jenkinsfiles for agent used')
    none_count = 0
    node_count = 0
    any_count = 0
    label_count = 0
    docker_count = 0
    dockerfile_count = 0
    number = 1

    for page_number in range(1,10): # We are aiming to retrieve ~1000 Jenkinsfiles that are available on GitHub, as every page has max 100 results.
        repositories = jenkinsfile_query('agent', page_number)
        try:

            for repo in repositories.json()['items']:
                print(repo['url'])
                logging.info(repo['url'])
                jenkinsfile_content = contents_query(repo['url'])
                file_content = readyFile(jenkinsfile_content)

                for line in file_content:

                    if re.search(r'\bagent\b\s*\bnone\b', line): # using regex to find the occurence of an agent of type 'none'.
                        none_count = none_count + 1 # increment count of total jenkinsfiles that have an agent of type 'none'.

                    if re.search(r'\bagent\b\s*\bany\b', line): # using regex to find the occurence of an agent of type 'any'.
                        any_count = any_count + 1 # increment count of total jenkinsfiles that have an agent of type 'any'.

                    if re.search(r'\bagent\b\s*\{\s*\blabel\b', line): # using regex to find the occurence of an agent of type 'label'.
                        label_count = label_count + 1 # increment count of total jenkinsfiles that have an agent of type 'label'.

                    if re.search(r'\bagent\b\s*\{\s*\bnode\b', line): # using regex to find the occurence of an agent of type 'node'.
                        node_count = node_count + 1 # increment count of total jenkinsfiles that have an agent of type 'node'.

                    if re.search(r'\bagent\b\s*\{\s*\bdocker\b', line): # using regex to find the occurence of an agent of type 'docker'.
                        docker_count = docker_count + 1 # increment count of total jenkinsfiles that have an agent of type 'docker'.

                    if re.search(r'\bagent\b\s*\{\s*\bdockerfile\b', line): # using regex to find the occurence of an agent of type 'dockerfile'.
                        dockerfile_count = dockerfile_count + 1 # increment count of total jenkinsfiles that have an agent of type 'dockerfile'.


                number = number + 1

        except Exception as e:
            print('Error occurred in finding out which kinds of agent are the most popular.')
            logging.error('Error occurred while finding out the most popular kind of agent.')
            logging.error(e)

    ''' Generate percentage of occurrences, actually a fraction'''
    try:
        percent_any = any_count / (number - 1)
        percent_node = node_count / (number - 1)
        percent_none = none_count / (number - 1)
        percent_label = label_count / (number - 1)
        percent_docker = docker_count / (number - 1)
        percent_dockerfile = dockerfile_count / (number - 1)

        agent_dictionary = {'any' : percent_any, 'node' : percent_node, 'none' : percent_none, 'label' : percent_label, 'docker' : percent_docker, 'dockerfile' : percent_dockerfile}
    except Exception as e:
        logging.error(e)
        agent_dictionary = {}

    return agent_dictionary


def global_agent(): # each stage needs it's own agent, global agent does not exist.

    agent = popular_agent()
    print(agent['none'])
    return agent['none']


def get_post_cond_stats():
    logging.info('Analyzing Jenkinsfiles for popular post conditions')
    post_block = defaultdict(int)
    post_conditions = []
    for page_number in range(1, 10):
        try:
            repositories = jenkinsfile_query('post', page_number)
            for repo in repositories.json()['items']:

                print(repo['url'])
                jenkinsfile_content = contents_query(repo['url'])
                file_content = readyFile(jenkinsfile_content)
                post_cond = {'url': repo['url'], 'post_conditions': []}
                for line in file_content:
                    # using regex to find the occurrence of any of the post conditions out of
                    # always, changed, fixed, regression, aborted, failure, success, unstable, and cleanup
                    if re.search(r'\balways\b\s*\{', line):
                        post_block['always'] += 1
                        post_cond['post_conditions'].append('always')
                    elif re.search(r'\bsuccess\b\s*\{', line):
                        post_block['success'] += 1
                        post_cond['post_conditions'].append('success')
                    elif re.search(r'\bfailure\b\s*\{', line):
                        post_block['failure'] += 1
                        post_cond['post_conditions'].append('failure')
                    elif re.search(r'\bchanged\b\s*\{', line):
                        post_block['changed'] += 1
                        post_cond['post_conditions'].append('changed')
                    elif re.search(r'\bfixed\b\s*\{', line):
                        post_block['fixed'] += 1
                        post_cond['post_conditions'].append('fixed')
                    elif re.search(r'\bregression\b\s*\{', line):
                        post_block['regression'] += 1
                        post_cond['post_conditions'].append('regression')
                    elif re.search(r'\baborted\b\s*\{', line):
                        post_block['aborted'] += 1
                        post_cond['post_conditions'].append('aborted')
                    elif re.search(r'\bunstable\b\s*\{', line):
                        post_block['unstable'] += 1
                        post_cond['post_conditions'].append('unstable')
                    elif re.search(r'\bcleanup\b\s*\{', line):
                        post_block['cleanup'] += 1
                        post_cond['post_conditions'].append('cleanup')

                # add the name of the post condition found to the list of post conditions for the jenkinsfile
                post_conditions.append(post_cond)

        except Exception as e:
            print(e)
            logging.error(e)

    try:
        min_value = min(post_block.values())
        max_value = max(post_block.values())
        min_result = [(key, value) for key, value in post_block.items() if value == min_value]
        max_result = [(key, value) for key, value in post_block.items() if value == max_value]

        max_dict_list = []
        for key in max_result:
            max_dict_list.append({'post_condition': key[0], 'count': key[1]})

        min_dict_list = []
        for key in min_result:
            min_dict_list.append({'post_condition': key[0], 'count': key[1]})

        result = {'most_frequent': max_dict_list,
                  'least_frequent': min_dict_list,
                  'post_conditions': post_conditions,
                  'all_post_conditions': post_block}
    except Exception as e:
        logging.error(e)
        result = {}

    return result


def get_pipeline_stage_stats():
    logging.info('Analyzing Jenkinsfiles for popular operations')
    stages = defaultdict(int)
    stageCountAll = list()
    stagesPerFile = list()
    for page_number in range(1, 10):
        try:
            repositories = jenkinsfile_query('stages', page_number)
            for repo in repositories.json()['items']:

                print(repo['url'])
                jenkinsfile_content = contents_query(repo['url'])
                file_content = readyFile(jenkinsfile_content)
                stagecount = 0
                stagesDict = {'url': repo['url'], 'stages': []}
                for line in file_content:
                    m = re.search(r"""\bstage\b\s*\((["'])(?:(?=(\\?))\2.)*?\1\)""", line)
                    if m:
                        stagestr = m.group(0).replace("stage('", "").replace("')", '')
                        stages[stagestr] += 1
                        stagecount += 1
                        stagesDict['stages'].append(stagestr)

                stageCountAll.append(stagecount)
                stagesPerFile.append(stagesDict)
        except Exception as e:
            print(e)

    try:
        max_stages = max(stages.keys(), key=(lambda k: stages[k]))
        min_stages = min(stages.keys(), key=(lambda k: stages[k]))
        print("The most popular stage is " + max_stages + " and least popular stage is " + min_stages)

        min_value = min(stages.values())
        max_value = max(stages.values())
        min_result = [(key, value) for key, value in stages.items() if value == min_value]
        max_result = [(key, value) for key, value in stages.items() if value == max_value]

        max_stages_dict_list = []
        for key in max_result:
            max_stages_dict_list.append({'stage': key[0], 'count': key[1]})

        min_stages_dict_list = []
        for key in min_result:
            min_stages_dict_list.append({'stage': key[0], 'count': key[1]})

        mean_stages = float(sum(stageCountAll)) / max(len(stageCountAll), 1)
        result = {'most_popular_operation': max_stages_dict_list,
                  'least_popular_operation': min_stages_dict_list,
                  'avg_stages': mean_stages,
                  'stages_per_file': stagesPerFile,
                  'all_stages_found': stages}
    except Exception as e:
        logging.error(e)
        result = {}

    return result


def get_trigger_stages_correlation():
    logging.info('Analyzing Jenkinsfiles for correlation between stages and triggers')
    counts = {'stages': 0, 'triggers': 0, 'stagetrigger': 0, 'stagesq': 0, 'triggersq': 0}
    totalfiles = 0
    jenkinsfiles = []
    for page_number in range(1, 10):
        try:
            repositories = jenkinsfile_query('triggers+stages', page_number)
            for repo in repositories.json()['items']:

                print(repo['url'])
                jenkinsfile_content = contents_query(repo['url'])
                file_content = readyFile(jenkinsfile_content)
                stagecount = 0
                triggercount = 0
                insidetrigger = False
                trigger = ''
                if re.search(r"triggers\s+\{", jenkinsfile_content.text):
                    totalfiles += 1
                    for line in file_content:
                        t = re.search(r"triggers\s+\{", line)
                        if t:
                            insidetrigger = True
                        if insidetrigger:
                            trigger.join(line)
                            if re.search(r"(cron|pollSCM|upstream)", line):
                                triggercount += 1
                            elif re.search(r"\s+\}", line):
                                insidetrigger = False

                        m = re.search(r"""\bstage\b\s*\((["'])(?:(?=(\\?))\2.)*?\1\)""", line)
                        if m:
                            stagecount += 1

                    counts['stages'] += stagecount
                    counts['triggers'] += triggercount
                    counts['stagetrigger'] += (stagecount*triggercount)
                    counts['stagesq'] += (stagecount**2)
                    counts['triggersq'] += (triggercount**2)
                    jenkinsfiles.append({'url': repo['url'], 'stages': stagecount, 'triggers': triggercount})
        except Exception as e:
            print(e)

    try:
        n = (totalfiles * counts['stagetrigger']) - (counts['stages'] * counts['triggers'])
        d = math.sqrt((totalfiles * counts['stagesq'] - counts['stages']**2) * (totalfiles * counts['triggersq'] - counts['triggers']**2))
        corr_coeff = n / d
        print('coeff is %.3f', corr_coeff)
        result = {'correlation_coefficient': corr_coeff,
                  'total_stages': counts['stages'],
                  'total_triggers': counts['triggers'],
                  'jenkinsfiles_analysed': jenkinsfiles}
    except Exception as e:
        logging.error(e)
        result = {}

    return result
