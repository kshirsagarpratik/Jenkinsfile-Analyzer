# Course Project

The goal of your course project is to empirically investigate a large number of devops pipeline programs and obtain statistical data that describe the content and patterns in devops pipelines. You will search and obtain jenkinsfiles and other pipeline artifacts from open-source repositories, e.g., github contains hundreds of pipeline examples and other code artifacts. The result of your investigation will be a report that summarizes the data - you can find an example of a report on my website (https://www.cs.uic.edu/~drmark/index_htm_files/Treasure.pdf). Examples of research questions that you will address include but not limited to the following.
* What are the most frequent post-condition blocks in the post section within jenkins pipelines? Create distribution graphs for post-condition blocks.
* How is the presence of triggers in a pipeline correlates with the number of stages in the pipeline?
* What are the most and the least frequent operations in pipeline stages?
* How often timeout periods are used in the pipeline runs and what are the most frequent intervals? How does the presence of timeouts correlate with certain commands executed at different stages of the pipeline?
* What tools are the most and the least frequently used in pipelines?

You will analyze pipelines in a number of steps. First, you need to obtain pipelines from various open-source repos, and the obvious starting point is to search and pull pipeline projects from Github, Krugle, and other open-source repositories of your choice. Just like in the previous two homeworks you will obtain devops projects from the repo and create a program that reads in the devops configuration file and analyzes the structure of the pipeline. The logic of your pipeline analyzer will be centered on answering the research questions that you formulate for this course project. However, you will go in a greater depth to determine what utilities and procedures are used in stages of the pipeline, how they interact with the project artifacts (e.g., run a test with certain parameters and then copy some files to a different directory). If the pipeline creates new artifacts (e.g., a new git project branch or an environment variable), your analyzer will examine if this branch exists in the project's git repo or the environment variable is accessed by its name in the source code of the software project. The depth of your analysis in the course project will determine your grade.

The output of your analyzer will be in a format of your choice (e.g., JSON, XML) that contain answers to your research questions. For example, the following entry describes the answer to the research question on how the presence of triggers in a pipeline correlates with the number of stages in the pipeline?
```
<rq correlationCoeff="0.87">How is the presence of triggers in a pipeline correlates with the number of stages in the pipeline?
	<proj1>gitURL1
		<trigger type="cron">H */4 * * 1-5
		</trigger>
		<trigger type="pollSCM">12
		</trigger>
		...
		<stage>1
		...
		</stage>
	</proj1>
</rq>
```

The part of the course project that requires a lot of thinking is the analysis of all components of the devops pipelines, linking them to commands that are used in stages, determining how to obtain information from the interactions among the commands and the project artifacts. Once you understand all relevant aspects of devops pipelines you will formulate research questions. Next, you will create abstractions based on which you will design programming components of this project and determine how to present the results of the analyses.

Please make sure that you were already added as a member of CS_540_2018 team in Bitbucket. Separate repositories will be created for each of your homeworks and for the course project. You will find a corresponding entry for this homework. You will fork this repository and your fork will be private, no one else besides you, your teammates and your course instructor will have access to your fork. Please remember to grant a read access to your repository to your instructor. You can commit and push your code as many times as you want. Your code will not be visible and it should not be visible to other students, except for your teammates. When you push it, your instructor will see you code in your separate private fork. Making your fork public or inviting other students to join your fork will result in losing your grade. For grading, only the latest push timed before the deadline will be considered. If you push after the deadline, your grade for the course priject will be zero. For more information about using git and bitbucket specifically, please use this link as the starting point https://confluence.atlassian.com/bitbucket/bitbucket-cloud-documentation-home-221448814.html.

------

For an additional bonus (up to 10%!) you will incorporate a machine learning algorithm for capturing and generalizing patterns of stages and commands in pipelines. Your ideas and creativity are highly welcome and will be rewarded! For example, like in your homeworks, you can obtain issues for each pulled software project and you can attempt to link these issues to specific organizations of the devops pipelines, if applicable.. You can create a separate database into which you can save the attributes of the pulled repos and bug reports and generalized patterns of pipelines. In short, your additional bonus will be based on how you connect various sources of information, not on simply downloading bits and pieces of information. Let your imagination fly!

------

Even though this is a individual course project, it can be done collaboratively. You are allowed to form groups between three to five teammates. If you want to work alone, it is perfectly fine. Logistically, one of you will create a private fork and will invite one or two of her classmates with the write access to your fork. You should be careful - once you form a group and write and submit code, you cannot start dividing your work and claim you did most of the work. Your forkmates may turn out to be freeloaders and you will be screwed. Be very careful and make sure that you trust your classmates before forming your group. I cannot and I will not resolve your internal group conflicts. Your submission will include the names of all of your forkmates and you will receive the same grade for this course project. 

I allow you to post questions and replies, statements, comments, discussion, etc. on Piazza. Remember that you cannot share your code and your solutions, but you can ask and advise others using Piazza on where resources and sample programs can be found on the internet, how to resolve dependencies and configuration issues, and how to design the logic of the algorithms and the workflows. Yet, your implementation should be your own or your team's and you cannot share it with the entire class. Alternatively, you cannot copy and paste someone else's implementation and put your name on it. Your submissions will be checked for plagiarism. When posting question and answers on Piazza, please select the appropriate folder, i.e., hw2 to ensure that all discussion threads can be easily located.

------

Submission deadline: Saturday, May 12 at 11PM CST. Your submission will include your source code, detailed documentation on all aspects of the installation and configuration of your solution, one or more of the SBT/Gradle/Maven build configurations, the README.md file in the root directory that contains the description of your implementation, how to compile and run it using your chosen build tool(s), and what are the limitations of your implementation. Please follow this naming convention while submitting your work : "Firstname_Lastname_hw2", so that we can easily recognize your submission. Those who work in groups can use longer names: "Firstname1_Lastname1_Firstname2_Lastname2_Firstname3_Lastname3_cp". I repeat, please make sure that you will give me read access to your private forked repository.

------
THE INSTRUCTOR WILL NOT ANSWER ANY REQUESTS FROM STUDENTS STARTING 7PM THE NIGHT BEFORE THE SUBMISSION DEADLINE.
------

Evaluation criteria:
* the maximum grade for this homework is 50%. Points are subtracted from this maximum grade: for example, saying that 2% is lost if some requirement is not completed means that the resulting grade will be 50%-2% => 48%;

* no comments or insufficient comments: up to 30% lost;

* no unit and integration tests: up to 30% lost;

* code does not compile or it crashes without completing the core functionality: up to 50% lost;

* the documentation is missing or insufficient to understand how to compile and run your program: up to 40% lost;

* only a subset of your functionality works: up to 30% lost;

* the minimum grade for this course project cannot be less than zero.

