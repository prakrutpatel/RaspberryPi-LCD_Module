#Send weather data to the server

import requests,json
import socket

ClientSocket = socket.socket()
host='127.0.0.1'
port = 1233


try:
    ClientSocket.connect((host, port))
except socket.error as e:
    print(str(e))

#Make an API call using openweathermap.org API key
#Replace {API Key} with your own API key
#Replace {city} with a city of your choice in the format St+Petersburg incase of a city with more than one word
url = 'http://api.openweathermap.org/data/2.5/weather?appid={API Key}&q={city}'
weather_data = requests.get(url).json()

weather_dat = weather_data['weather'][0]['main']
temp = int(weather_data['main']['temp']-273.15)
first="    Forecast"
second=str(weather_dat)+' '+str(temp)+'C'
message = {
    "1": first,
    "2": second,
    "time": 5,
    "priority": "Low"
}
data=json.dumps(message)
ClientSocket.send(bytes(data,"utf-8"))

ClientSocket.close()
