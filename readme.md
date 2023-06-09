# LegalWRITER
<p align="center">
<img src="https://i.imgur.com/trmipRit.png"/>
</p>

### GPT-3.5-turbo + Harvard Law's Case Access Project 
-is your new legal writting assistant.

The purpose of the program outlined in these files is to create a legal research assistant. It uses OpenAI's GPT-3 model to interact with a user and perform relevant legal research. The program can take a question from a user, create a search query, retrieve relevant cases, filter them, generate helpful summaries, and respond with a comprehensive and understandable explanation of relevant law with proper citations.  Finally, it will create a case summary for youfor the cases cited.

You will need the following accounts and their associated APIs to use this application:

### OpenAI
https://platform.openai.com/signup

### Case Access Project
https://case.law/user/register/

## app.py: 

This is the main Flask application. It creates a web server that listens for requests. The '/' route serves the main index.html page, and the '/submit' route takes a legal question as input, uses the other modules to find and analyze relevant legal cases, and then generates a response to the question.

## search.py: 

This module handles the initial search for legal cases. It first uses OpenAI's GPT model to generate a legal query term based on the input prompt. It then uses the case.law to search Harvard Law School's Case Access Project (CAP) database for relevant legal cases. The search results are returned as JSON.

## analysis.py: 

This module analyzes the search results in more detail. It checks parenthetical elements in the case meta data of each case, then extracts the citation and case name. It then calculates a relevance score for each chunk using OpenAI's GPT model. The relevance score is used to rank the cases. It also extracts helpful quotes from the cases and returns those as part of the case information.

## output.py: 

This module generates the final output, which is a response to the legal question. It uses OpenAI's GPT model to generate a response based on the case information and the initial prompt. The generated response is then returned to the Flask application.

## Summarizer.py

This module will provide the option for the end-user to get a summary of the cases which were used in the answer.  The summary will be created with chatGPT and will br broken into chunks, ingested, and then summarized.  I have not tested this file yet, but the basic princible works on openai.com with chatGPT-3.  This will be the final component of the web app.

##

The system is designed to work in a conversational manner, which means it processes the input question, conducts a search, analyzes the results, and generates a response all in the context of a conversation.

According to ChatGPT, "This program represents a significant step in legal tech, offering a conversational interface for legal research that could save legal professionals considerable time. It showcases the utility of AI in parsing large amounts of legal data and delivering relevant, synthesized, and actionable insights."

This is a work in progress but it is functional.  Improvements over LawSCHOLAR include use of gpt-3.5-turbo and CAP which finds more relevant cases than google scholar.  They are ranked for relevance and not popularity.  Prompts still need to be engineered better and performace should be improved to give faster results. The webUI should get updated to allow for other search filters, e.g. other jurisdictions, currently only serves Vermont. JavaScript needs to be updated to allow paragraph breaks. 

The final task will be to create a case summary function to generate case summaries for use in legal writing.  The goal is to make a useful tool to speed up legal research and writing for lawyers. Of course, the lawyer will need to check the work, but the hope is that it will save time by generating useful content.  Finally, the server should be replaced with a deployment server (wsgi) rather than the development server (FLASK). 
