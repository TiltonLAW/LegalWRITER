import openai
import os

# Load OpenAI API key from environment variable
openai.api_key = os.environ["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"]

# Set the OpenAI API model ID to use
MODEL_ID = "text-davinci-003"


def generate_response(prompt):
    # Set the parameters for the OpenAI API call
    completions = openai.Completion.create(
        engine=MODEL_ID,
        prompt=prompt,
        max_tokens=1024,
        n=1,
        stop=None,
        temperature=0,
    )

    # Extract the generated response from the API call results
    response = completions.choices[0].text.strip()

    return response
