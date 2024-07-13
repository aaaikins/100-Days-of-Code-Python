import requests

# Define the parameters for the API request
amount = 10
question_type = 'boolean'
category = 18

# Create a dictionary of parameters for the API request
parameters = {
    "amount": amount,
    "type": question_type,
    "category": category
}

# Send a GET request to the Open Trivia Database API
response = requests.get("https://opentdb.com/api.php", params=parameters)

# Raise an HTTPError if the HTTP request returned an unsuccessful status code
response.raise_for_status()

# Parse the JSON response into a Python dictionary
data = response.json()

# Extract the list of questions from the response data
question_data = data['results']
