from P import *
from rq_sai import *
import unittest
import os


def test_jenkinsfile_query_ex_handle(self):
    self.assertIsNotNone(jenkinsfile_query('try', 1))

def test_jenkinsfile_query_agent(self):
    self.assertIsNotNone(jenkinsfile_query('agent', 1))

def test_jenkinsfile_query_docker(self):
    self.assertIsNotNone(jenkinsfile_query('docker', 1))

def test_jenkinsfile_query_post(self):
    self.assertIsNotNone(jenkinsfile_query('post', 1))

def test_jenkinsfile_query_stages(self):
    self.assertIsNotNone(jenkinsfile_query('stages', 1))

def test_regex(self):
    self.assertIsNotNone(re.search(r'\bagent\b\s*\bnone\b', 'agent none'))
    self.assertIsNotNone(re.search(r'\btry\b\s*\{', 'try {'))
    self.assertIsNotNone(re.search(r'\bdocker\b\s*\{', 'docker {'))

test_regex()
test_jenkinsfile_query_agent()
test_jenkinsfile_query_docker()
test_jenkinsfile_query_ex_handle()
test_jenkinsfile_query_stages()
test_jenkinsfile_query_post()


