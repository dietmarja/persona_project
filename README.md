# Overall Readme File for the Persona Project
The person project seeks to find out whether and under what conditions, a persona can outperform the LLM it is derived from. 
The Python program in the repository "person_project" provides the tools or modules used to achieve this goal. Allocated to a subfolder, 
each of the modules addresses a particular aspect of the questions to be addressed while otherwise maintaining a structure similar to the other modules. 
For instance, each module can be configured, it stated via a bash script and has a specific readme file,  

### persona2interviews
This is the central module that sets the stage by turning person description into interviews. The system can be 
configure such that it runs either 1:1 Interviews or 1:1 interviews. At the moment, only persona2interviews is available via GitHub. 

persona2interviews
### persona2interviews

### Running the application
Go to the root folder of the module lik so ...

cd /Users/dietmar/Dropbox/PycharmProjects/persona_project/persona2interviews/

and run the script

./code/run_persona2interviews.sh | tee terminal-output.txt

### interviews2statistics


./code/run_interviews2statistics.sh | tee t.txt

### interviews2token_distribution
./code/run_interviews2token_distribution.sh | tee terminal_output.txt
