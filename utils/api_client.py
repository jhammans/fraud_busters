import requests
import sys


def fetch_api_data(url, params=None, headers=None, method="GET", timeout=60):
    """Function to fetch data from a specified URL with given parameters"""
    try:
        # Perform the HTTP request based on the specified method
        if method.upper() == "GET":
            response = requests.get(url, params=params, headers=headers, timeout=timeout)
        elif method.upper() == "POST":
            response = requests.post(url, data=params, headers=headers, timeout=timeout)
        elif method.upper() == "PUT":
            response = requests.put(url, data=params, headers=headers, timeout=timeout)
        elif method.upper() == "DELETE":
            response = requests.delete(url, params=params, headers=headers, timeout=timeout)
        else:
            # Handle unsupported HTTP methods
            print(f"HTTP method {method} is not supported.")
            sys.exit()

        # Raise an exception for HTTP error responses
        response.raise_for_status()
    except requests.exceptions.HTTPError as errh:
        # Handle HTTP errors
        print(f"Http Error: {errh}")
        sys.exit()
    except requests.exceptions.ConnectionError as errc:
        # Handle connection errors
        print(f"Error Connecting: {errc}")
        sys.exit()
    except requests.exceptions.Timeout as errt:
        # Handle timeout errors
        print(f"Timeout Error: {errt}")
        sys.exit()
    except requests.exceptions.RequestException as err:
        # Handle any other request exceptions
        print(f"Unexpected Error: {err}")
        sys.exit()

    # Parse the response content as JSON
    try:
        jsonData = response.json()
    except ValueError:
        # Handle cases where the response is not valid JSON
        print("Response content is not valid JSON")
        sys.exit()

    return jsonData