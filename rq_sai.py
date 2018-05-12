import requests # Helps working with HTTP requests such as GitHub API.
import os # For performing tasks on shell.
import subprocess # For performing tasks on shell.
import logging # For creating log files
import re
from P import *
from collections import defaultdict
import math


def getPostCondStats():
    print('Attempting to retrieve jenkinsfile(s) from various GitHub repositories through it\'s REST API...')
    # We are aiming to retrieve ~1000 Jenkinsfiles that are available on GitHub, as every page has max 100 results.
    post_block = defaultdict(int)
    post_conditions = []
    for page_number in range(1, 10):
        try:
            repositories = jenkinsfile_query('post', page_number)
            for repo in repositories.json()['items']:

                print(repo['url'])
                jenkinsfile_content = contents_query(repo['url'])
                file_pointer = open('Jenkinsfile.txt', 'w+')
                file_pointer.write(jenkinsfile_content.text)
                file_pointer.close()
                file_pointer = open('Jenkinsfile.txt', 'r')
                file_content = file_pointer.readlines()
                post_cond = {'url': repo['url'], 'post_conditions': []}
                for line in file_content:
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

                file_pointer.close()
                post_conditions.append(post_cond)

        except Exception as e:
            print(e)

    print(post_block)
    # sorted_pb = [(k, v) for k, v in post_block.items()]
    max_post_block = max(post_block.keys(), key=(lambda k: post_block[k]))
    min_post_block = min(post_block.keys(), key=(lambda k: post_block[k]))
    print("The most frequent post condition is " + max_post_block + " and least frequent is " + min_post_block)

    min_value = min(post_block.values())
    max_value = max(post_block.values())
    min_result = [(key, value) for key, value in post_block.iteritems() if value == min_value]
    max_result = [(key, value) for key, value in post_block.iteritems() if value == max_value]

    max_dict_list = []
    for key in max_result:
        max_dict_list.append({'post_condition': key, 'count': max_result[key]})

    min_dict_list = []
    for key in min_result:
        min_dict_list.append({'post_condition': key, 'count': min_result[key]})

    result = {'most_frequent': max_dict_list,
              'least_frequent': min_dict_list,
              'post_conditions': post_conditions}

    return result


def getPipelineStageStats():
    stages = defaultdict(int)
    stageCountAll = list()
    stagesPerFile = list()
    for page_number in range(1, 10):
        try:
            repositories = jenkinsfile_query('stages', page_number)
            for repo in repositories.json()['items']:

                print(repo['url'])
                jenkinsfile_content = contents_query(repo['url'])
                file_pointer = open('Jenkinsfile.txt', 'w+')
                file_pointer.write(jenkinsfile_content.text)
                file_pointer.close()
                file_pointer = open('Jenkinsfile.txt', 'r')
                file_content = file_pointer.readlines()
                stagecount = 0
                stagesDict = {'url': repo['url'], 'stages': []}
                for line in file_content:
                    m = re.search(r"""\bstage\b\s*\((["'])(?:(?=(\\?))\2.)*?\1\)""", line)
                    if m:
                        stagestr = m.group(0).replace("stage('", "").replace("')", '')
                        stages[stagestr] += 1
                        stagecount += 1
                        stagesDict['stages'].append(stagestr)
                file_pointer.close()
                print(stagecount)

                stageCountAll.append(stagecount)
                stagesPerFile.append(stagesDict)
        except Exception as e:
            print(e)

    max_stages = max(stages.keys(), key=(lambda k: stages[k]))
    min_stages = min(stages.keys(), key=(lambda k: stages[k]))
    print("The most popular stage is " + max_stages + " and least popular stage is " + min_stages)

    min_value = min(stages.values())
    max_value = max(stages.values())
    min_result = [(key, value) for key, value in stages.iteritems() if value == min_value]
    max_result = [(key, value) for key, value in stages.iteritems() if value == max_value]

    max_stages_dict_list = []
    for key in max_result:
        max_stages_dict_list.append({'stage': key, 'count': max_result[key]})

    min_stages_dict_list = []
    for key in min_result:
        min_stages_dict_list.append({'stage': key, 'count': min_result[key]})

    mean_stages = float(sum(stageCountAll)) / max(len(stageCountAll), 1)
    result = {'most_popular_operation': max_stages_dict_list,
              'least_popular_operation': min_stages_dict_list,
              'avg_stages': mean_stages,
              'stages_per_file': stagesPerFile}

    return result


def getTriggerStagesCorelation():
    counts = {'stages': 0, 'triggers': 0, 'stagetrigger': 0, 'stagesq': 0, 'triggersq': 0}
    totalfiles = 0
    jenkinsfiles = []
    for page_number in range(1, 2):
        try:
            repositories = jenkinsfile_query('triggers+stages', page_number)
            for repo in repositories.json()['items']:

                print(repo['url'])
                jenkinsfile_content = contents_query(repo['url'])
                file_pointer = open('Jenkinsfile.txt', 'w+')
                file_pointer.write(jenkinsfile_content.text)
                file_pointer.close()
                file_pointer = open('Jenkinsfile.txt', 'r')
                file_content = file_pointer.readlines()
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
                            print(line)
                            trigger.join(line)
                            if re.search(r"(cron|pollSCM|upstream)", line):
                                triggercount += 1
                            elif re.search(r"\s+\}", line):
                                insidetrigger = False

                        m = re.search(r"""\bstage\b\s*\((["'])(?:(?=(\\?))\2.)*?\1\)""", line)
                        if m:
                            stagecount += 1

                    print(stagecount)
                    print(triggercount)
                    counts['stages'] += stagecount
                    counts['triggers'] += triggercount
                    counts['stagetrigger'] += (stagecount*triggercount)
                    counts['stagesq'] += (stagecount**2)
                    counts['triggersq'] += (triggercount**2)
                    jenkinsfiles.append({'url': repo['url'], 'stages': stagecount, 'triggers': triggercount})
                file_pointer.close()
        except Exception as e:
            print(e)

    n = (totalfiles * counts['stagetrigger']) - (counts['stages'] * counts['triggers'])
    d = math.sqrt((totalfiles * counts['stagesq'] - counts['stages']**2) * (totalfiles * counts['triggersq'] - counts['triggers']**2))
    corr_coeff = n / d
    print('coeff is %.3f', corr_coeff)
    result = {'correlation_coefficient': corr_coeff,
              'total_stages': counts['stages'],
              'total_triggers': counts['triggers'],
              'jenkinsfiles_analysed': jenkinsfiles}
    return result
