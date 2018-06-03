''' The first step is to find and retrieve Jenkinsfile(s) from various open source repositories. We decided to use GitHub's REST API for our application. We are trying to access a jenkinsfile's raw content so that we can append it to one text file that contains all the jenkinsfiles' contents. This process will streamline parsing and generating results of analyses later on.

We are using a Jupyter Notebook from Anaconda with Python 3.6, we use the following packages to start off with our task. '''

from Questions import *
import json
import plotly
import plotly.plotly as py
import plotly.graph_objs as go

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
        'how often do you find exception handling in pipelines': exception_handled,
        'percent of jenkins pipelines involving docker': docker_used,
        'what agents are used in a jenkins pipeline': agent_used,
        'how often is a global agent used in jenkins pipeline': global_agent_used,
        'what post conditions are commonly found in a jenkins pipeline': post_condition_stats,
        'what are the common pipeline operations': stage_stats,
        'correlation between the number of triggers and stages in a pipeline': trigger_stage_corr
    }

    # Writing data to .json file
    with open('result.json', 'w') as f:
        json.dump(jsondata, f, ensure_ascii=False, indent=4)
    logging.info('result.json created!')

    # creating some graphs with the statistics

    # set plotly credentials
    plotly.tools.set_credentials_file(username='', api_key='')

    # distribution of the number of pipeline operations in a jenkinsfile
    stages_count = []
    for stage in stage_stats['stages_per_file']:
        stages_count.append(len(stage['stages']))
    trace0 = go.Box(
        y=stages_count,
        name="Number of Stages in a Jenkins Pipeline"
    )
    plot0 = [trace0]
    layout0 = go.Layout(title='Distribution of the number of stages per Jenkinsfile', width=1280, height=640)
    fig0 = go.Figure(data=plot0, layout=layout0)

    py.image.save_as(fig0, filename='Stage_Dist.png')
    logging.info('Graph - Distribution of the number of stages per Jenkinsfile created')
    trace1 = go.Bar(
        x=list(stage_stats['all_stages_found'].keys()),
        y=list(stage_stats['all_stages_found'].values()),
        name="Pipeline Operations"
    )
    plot1 = [trace1]
    layout1 = go.Layout(title='Distribution of pipeline operations', width=1280, height=720)
    fig1 = go.Figure(data=plot1, layout=layout1)

    py.image.save_as(fig1, filename='Stage_Dist_bar.png')

    logging.info('Graph - Distribution of pipeline operations created')

    # distribution of the number of pipeline operations in a jenkinsfile
    post_cond_count = []
    for post_cond in post_condition_stats['post_conditions']:
        post_cond_count.append(len(post_cond['post_conditions']))
    trace2 = go.Box(
        y = post_cond_count,
        name = "Number of Post Conditions in a Jenkins Pipeline"
    )
    plot2 = [trace2]
    layout2 = go.Layout(title='Distribution of the number of post conditions per Jenkinsfile', width=1280, height=720)
    fig2 = go.Figure(data=plot2, layout=layout2)

    py.image.save_as(fig2, filename='Post_Conditions_Dist.png')
    logging.info('Graph - Distribution of Number of Post conditions created')

    trace3 = go.Bar(
        x=list(post_condition_stats['all_post_conditions'].keys()),
        y=list(post_condition_stats['all_post_conditions'].values()),
        name="Post Conditions"
    )
    plot3 = [trace3]
    layout3 = go.Layout(title='Distribution of post conditions', width=1280, height=720)
    fig3 = go.Figure(data=plot3, layout=layout3)

    py.image.save_as(fig3, filename='Post_condition_bar.png')
    logging.info('Graph - Distribution of post conditions created')

    trace_pie = go.Pie(labels=list(agent_used.keys()), values=list(agent_used.values()))

    py.image.save_as([trace_pie], filename='styled_pie_chart.png')
    logging.info('Graph - Distribution of agents used created')

except Exception as e:
    print(e)
    logging.error(e)



