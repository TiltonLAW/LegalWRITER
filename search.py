import os
import openai
import requests

# search.py

os.environ['OPENAI_API_KEY'] = '[insert your openai api here]'
os.environ['CASELAW_API_KEY'] = '[inser your case.law api here]'

# create good search terms from the prompt

def generate_query(prompt):
    openai.api_key = os.environ['OPENAI_API_KEY']
    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "system", "content": "You are a helpful legal, research assistant."},
            {"role": "user", "content": f"Create a search query for this question: \"{prompt}\"? Please reduce the question to the three most important words to get helpful results from a caselaw search engine. Do not answer in the narrative form, only provide the search terms in your reply and nothing else.  For example, a question 'can a person use force in defense of their own personal proerty?' should return a result: 'force defense property'; and the question, 'what are the elements of promissory estoppel?' should return only: 'elements promissory estoppel.'"},
        ],
        temperature=0.8,
        max_tokens=10,
        top_p=1,
        frequency_penalty=0,
        presence_penalty=0
    )
    term = response.choices[0].message['content'].strip().replace('"', '')
    print(f"Generated legal term for the prompt '{prompt}': {term}")
    return term

# search case.law with the query

def get_search_results(query):
    case_law_api_key = os.environ['CASELAW_API_KEY']
    query_encoded = requests.utils.quote(query)
    print(f"Query: '{query}'")
    response = requests.get(
        f'https://api.case.law/v1/cases/?page_size=4&search={query_encoded}&jurisdiction=vt&court=vt&decision_date_min=1970',
        headers={'Authorization': f'Token {case_law_api_key}'}
    )
    search_results = response.json()
    
    print(f"Search results for query '{query}':")
    for i, result in enumerate(search_results.get('results', [])):
        print(f"Result {i + 1}: {result['name']}")    

    return search_results
