import os
import openai

# Extract the case text from the given case JSON
def extract_case_text(case):
    opinions = case.get('casebody', {}).get('data', {}).get('opinions', [])
    if opinions:
        case_text = opinions[0].get('text', '')
        return case_text
    return ''

# Call the OpenAI API
def call_openai_api(prompt, role="user"):
    openai.api_key = os.environ['OPENAI_API_KEY']
    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "system", "content": "You are a a document/text loader, you load and remember content of the next text/s or document/s."},
            {"role": role, "content": prompt},
        ],
        temperature=0.8,
        max_tokens=4096,
    )
    return response.choices[0].message['content']

# Load case text chunk by chunk
def load_case_text(case):
    chunk_size = 4000  # size of chunks (OpenAI has a limit of 4096 tokens)
    case_text = extract_case_text(case)

    if case_text:
        # Split the case text into chunks
        case_text_chunks = [case_text[i:i+chunk_size] for i in range(0, len(case_text), chunk_size)]
        num_chunks = len(case_text_chunks)

        # Load first chunk with document loading instructions
        first_chunk = case_text_chunks[0]
        instructions = "There might be multiple files, each file is marked by name in the format ### DOCUMENT NAME. I will send you them by chunks. Each chunk start will be noted as [START CHUNK x/TOTAL], and end of this chunk will be noted as [END CHUNK x/TOTAL], where x is number of current chunk and TOTAL is number of all chunks I will send you. I will send you multiple messages with chunks, for each message just reply OK: [CHUNK x/TOTAL], don't reply anything else, don't explain the text! Let's begin:"
        first_prompt = f"[START CHUNK 1/{num_chunks}]\n### {case['name']} ###\n{first_chunk}\n[END CHUNK 1/{num_chunks}]"
        response = call_openai_api(first_prompt + instructions)

        # Check if the response is as expected
        if response.strip() != f"OK: [CHUNK 1/{num_chunks}]":
            print(f"Unexpected response for chunk 1/{num_chunks}: {response}")
            return None

        # Load remaining chunks
        for i, chunk in enumerate(case_text_chunks[1:], start=2):
            prompt = f"[START CHUNK {i}/{num_chunks}]\n### {case['name']} ###\n{chunk}\n[END CHUNK {i}/{num_chunks}]"
            response = call_openai_api(prompt)

            # Check if the response is as expected
            if response.strip() != f"OK: [CHUNK {i}/{num_chunks}]":
                print(f"Unexpected response for chunk {i}/{num_chunks}: {response}")
                return None

        return case_text  # Return the original case_text as all chunks are loaded successfully

    return ''

# Summarize a single case
def summarize_case(case):
    loaded_case_text = load_case_text(case)
    if loaded_case_text:
        summary_prompt = f"Please write a summary for the case {case['name_abbreviation']}"
        case_summary = call_openai_api(summary_prompt, role="user")
        return case_summary

    return ''

# Example usage:
# case = ...  # load the case from JSON file
# print(summarize_case(case))

