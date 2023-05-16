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
            {"role": "user", "content": f"Based on the research ({case_info}) only, answer the legal question(\"{prompt}\").\nDisregard all off topic and irrelevant portions of the research. \nProviding citations and relevant quotes, if any, provide an comprehesive and accurate legal analysis answering the question.\nAt the end of the answer, add 'Cases researched:' then list names and citations of all relevant cases found in the research."},
        ],
        temperature=0.5,
        max_tokens=2420,
        top_p=1,
        frequency_penalty=0,
        presence_penalty=0
    )

    answer = response.choices[0].message['content']

    return answer