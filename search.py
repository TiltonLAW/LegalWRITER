import os
import requests
import openai

# search.py

os.environ['OPENAI_API_KEY'] = '-----------insert key here--------------------'
os.environ['CASELAW_API_KEY'] = '-----------insert key here--------------------'

# search case.law with the query

def get_search_results(query, prompt):
    # print(f"Query before check: '{query}'")
    if query is None or query == "":
        # Generate a query using GPT
        query = generate_query(prompt)

    case_law_api_key = os.environ['CASELAW_API_KEY']
    query_encoded = requests.utils.quote(query)
    print(f"Query: '{query}'")
    response = requests.get(
        f'https://api.case.law/v1/cases/?page_size=3&search={query_encoded}&jurisdiction=vt&court=vt&decision_date_min=1960',
        headers={'Authorization': f'Token {case_law_api_key}'}
    )
    search_results = response.json()
    # print(f"Search results: '{search_results}':")
    # Include the query in the search_results dictionary
    search_results['query'] = query

    print(f"Search results for query '{query}':")
    for i, result in enumerate(search_results.get('results', [])):
        print(f"Result {i + 1}: {result['name']}")

    return search_results

def generate_query(prompt):
    openai.api_key = os.environ['OPENAI_API_KEY']
    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "system", "content": "You are a helpful legal assistant."},
            {"role": "user", "content": f"Generate a search query for a caselaw search engine to find and answer for this question: \"{prompt}\"? If possible use a single legal doctrine or single term of art that fits perfectly, otherwise please reduce the question to the three most important words to get helpful results from a caselaw search engine. The answer should not exceed 4 words. Do not answer in the narrative form, only provide the search terms in your reply and nothing else:"},
        ],
        temperature=0.7,
        max_tokens=7,
        top_p=1,
        frequency_penalty=0,
        presence_penalty=0
    )
    term = response.choices[0].message['content'].strip().replace('"', '')
    print(f"Generated legal term for the prompt '{prompt}': {term}")
    return term

def load_case_json(case_url):
    response = requests.get(case_url)
    case_data = response.json()
    return case_data
