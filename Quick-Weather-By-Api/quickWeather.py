import json
import requests
import sys
import pprint

'''
quickWeather.py - Prints the current weather for a location from the command line.

天气API：
http://www.haoservice.com


'''

# Compute location from command line arguments.
if len(sys.argv) < 2:
    print('Usage: quickWeather.py location in terminal')
    print('For example: python3 quickWeather.py 北京')
    sys.exit()
location = ' '.join(sys.argv[1:])

# Download the JSON data from OpenWeatherMap.org's API
url ='http://apis.haoservice.com/weather?cityname=%s&key=13d0b795ddf64ad59a9989016e9ac3b0' % (location)
response = requests.get(url)
response.raise_for_status()

# Load JSON data into a Python variable.
weatherData = json.loads(response.text)


pprint.pprint(weatherData)  # 输出字典
