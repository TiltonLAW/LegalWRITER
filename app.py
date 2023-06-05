# app.py

from flask import Flask, render_template, request, jsonify
import search
import analysis
import output
import summarizer
import requests

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/submit', methods=['POST'])
def submit():
    data = request.get_json()
    prompt = data['prompt']
    query = data.get('query', None)
    
    # Fetch the search results
    search_results = search.get_search_results(query, prompt)
    
    # Pass the prompt to the get_search_results function
    research_body, case_infos = analysis.filter_and_rank_cases(prompt, query, search_results)
    
    # Analyze and rank the results
    results, case_infos = analysis.filter_and_rank_cases(prompt, query, search_results)

    # Generate the response
    answer, summarize_buttons = output.generate_response(prompt, results, case_infos)

    return jsonify({"answer": answer, "summarize_buttons": summarize_buttons})

@app.route('/summarize', methods=['POST'])
def summarize():
    data = request.get_json()
    url = data['url'] # Update to use JSON URL
    response = requests.get(url)
    case_data = response.json()  # Parse the response as JSON

    summary = summarizer.summarize_case(url)  # Pass the parsed JSON data to the summarize_case function
    return jsonify({"summary": summary})


# if __name__ == '__main__':
  #  app.run(debug=true)
