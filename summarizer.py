import os
import openai
import requests
import json
import textwrap

# summarizer.py

def extract_case_data(case_data):
    opinions = case_data['casebody']['data'].get('opinions', [])
    if not opinions:
        return None
    else:
        majority_opinion_text = opinions[0].get('text', '')
        return {'majority': majority_opinion_text}

def call_openai_api(prompt, role="user"):
    openai.api_key = os.environ['OPENAI_API_KEY']
    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "system", "content": "You are a helpful assistant."},
            {"role": role, "content": prompt},
        ],
        temperature=0.5,
        max_tokens=3000,
    )
    return response.choices[0].message['content']

def recursive_summarize(text):
    if len(text) <= 2000:
        summary = call_openai_api("Please summarize the following text:\n" + text, role="user")
        print(f"Summary for text of length {len(text)}: {summary}")
        return summary
    else:
        # Split the text into chunks of 2000 characters each
        chunks = textwrap.wrap(text, 2000)
        summaries = [recursive_summarize(chunk) for chunk in chunks]
        combined_summary = " ".join(summaries)
        print(f"Combined summary for text of length {len(text)}: {combined_summary}")
        return combined_summary

def summarize_case(url):
    # Load the full case text
    headers = {'Authorization': 'Token ' + os.environ['CASELAW_API_KEY']}
    response = requests.get(url, headers=headers)
    case_data = response.json()
    case_data = extract_case_data(case_data)

    if case_data:
        # Load and summarize the case text
        full_case = case_data['majority']
        case_summary = recursive_summarize(full_case)
        print(f"Final case summary: {case_summary}")
        return case_summary

    return ''
