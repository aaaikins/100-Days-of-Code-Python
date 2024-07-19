import time
from datetime import datetime, timedelta
from data_manager import DataManager
from flight_search import FlightSearch
from flight_data import find_cheapest_flight
from notification_manager import NotificationManager

# Initialize instances of required classes
data_manager = DataManager()
sheet_data = data_manager.get_destination_data()
flight_search = FlightSearch()
notification_manager = NotificationManager()

# Constant for the origin city IATA code
ORIGIN_CITY_IATA = "PWN"

# Update IATA codes for destinations that are missing them
for row in sheet_data:
    if row["iataCode"] == "":
        row["iataCode"] = flight_search.get_destination_code(row["city"])
        time.sleep(2)  # Sleep to avoid hitting API rate limits

print(f"Updated sheet data:\n{sheet_data}")

# Save the updated data back to the data manager
data_manager.destination_data = sheet_data
data_manager.update_destination_codes()

# Define the search window for flights
tomorrow = datetime.now() + timedelta(days=1)
six_months_from_today = datetime.now() + timedelta(days=(6 * 30))

# Search for flights and notify about the cheapest flights
for destination in sheet_data:
    print(f"Getting flights for {destination['city']}")
    flights = flight_search.check_flights(
        ORIGIN_CITY_IATA,
        destination["iataCode"],
        from_time=tomorrow,
        to_time=six_months_from_today
    )

    # Find the cheapest flight from the returned flight data
    cheapest_flight = find_cheapest_flight(flights)

    # Check if a cheaper flight is found and notify
    if cheapest_flight.price != "N/A" and cheapest_flight.price < destination.get("lowestPrice", float('inf')):
        print(f"Lower price flight found to {destination['city']}!")

        notification_manager.send_whatsapp(
            message_body=f"Low price alert! Only £{cheapest_flight.price} to fly "
                         f"from {cheapest_flight.origin_airport} to {cheapest_flight.destination_airport}, "
                         f"on {cheapest_flight.out_date} until {cheapest_flight.return_date}."
        )
