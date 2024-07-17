import requests
from datetime import datetime

# Constants
TOKEN = "your_token_here"  # replace this with actual token
HEADERS = {
    "X-USER-TOKEN": TOKEN
}
PIXELA_ENDPOINT = "https://pixe.la/v1/users"


def create_account(username, token):
    """
    Creates a new Pixela account.
    """
    user_params = {
        "token": token,
        "username": username,
        "agreeTermsOfService": "yes",
        "notMinor": "yes",
    }
    try:
        response = requests.post(url=PIXELA_ENDPOINT, json=user_params)
        response.raise_for_status()  # Raises an HTTPError if the status is 4xx, 5xx
        print("Account created successfully!")
    except requests.exceptions.HTTPError as http_err:
        print(f"HTTP error occurred: {http_err}")
    except Exception as err:
        print(f"Other error occurred: {err}")


def create_graph(username, graphid, graph_name, unit):
    """
    Creates a new graph under the specified Pixela user account.
    """
    graph_endpoint = f"{PIXELA_ENDPOINT}/{username}/graphs"
    graph_config = {
        "id": graphid,
        "name": graph_name,
        "unit": unit,
        "type": "float",
        "color": "sora",
    }
    try:
        response = requests.post(url=graph_endpoint, json=graph_config, headers=HEADERS)
        response.raise_for_status()
        print("Graph created successfully!")
    except requests.exceptions.HTTPError as http_err:
        print(f"HTTP error occurred: {http_err}")
    except Exception as err:
        print(f"Other error occurred: {err}")


def create_pixel(username, graphid, month, day, quantity):
    """
    Creates a pixel on the specified date in the specified graph.
    """
    pixel_creation_endpoint = f"{PIXELA_ENDPOINT}/{username}/graphs/{graphid}"
    today = datetime(year=datetime.now().year, month=month, day=day)
    date_str = today.strftime("%Y%m%d")
    pixel_data = {
        "date": date_str,
        "quantity": quantity,
    }
    try:
        response = requests.post(url=pixel_creation_endpoint, json=pixel_data, headers=HEADERS)
        response.raise_for_status()
        print("Pixel created successfully!")
    except requests.exceptions.HTTPError as http_err:
        print(f"HTTP error occurred: {http_err}")
    except Exception as err:
        print(f"Other error occurred: {err}")


def update_pixel(username, graphid, month, day, new_quantity):
    """
    Updates the quantity of an existing pixel on the specified date.
    """
    today = datetime(year=datetime.now().year, month=month, day=day)
    date_str = today.strftime("%Y%m%d")
    new_pixel_data = {
        "quantity": new_quantity
    }
    update_endpoint = f"{PIXELA_ENDPOINT}/{username}/graphs/{graphid}/{date_str}"
    try:
        response = requests.put(url=update_endpoint, json=new_pixel_data, headers=HEADERS)
        response.raise_for_status()
        print("Pixel updated successfully!")
    except requests.exceptions.HTTPError as http_err:
        print(f"HTTP error occurred: {http_err}")
    except Exception as err:
        print(f"Other error occurred: {err}")


def delete_pixel(username, graphid, month, day):
    """
    Deletes an existing pixel on the specified date.
    """
    today = datetime(year=datetime.now().year, month=month, day=day)
    date_str = today.strftime("%Y%m%d")
    delete_endpoint = f"{PIXELA_ENDPOINT}/{username}/graphs/{graphid}/{date_str}"
    try:
        response = requests.delete(url=delete_endpoint, headers=HEADERS)
        response.raise_for_status()
        print("Pixel deleted successfully!")
    except requests.exceptions.HTTPError as http_err:
        print(f"HTTP error occurred: {http_err}")
    except Exception as err:
        print(f"Other error occurred: {err}")

# Example usage
# Make sure to replace 'your_token_here' and provide actual 'username'
# create_account("your_username", TOKEN)
# create_graph("your_username", GRAPHID, "My Graph", "commit")
# create_pixel("your_username", GRAPHID, 7, 15, "10.1")
# update_pixel("your_username", GRAPHID, 7, 15, "70.61")
# delete_pixel("your_username", GRAPHID, 7, 15)
