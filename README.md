# Jenkinsfile Analyzer

## Problem Statement

We have implemented a Jenkins pipeline analyzer in Python. We aim to address particular aspects of a Jenkins pipeline and we explored a lot of possibilities. A detailed description of our actions is given throughout this document. Below, we start with an abstract of our system.

![architecture](img/arch.PNG)
<h4 align="center">System Architecture</h4>

![flow](img/flow.PNG)
<h4 align="center">Pattern: Pipe and Filter</h4>

## Express Execution

**Note : Please enter your own credentials for github if you want to execute the code and see!**

To run the application:

#### Installing Python

Download the latest version of Python from https://www.python.org/downloads/. Make sure you download Python 3.x.

#### Installing pip

Download the latest version of pip from https://pip.pypa.io/en/stable/installing/

#### How to run it

Run the following commands to install the required modules

`sudo pip install -r requirements.txt`

Run Script.py

`python Script.py`

You can view the unit tests in `unittests.py`, to run them you can execute

`python unittests.py`