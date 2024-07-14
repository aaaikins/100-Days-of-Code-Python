import requests
import os
from twilio.rest import Client

account_sid = os.environ.get("ACCOUNT_SID")
auth_token = os.environ.get("AUTH_TOKEN")

# Print the auth_token and account_sid to verify they're being retrieved correctly (remove this in production code)
print(f"Account SID: {account_sid}")
print(f"Auth Token: {auth_token}")

if not auth_token or not account_sid:
    raise ValueError("Twilio credentials are missing. Make sure the ACCOUNT_SID and AUTH_TOKEN environment variables are set.")

client = Client(account_sid, auth_token)

endpoint = 'https://api.openweathermap.org/data/2.5/forecast'
MY_LATITUDE = 44.552841
MY_LONGITUDE = -69.631310
api_key = os.environ.get("API_KEY")

# Print the api_key to verify it's being retrieved correctly (remove this in production code)
print(f"API Key: {api_key}")

if not api_key:
    raise ValueError("OpenWeatherMap API Key is missing. Make sure the API_KEY environment variable is set.")

parameters = {
    'lat': MY_LATITUDE,
    'lon': MY_LONGITUDE,
    'appid': api_key,
    'cnt': 4
}

response = requests.get(endpoint, params=parameters)
response.raise_for_status()
data = response.json()

will_rain = False
for i in range(len(data['list'])):
    weather = data['list'][i]['weather']
    weather_id = weather[0]['id']
    if int(weather_id) < 700:
        will_rain = True
        break

if will_rain:
    message = client.messages.create(
        from_='whatsapp:+14155238886',
        body="It's going to rain. Bring your ☔️",
        to='whatsapp:+12076494169'
    )

    print(message.status)
