import os
import json

def is_narrative(parenthetical):
    return len(parenthetical.split()) > 7

def parse_json(json_file):
    narrative_parentheticals = []
    
    with open(json_file) as file:
        data = json.load(file)
        for citation in data.get('cites_to', []):
            for pin_cite in citation.get('pin_cites', []):
                parenthetical = pin_cite.get('parenthetical', '')
                if is_narrative(parenthetical):
                    narrative_parentheticals.append(parenthetical)
                    
    return narrative_parentheticals[:5]  # Only take the first 5

def filter_and_rank_cases(prompt, search_results):
    case_infos = []
    research_body = []

    if 'results' not in search_results:
        return research_body, case_infos

    results = search_results['results'][:5]  

    # Process each case
    for case in results:
        print(f"Processing case: {case['name']}\n\n")  # Debug print

        cites_to = case.get('cites_to', [])
        case_parentheticals = []
        for cite in cites_to:
            pin_cites = cite.get('pin_cites', [])
            # Filter out parentheticals that aren't narrative
            parentheticals = [pin_cite.get('parenthetical') for pin_cite in pin_cites if pin_cite.get('parenthetical') and is_narrative(pin_cite.get('parenthetical'))]
            if parentheticals:
                print(f"Filtered parentheticals : {parentheticals}\n\n")  # Debug print
                case_parentheticals.extend(parentheticals)

        # Only take the first 5 parentheticals
        case_parentheticals = case_parentheticals[:7]

        # Get the official citation
        citations = case.get('citations', [])
        official_cite = next((c['cite'] for c in citations if c['type'] == 'official'), '')

        # Format the citation as 'Name, Citation (Year)'
        formatted_citation = f"{case['name_abbreviation']}, {official_cite} ({case['decision_date'][:4]})" if official_cite else ''

        # Add the slim case text to the research_body
        slim_case_text = {"case_name": case['name'], 
                          "citation": formatted_citation, 
                          "parentheticals": case_parentheticals}
        research_body.append(slim_case_text)

    # Iterate over the research body
    for slim_case_text in research_body:
        # Create a case information dictionary
        case_info = {
            "case_name": slim_case_text['case_name'],
            "citation": slim_case_text['citation'],
            "helpful_parenthetical": ', '.join(slim_case_text['parentheticals']),
        }
    
        # Add the case information dictionary to the list
        case_infos.append(case_info)

    return research_body, case_infos
