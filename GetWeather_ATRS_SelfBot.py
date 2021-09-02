import sys
import subprocess


def pip_install(module: str):
    subprocess.run([sys.executable, "-m", "pip", "-q", "--disable-pip-version-check", "install", module])


try:
    from bs4 import BeautifulSoup
except:
    print("'bs4' module not found! Trying to install... [GetWeather_Lexi]")
    pip_install("bs4")
    from bs4 import BeautifulSoup

try:
    import requests
except:
    print("'requests' module not found! Trying to install... [GetWeather_Lexi]")
    pip_install("requests")
    import requests

try:
    import re
except:
    print("'re' module not found! Trying to install... [GetWeather_Lexi]")
    pip_install("re")
    import re

try:
    import urllib.request
except:
    print("'urllib' module not found! Trying to install... [GetWeather_Lexi]")
    pip_install("urllib")
    import urllib.request

try:
    import json
except:
    print("'json' module not found! Trying to install... [GetWeather_Lexi]")
    pip_install("json")
    import json


class GetWeather:
    def __init__(self):
        self.city = None
        self.api_key = None
        self.weather_description = None
        self.temperature = None
        self.feels_like = None
        self.current_temp_min = None
        self.current_temp_max = None
        self.atmospheric_pressure = None
        self.humidity = None
        self.visibility = None
        self.wind = None
        self.wind_gust = None
        self.clouds_cover = None
        self.location = None
        self.time = None
        self.source = None
        self.wind_direction = None

    def basic_weather(self, city):
        city = str(city)
        try:
            url = "https://www.google.com/search?q=weather+in+" + city.replace(" ", "+")

            r = requests.get(url)
            htmlcontent = r.content
            html_content = BeautifulSoup(htmlcontent, "html.parser")

            location = str(html_content.find("span", class_="BNeawe tAd8D AP7Wnd"))
            location = re.sub(r"(<.*?>)*", "", location)

            temperature = str(html_content.find("div", class_="BNeawe iBp4i AP7Wnd"))
            temperature = re.sub(r"(<.*?>)*", "", temperature)

            description = str(html_content.find("div", class_="BNeawe tAd8D AP7Wnd"))
            description = re.sub(r"(<.*?>)*", "", description).split("\n")

            time = description[0]
            weather_description = description[1]

            if location is None or temperature is None or description is None or description is None:
                raise Exception("Something went wrong. No weather details fetched. ")

            self.city = city
            self.api_key = None
            self.weather_description = weather_description
            self.temperature = temperature
            self.feels_like = None
            self.current_temp_min = None
            self.current_temp_max = None
            self.atmospheric_pressure = None
            self.humidity = None
            self.visibility = None
            self.wind = None
            self.wind_gust = None
            self.clouds_cover = None
            self.location = location
            self.time = time
            self.source = "The Weather Channel"
            self.wind_direction = None
        except:
            raise Exception("Something went wrong. No weather details fetched. ")

    def detailed_weather(self, city, api_key):
        city = str(city)
        api_key = str(api_key)
        try:
            def direction(degree):
                val = int((degree / 22.5) + .5)
                directions = ["N", "NNE", "NE", "ENE", "E", "ESE", "SE", "SSE", "S", "SSW", "SW", "WSW", "W", "WNW", "NW",
                              "NNW"]
                return directions[(val % 16)]

            url = "https://api.openweathermap.org/data/2.5/weather?q=" + city + "&units=metric&appid=" + api_key

            details = urllib.request.urlopen(url).read().decode()
            json_results = json.loads(details)

            if int(json_results["cod"]) == 200:
                weather_description = str(
                    json_results["weather"][0]["main"] + " (" + json_results["weather"][0]["description"] + ") ")
                temperature = str(int(json_results["main"]["temp"])) + "°C"
                feels_like = str(int(json_results["main"]["feels_like"])) + "°C"
                current_temp_min = str(int(json_results["main"]["temp_min"])) + "°C"
                current_temp_max = str(int(json_results["main"]["temp_max"])) + "°C"
                atmospheric_pressure = str(json_results["main"]["pressure"]) + " mb"
                humidity = str(json_results["main"]["humidity"]) + "%"
                visibility = str(int(int(json_results["visibility"]) / 1000)) + " Km"
                wind_direction = str(direction(int(json_results["wind"]["deg"])))
                wind = str(int(float(json_results["wind"]["speed"]) * 3.6)) + " Km/h"
                wind_gust = str(int(float(json_results["wind"]["gust"]) * 3.6)) + " Km/h"
                clouds_cover = str(json_results["clouds"]["all"]) + "%"
                location = str(json_results["name"])
            else:
                raise Exception(
                    "Something went wrong. No weather details fetched. Seems like not authorized with given API Key. ")

            self.city = city
            self.api_key = api_key
            self.weather_description = weather_description
            self.temperature = temperature
            self.feels_like = feels_like
            self.current_temp_min = current_temp_min
            self.current_temp_max = current_temp_max
            self.atmospheric_pressure = atmospheric_pressure
            self.humidity = humidity
            self.visibility = visibility
            self.wind = wind
            self.wind_gust = wind_gust
            self.clouds_cover = clouds_cover
            self.location = location
            self.time = None
            self.source = "OpenWeatherMap"
            self.wind_direction = wind_direction
        except:
            raise Exception("Something went wrong. No weather details fetched. Seems like not authorized with given "
                            "API Key. ")
