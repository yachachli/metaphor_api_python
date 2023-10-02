import json
import openai
import requests
from metaphor_python import Metaphor

# Load API Keys
with open('metaphor_API_key.json', 'r') as file:
    metaphor_api_key = json.load(file).get('API_Key')
    
with open('openAI_API_Key.json', 'r') as file:
    openai_api_key = json.load(file).get('API_Key')

# Set API Keys
openai.api_key = openai_api_key
metaphor = Metaphor(metaphor_api_key)
ingredients = input("Comma seperated ingredients: ")
ingredient_prompt = ("Hello, given the following ingredients I own, please provide me with one single best recipe I can make using them. Please only provide the name of the recipe in the form: Recipe1 The ingredients are: " +  ingredients )
# SYSTEM_MESSAGE = "You are a helpful assistant that generates recipes based strictly off of users comma seperated ingredients. when generating recipes, generate only 1 best recipe given the users ingredients listed, only the name of the recipe"


# Generate Search Query using OpenAI
completion = openai.ChatCompletion.create(
    model="gpt-3.5-turbo",
    messages=[
        #{"role": "system", "content": },
        {"role": "user", "content": ingredient_prompt},
    ],
    temperature=0.6,
    max_tokens=150,
)

query = completion.choices[0].message.content
#print(query)

# Search using Metaphor API

search_response = metaphor.search(
    query, use_autoprompt=True, start_published_date="2023-06-01"
)
#print(f"URLs: {[result.url for result in search_response.results]}\n")

contents_result = search_response.get_contents()
first_result = contents_result.contents[0]

SYSTEM_MESSAGE = "You are a helpful assistant that summarizes the content of a webpage. Summarize the users input."

completion = openai.ChatCompletion.create(
    model="gpt-3.5-turbo",
    messages=[
        {"role": "system", "content": SYSTEM_MESSAGE},
        {"role": "user", "content": first_result.extract},
    ],
)

summary = completion.choices[0].message.content
print(f"Summary for {first_result.title}: {summary}")