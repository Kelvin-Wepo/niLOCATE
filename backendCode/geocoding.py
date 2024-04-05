import os

import requests
from urllib.parse import urlencode
from pprint import pprint
from django.conf import settings

api_key = settings.GOOGLE_API_KEY


# def geocoding_from_address(address):
#     endpoint = "https://maps.googleapis.com/maps/api/geocode/json"
#     params = {"address": address, 'region': 'ke', "key": api_key}
    
#     url_params = urlencode(params)

#     url = f"{endpoint}?{url_params}"
#     req = requests.get(url)
#     formatted_address = req.json()['results'][0]['formatted_address']
#     lat = req.json()['results'][0]['geometry']['location']['lat']
#     lng = req.json()['results'][0]['geometry']['location']['lng']
#     # print(formatted_address)
#     # print(lat)
#     # print(lng)
#     data = {
#         'formatted_address': formatted_address,
#         'lat': lat,
#         'lng': lng
#     }
#     print(data)
#     return data


def geocoding_from_address(address):
    endpoint = "https://maps.googleapis.com/maps/api/geocode/json"
    params = {"address": address, "region": "ke", "key": api_key}

    url_params = urlencode(params)
    url = f"{endpoint}?{url_params}"

    try:
        req = requests.get(url)
        req.raise_for_status()  # Raise an exception for 4xx/5xx status codes
        results = req.json().get("results", [])
        if results:
            first_result = results[0]
            formatted_address = first_result.get("formatted_address")
            location = first_result.get("geometry", {}).get("location", {})
            lat = location.get("lat")
            lng = location.get("lng")
            data = {"formatted_address": formatted_address, "lat": lat, "lng": lng}
            return data
        else:
            print("No results found")
            return None
    except requests.exceptions.HTTPError as err:
        print(f"HTTP error occurred: {err}")
        return None
    except requests.exceptions.RequestException as e:
        print(f"An error occurred: {e}")
        return None


# p = geocoding_from_address('Kencom bustop')
# print(p)

# def reverse_geocoding(latlang):
#     endpoint = f"https://maps.googleapis.com/maps/api/geocode/json"
#     url = f"{endpoint}?latlng={latlang}&key={api_key}"
#     req = requests.get(url)
#     address = req.json()['results'][0]['formatted_address']
#     return address


def reverse_geocoding(latlng):
    endpoint = "https://maps.googleapis.com/maps/api/geocode/json"
    params = {
        "latlng": latlng,
        "key": settings.GOOGLE_API_KEY
    }
    try:
        response = requests.get(endpoint, params=params)
        response.raise_for_status()
        data = response.json()
        if 'results' in data and len(data['results']) > 0:
            return data['results'][0]['formatted_address']
    except requests.exceptions.RequestException as e:
        print(f"Error: {e}")
    return None



# add = reverse_geocoding('23.7465882,90.3846205')
# print(add)
