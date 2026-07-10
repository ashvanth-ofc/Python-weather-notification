from plyer import notification
import requests

city = 'indore' ## Change city name here

w_codes = {0:'Clear sky',1:'Mainly clear',2:'Partly cloudy',3:'Overcast',
           45:'Fog',48:'Depositing rime fog',51:'Light Drizzle',
           53:'Moderate Drizzle',55:'Heavy Drizzle',56:'Light Freezing drizzle',
           57:'Heavy Freezing dizzle',61:'Light Rain',63:'Moderate Rain',
           65:'Heavy Rain',66:'Light Freezing rain',67:'Heavy Freezing Rain',
           71:'Light Snowfall',73:'Moderate Snowfall',75:'Heavy Snowfall',
           77:'Snow grains',80:'Light Rain shower',81:'Moderate Rain shower',
           82:'Violent Rain shower',85:'Light Snow Shower',86:'Heavy Snow Shower',
           95:'Thunderstrom',96:'Thunderstorm with light hail',99:'Thunderstorm with heavy hail'}

def findweather(city):   
    #Find latitude and longitude of city
    geocode = requests.get('https://geocoding-api.open-meteo.com/v1/search',params={'name':city,'count':1}).json()
    lat,long = geocode['results'][0]['latitude'],geocode['results'][0]['longitude']
    #finding weather
    weather = requests.get("https://api.open-meteo.com/v1/forecast",params={"latitude": lat,"longitude": long,"current_weather": True}).json()
    temp = weather["current_weather"]["temperature"]
    wind = weather["current_weather"]["windspeed"]
    wind_direction = weather["current_weather"]["winddirection"]
    code = weather['current_weather']['weathercode']
    return temp,wind,wind_direction,code


def send_notification(city):
    temp,wind,wind_direction,code = findweather(city)
    #Converting Wind direction Degrees-->compass directions
    directions = ["North", "North-East", "East", "South-East", "South", "South-West", "West", "North-West"]
    index = round(wind_direction / 45) % 8
    #Creating the message to be displayed
    message = f"Weather: {w_codes.get(code,'Unknown')}\nTemperature: {temp}°C\nWind: {wind}km/h ({directions[index]})\n"
    #Sending Notification
    notification.notify(title=f'Weather in {city.title()}\n',message=message,timeout=5)
while True:
   try:
        city = input('Enter city name: ')
        if city.lower() == 'exit':
            break
        send_notification(city)
   except:
        print("An error occured")
   finally:
        print("Program Executed")
