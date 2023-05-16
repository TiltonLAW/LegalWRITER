# analysis.py

import os
import openai
import re
import requests

def get_relevance_scores(prompt, parentheticals):
    openai.api_key = os.getenv("OPENAI_API_KEY")

    # Check if there are any parentheticals
    if not parentheticals:
        return []

    # Join all parentheticals into a single string, each separated by a newline
    all_parentheticals = "\n".join(f"Case text: \"{p}\"." for p in parentheticals)

    print(f"Sending the following texts for scoring:\n{all_parentheticals}")  # Debug print

    response = openai.Completion.create(
        model="text-curie-001",
        prompt=f"On a scale of 1 to 10, how relevant is the statement '{all_parentheticals}' to the prompt: \"{prompt}\".\n\n Score with a number only, do not add any narrative or words.  Relevance score: ",
        max_tokens=20,
        temperature=0.8,
        top_p=1,
        frequency_penalty=0,
        presence_penalty=0
    )

    # Split the response text into individual scores
    scores_text = response.choices[0].text.strip().split("\n")
    print(f"Received scores: {scores_text}")  # Debug print

    # Extract only the score (digit) from each score text
    scores = []
    for score_text in scores_text:
        match = re.search(r"\d+", score_text)  # Use regex to find the first number in the string
        if match:
            score = int(match.group())  # Convert the matched number to an int
            scores.append(score)
        else:
            scores.append(0)  # If no number is found, append 0

    print(f"Scores: {scores}")  # Debug print scores
    return scores

def filter_and_rank_cases(prompt, search_results):
    if 'results' not in search_results:
        return [], []

    results = search_results['results'][:5]  

    case_infos = []

    # Calculate relevance scores for each case
    for case in results:
        print(f"Processing case: {case['name']}")  # Debug print

        cites_to = case.get('cites_to', [])
        for cite in cites_to:
            pin_cites = cite.get('pin_cites', [])
            # Filter out parentheticals with less than 5 words
            parentheticals = [pin_cite.get('parenthetical') for pin_cite in pin_cites if pin_cite.get('parenthetical') and len(pin_cite.get('parenthetical').split()) > 5]

            print(f"Filtered parentheticals (more than 5 words): {parentheticals}")  # Debug print

            if parentheticals:
                scores = get_relevance_scores(prompt, parentheticals[:4])  # Limit to the first 4 parentheticals

                for parenthetical, score in zip(parentheticals[:4], scores):  # Only consider first 4 parentheticals
                    print(f"Relevance score for '{parenthetical}': {score}")  # Debug print

                    # Consider a parenthetical helpful only if the score is between 7 and 10 (inclusive)
                    if 7 <= score <= 10:  
                        # Get the official citation
                        citations = case.get('citations', [])
                        official_cite = next((c['cite'] for c in citations if c['type'] == 'official'), '')
                        
                        # Format the citation as 'Name, Citation (Year)'
                        formatted_citation = f"{case['name_abbreviation']}, {official_cite} ({case['decision_date'][:4]})" if official_cite else ''

                        case_infos.append({
                        'case_name': case['name_abbreviation'],
                        'citation': formatted_citation,
                        'helpful_parenthetical': parenthetical
                    })

    return results, case_infos
