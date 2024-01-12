from .keys import PEXELS_API_KEY, OPEN_WEATHER_API_KEY
import requests
import json
def get_photo_url(query):
# Create a dictionary for the headers to use in the request
    # Create the URL for the request with the city and state
    url = f"https://api.pexels.com/v1/search?query={query}"

    headers= {
        "AUTHORIZATION": PEXELS_API_KEY
    }

    response = requests.get(url, headers=headers)._content

    api_dic = json.loads(response)

    print(api_dic)
    return api_dic['photos'][0]['src']['original']
    # Make the request

    # Parse the JSON response

    # Return a dictionary that contains a `picture_url` key and
    #   one of the URLs for one of the pictures in the response



def get_weather_data(city,state):

     # Create the URL for the geocoding API with the city and state
    geocoding_url = f"http://api.openweathermap.org/geo/1.0/direct?q={city},{state}&appid={OPEN_WEATHER_API_KEY}"
    # Make the request
    response = requests.get(geocoding_url)
    # Parse the JSON response
    api_dict = response.json()
    # Get the latitude and longitude from the response
    lat = api_dict[0]["lat"]
    lon = api_dict[0]["lon"]

    # Create the URL for the current weather API with the latitude
    #   and longitude
    weather_url = f"https://api.openweathermap.org/data/2.5/weather?lat={lat}&lon={lon}&appid={OPEN_WEATHER_API_KEY}"
    # Make the request
    weather_response = requests.get(weather_url)
    # Parse the JSON response
    weather_dict = json.loads(weather_response.content)
    # Get the main temperature and the weather's description and put
    #   them in a dictionary


    # Return the dictionary
    temp_dict = {
        "weather": weather_dict["weather"][0]["main"],
        "temp": weather_dict["main"]["temp"],
    }
    return temp_dict
