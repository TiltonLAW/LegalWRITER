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

    response = openai.Completion.create(
        model="text-davinci-003",
        prompt=f"On a scale of 1 (not helpful) to 10 (highly helpful), how helpful are the following case texts for answering the legal question: \"{prompt}\"?\n\n{all_parentheticals}\n\nRelevance scores: ",
        max_tokens=20,
        temperature=0.7,
        top_p=1,
        frequency_penalty=0,
        presence_penalty=0
    )

    # Split the response text into individual scores
    scores_text = response.choices[0].text.strip().split("\n")

    # Extract only digits from each score and convert to int
    scores = [int(''.join(filter(str.isdigit, score_text))) if score_text.isdigit() else 0 for score_text in scores_text]

    return scores


def filter_and_rank_cases(prompt, search_results):
    if 'results' not in search_results:
        return [], []

    results = search_results['results'][:9]  

    case_infos = []

    # Calculate relevance scores for each case
    for case in results:
        cites_to = case.get('cites_to', [])
        for cite in cites_to:
            pin_cites = cite.get('pin_cites', [])
            parentheticals = [pin_cite.get('parenthetical') for pin_cite in pin_cites if pin_cite.get('parenthetical')]

            print(f"Case: {case['name']}, Parentheticals: {parentheticals}")  # Debug print

            # Limit to the first 3 parentheticals
            parentheticals = parentheticals[:5]

            if parentheticals:
                scores = get_relevance_scores(prompt, parentheticals)

                for parenthetical, score in zip(parentheticals, scores):
                    # Consider a parenthetical helpful only if the score is between 7 and 10 (inclusive)
                    if 7 <= score <= 10:  
                        print(f"Relevance score for this parenthetical: {score} in {case['name']} stating {parenthetical}")  # Print the relevance score for each parenthetical

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

    # Debugging line: print the number of values to return
    print(f"Returning {len(results)} ranked cases and {len(case_infos)} case info items.")

    return results, case_infos