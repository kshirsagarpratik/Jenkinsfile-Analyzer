''' The first step is to find and retrieve Jenkinsfile(s) from various open source repositories. We decided to use GitHub's REST API for our application. We are trying to access a jenkinsfile's raw content so that we can append it to one text file that contains all the jenkinsfiles' contents. This process will streamline parsing and generating results of analyses later on.

We are using a Jupyter Notebook from Anaconda with Python 3.6, we use the following packages to start off with our task. '''

from Questions import *
import json

'''Configure the log file'''
LOG_FILENAME = 'course_proj.log'
logging.basicConfig(
    filename = LOG_FILENAME,
    level = logging.DEBUG,
    format = '%(asctime)s %(levelname)s %(message)s',
    filemode = 'w'
)
try:
    # get the result of each of the questions
    exception_handled = exception_handling()
    docker_used = docker()
    agent_used = popular_agent()
    global_agent_used = global_agent()
    post_condition_stats = get_post_cond_stats()
    stage_stats = get_pipeline_stage_stats()
    trigger_stage_corr = get_trigger_stages_correlation()

    # get the result of each of the questions and create a dictionary of the results of the questions to create a json file
    jsondata = {
        'jenkinsfiles_exception_handling': exception_handled,
        'docker_used': docker_used,
        'agents_used': agent_used,
        'global_agent_used': global_agent_used,
        'post_condition_stats': post_condition_stats,
        'stage_stats': stage_stats,
        'trigger_stage_correlation': trigger_stage_corr
    }

    # Writing JSON data
    with open('result.json', 'w') as f:
        json.dump(jsondata, f, ensure_ascii=False, indent=4)
    logging.info('result.json created!')

    # creating some graphs with the statistics


except Exception as e:
    logging.error(e)



