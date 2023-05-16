import openai
import os

# output.py

def generate_response(prompt, relevant_cases, case_infos):
    openai.api_key = os.environ['OPENAI_API_KEY']
    case_info = " ".join([f"{case['citation']}: {case['helpful_parenthetical']}" for case in case_infos])
    
    print("Case info:", case_info)  # Add this line to print case_info
    
    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "system", "content": "You are a helpful, legal assistant."},
            {"role": "user", "content": f"Based on the following caselaw provided, answer the legal question: \"{prompt}\".\n\nCaselaw: {case_info}\n\nProviding citations and relevant quotes, if any, Please provide an accurate and thorough answer:"},
        ],
        temperature=0.5,
        max_tokens=3090,
        top_p=1,
        frequency_penalty=0,
        presence_penalty=0
    )

    answer = response.choices[0].message['content']

    return answer