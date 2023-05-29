# LegalWRITER

![Alt AI Lawyer](https://imgur.com/trmipRi)

### GPT-3.5-turbo + LangChain + Harvard Law's Case Access Project is your new legal writting assistant.

The purpose of the program outlined in these files is to create a legal research assistant. It uses OpenAI's GPT-3 model to interact with a user and perform relevant legal research. The program can take a question from a user, create a search query, retrieve relevant cases, filter them, generate helpful summaries, and respond with a comprehensive and understandable explanation of relevant law with proper citations.

## app.py: 

This is the main Flask application. It creates a web server that listens for requests. The '/' route serves the main index.html page, and the '/submit' route takes a legal question as input, uses the other modules to find and analyze relevant legal cases, and then generates a response to the question.

## search.py: 

This module handles the initial search for legal cases. It first uses OpenAI's GPT model to generate a legal query term based on the input prompt. It then uses the case.law to search Harvard Law School's Case Access Project (CAP) database for relevant legal cases. The search results are returned as JSON.

## langchain.py: 

This module processes the search results using LangChain, a text similarity search library. It uses LangChain's Language Model Mediator (LLM) and ConversationChain to create a conversational context and process the search results. It then splits the case texts into smaller chunks and indexes them for similarity search. It ranks the cases based on their similarity to the query.

## analysis.py: 

This module analyzes the search results in more detail. It checks parenthetical elements in the case meta data of each case, then extracts the citation and case name. It then calculates a relevance score for each chunk using OpenAI's GPT model. The relevance score is used to rank the cases. It also extracts helpful quotes from the cases and returns those as part of the case information.

## output.py: 

This module generates the final output, which is a response to the legal question. It uses OpenAI's GPT model to generate a response based on the case information and the initial prompt. The generated response is then returned to the Flask application.

## 

The system is designed to work in a conversational manner, which means it processes the input question, conducts a search, analyzes the results, and generates a response all in the context of a conversation.

According to ChatGPT, "This program represents a significant step in legal tech, offering a conversational interface for legal research that could save legal professionals considerable time. It showcases the utility of AI in parsing large amounts of legal data and delivering relevant, synthesized, and actionable insights."

This is a work in progress but it is functional.  Improvements over LawSCHOLAR include use of gpt-3.5-turbo and CAP which finds more relevant cases than google scholar.  They are ranked for relevance and not popularity.  Prompts still need to be engineered better and performace should be improved to give faster results. The webUI should get updated to allow for other search filters, e.g. other jurisdictions, currently only serves Vermont. JavaScript needs to be updated to allow paragraph breaks. Finally, the server should be replaced with a deployment server (wsgi) rather than the development server (FLASK).
