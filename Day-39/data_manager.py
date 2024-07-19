import os
import requests
from requests.auth import HTTPBasicAuth
from dotenv import load_dotenv
import logging

load_dotenv("./venv/.env")

SHEETY_PRICES_ENDPOINT = "https://api.sheety.co/ac6db95b5007ae8add39cf298d3a9966/flightDeals/prices"

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')


class DataManager:
    def __init__(self):
        self._user = os.environ.get("SHEETY_USERNAME")
        self._password = os.environ.get("SHEETY_PASSWORD")
        self._authorization = HTTPBasicAuth(self._user, self._password)
        self.destination_data = {}
        logging.info("DataManager initialized with user: %s", self._user)

    def get_destination_data(self):
        """
        Fetches destination data from the Sheety API.
        """
        try:
            response = requests.get(url=SHEETY_PRICES_ENDPOINT, auth=self._authorization)
            response.raise_for_status()
            data = response.json()
            self.destination_data = data.get("prices", [])
            logging.info("Destination data retrieved successfully")
        except requests.exceptions.RequestException as e:
            logging.error("Error fetching destination data: %s", e)
            self.destination_data = []
        return self.destination_data

    def update_destination_codes(self):
        """
        Updates the IATA codes for each city in the destination data.
        """
        for city in self.destination_data:
            new_data = {
                "price": {
                    "iataCode": city.get("iataCode", "")
                }
            }
            try:
                response = requests.put(
                    url=f"{SHEETY_PRICES_ENDPOINT}/{city['id']}",
                    json=new_data,
                    auth=self._authorization
                )
                response.raise_for_status()
                logging.info("Updated IATA code for city ID %s", city['id'])
            except requests.exceptions.RequestException as e:
                logging.error("Error updating IATA code for city ID %s: %s", city['id'], e)
