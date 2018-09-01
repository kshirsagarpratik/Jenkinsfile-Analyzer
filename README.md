# Jenkinsfile Analyzer

## Problem Statement

We have implemented a Jenkins pipeline analyzer in Python. We aim to address particular aspects of a Jenkins pipeline and we explored a lot of possibilities. A detailed description of our actions is given throughout this document. Below, we start with an abstract of our system.

![architecture](img/arch.PNG)
<h4 align="center">System Architecture</h4>

---

![flow](img/flow.PNG)
<h4 align="center">Pattern: Pipe and Filter</h4>

---

## Description

As you can see, at the heart of our system lies a Python script, which governs the behavior of all the other components. We tried to make our code as modular as possible so as to enable maximum `reusability`, easy `debugging` and `high performance` and `scalability`. We use GitHub as our source of Jenkinsfiles of various open source repositories and we have all of our programming modules in Python. We rely on converting our research requirements as a knowledge base of questions and make use of Regular Expressions to aggregate the apt data. Using JSON, we output our results onto a file and we also use some visualisation components to plot certain important measurements.

**Our system follows the Pipe and Filter pattern and the general workflow of our system is as follows:**

1. Obtain Jenkinsfiles from GitHub repositories through REST API.
2. Filter out the Jenkinsfile which are of importance, using certain keywords in the query along the HTTP request. We are firing unique queries which are appropriate to each of the research questions.
3. We thus obtain the raw contents of a Jenkinsfile and we store it in a .txt file which can be easily parsed.
4. We parse the .txt file and use Regular Expressions to extract vital information that can be used in the empirical analysis, as we will explain in depth in further sections.
5. The vital information that is extracted, is mapped with a Knowledge Base of the Research Questions to aggregate data that is essential to the empirical analysis.
6. The output of the empirical analysis is processed in a JSON file and some apt visualisation is performed with the results obtained.

## Formulation of Research Questions

> “How many Jenkins pipelines have some form of ​Exception Handling incorporated in them?”

We were particularly interested in this aspect of a DevOps pipeline as pipeline being a fairly complex process, automating one would bound to have some forms of Exceptions arise as there is plenty of margin for error due to the high number of interdependent components. We were interested in finding out how many of such pipelines ​do ​actually take care of handling runtime exceptions​.

> “What is the most frequent ​post-condition blocks in the post section within jenkins pipelines?”

We were interested in finding out what were the most/least popular post actions in a Jenkinsfile. We try to see which one or more additional steps that are run upon the completion of a Pipeline’s or stage’s run​.

> “What is the most frequently used ​agent ​ in a Jenkins pipeline?”

Agents specify ​where the entire Pipeline, or a specific stage, will execute in the Jenkins environment. We knew that there are certain kinds of agents that are available to the pipeline, so we wanted to know which ones of them are popular among applications and which ones are not so much.

> “What fraction of Jenkinsfile pipelines have no ​global agents​?”

We know that lack of a global agent implies that each stage section will need to contain its own agent section, this taking away a certain degree of centrality. We wanted to find out what fraction of Jenkinsfile follow such a pattern.

> “What percent of Jenkins pipelines involve Docker at some stage of execution?”

Docker, a container technology is prevalent in DevOps due to its performance and scalability in addition to its ​platform independence​. We wanted to find out how many Jenkins pipelines have adopted this technology as part of their routine.

> “What is the ​correlation between ​triggers in a pipeline and the number of stages​?”

We wanted to find out if there exists a correlation amongst the two and if it does, what is the significance of it. It seemed interesting to investigate co dependence of the two phenomena.

> “What are the most ​frequent​ Jenkins pipeline ​operations​?”

We discovered through observing various Jenkinsfiles that there exist many kinds of operations in a Jenkins pipeline so we try to discover which ones of them are the most frequent.

> “What is the ​average number of stages​ in a Jenkins pipeline?”

A Jenkins pipeline can have variable number of stages, so naturally we wanted to find the average number of stages, ie, how many stages is a
Jenkins pipeline would have, on average.

## Details of the Implementation

The system was implemented using Python 3.6.5 and PyCharm IDE. The logistic details of the implementation have been mentioned in the previous sections of this document. Here are some Python modules we used to implement the code:

*`Requests`
We used this package to deal with HTTP requests in order to interact with GitHub API to retrieve Jenkinsfiles.

*`RE`
This Regular Expressions library was used to a great extent as part of our Regex component. In the next section, we’ll show you how we used Regex to search/match patterns in the Jenkinsfile to find word strings that are pertinent in the empirical analysis.

*`Math`
We use this library in order to implement formulae used to find Carl Pearson’s Correlation coefficient.

*`JSON`
We use this library to produce our output in a pretty JSON format.

*`Logging`
We use this package for logging purposes, ie, creating and maintaining log files.

*`Plotly`
We use this package for generating visualisations such as charts and plots.

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