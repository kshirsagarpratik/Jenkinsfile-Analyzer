import requests # Helps working with HTTP requests such as GitHub API.
import os # For performing tasks on shell.
import subprocess # For performing tasks on shell.
import logging # For creating log files
import re
from P import *
from collections import defaultdict


def getPostCondStats():
    print('Attempting to retrieve jenkinsfile(s) from various GitHub repositories through it\'s REST API...')
    # We are aiming to retrieve ~1000 Jenkinsfiles that are available on GitHub, as every page has max 100 results.
    post_block = defaultdict(int)
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
                for line in file_content:
                    if re.search(r'\balways\b\s*\{', line):
                        post_block['always'] += 1
                    elif re.search(r'\bsuccess\b\s*\{', line):
                        post_block['success'] += 1
                    elif re.search(r'\bfailure\b\s*\{', line):
                        post_block['failure'] += 1
                    elif re.search(r'\bchanged\b\s*\{', line):
                        post_block['changed'] += 1
                    elif re.search(r'\bfixed\b\s*\{', line):
                        post_block['fixed'] += 1
                    elif re.search(r'\bregression\b\s*\{', line):
                        post_block['regression'] += 1
                    elif re.search(r'\baborted\b\s*\{', line):
                        post_block['aborted'] += 1
                    elif re.search(r'\bunstable\b\s*\{', line):
                        post_block['unstable'] += 1
                    elif re.search(r'\bcleanup\b\s*\{', line):
                        post_block['cleanup'] += 1

                file_pointer.close()

        except Exception as e:
            print(e)

    print(post_block)
    # sorted_pb = [(k, v) for k, v in post_block.items()]
    max_post_block = max(post_block.keys(), key=(lambda k: post_block[k]))
    min_post_block = min(post_block.keys(), key=(lambda k: post_block[k]))
    print("The most frequent post condition is " + max_post_block + " and least frequent is " + min_post_block)


def getPipelineStageStats():
    stages = defaultdict(int)
    stageCountAll = list()
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
                triggercount = 0
                insidetrigger = False
                trigger = ''
                for line in file_content:
                    m = re.search(r"""\bstage\b\s*\((["'])(?:(?=(\\?))\2.)*?\1\)""", line)
                    if m:
                        stagestr = m.group(0).replace("stage('", "").replace("')", '')
                        stages[stagestr] += 1
                        stagecount += 1
                    else:
                        t = re.search(r"triggers\s+\{", line)
                        #t = re.search(r"^(cron|pollSCM|upstream)", line)
                        if t:
                            insidetrigger = True
                        if insidetrigger:
                            print(line)
                            trigger.join(line)
                            if re.search(r"\s+\}", line):
                                insidetrigger = False
                            elif re.search(r"(cron|pollSCM|upstream)", line):
                                triggercount += 1

                file_pointer.close()
                print(trigger)
                print(stagecount)
                print(triggercount)
                stageCountAll.append((stagecount, triggercount))

        except Exception as e:
            print(e)

    #print(stages)
    max_stages = max(stages.keys(), key=(lambda k: stages[k]))
    min_stages = min(stages.keys(), key=(lambda k: stages[k]))
    print("The most popular stage is " + max_stages + " and least popular stage is " + min_stages)