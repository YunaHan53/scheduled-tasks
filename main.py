import os
import requests
from twilio.rest import Client

OW_Endpoint = "https://api.openweathermap.org/data/2.5/forecast"
api_key = os.environ.get("OW_API_KEY")
account_sid = os.environ.get("ACCT_SID")
auth_token = os.environ.get("AUTH_TOKEN")

weather_params = {
    "lat": 35.7721,
    "lon": -78.6386,
    "cnt": 4,
    "appid": api_key,
}

response = requests.get(OW_Endpoint, params=weather_params)
status = response.status_code
response.raise_for_status()

data = response.json()
will_rain = False

weather_list = data["list"]
for item in weather_list:
    date_time = item["dt_txt"]
    date = date_time.split(" ")[0]
    hour = int(date_time.split(" ")[1].split(":")[0])
    est_hour = (hour-5)
    if est_hour > 12:
        est_hour -= 12
        est_hour = f"{est_hour}PM"
    else:
        est_hour = f"{est_hour}AM"

    weather = item["weather"]
    weather_id = weather[0]["id"]

    if weather_id < 700:
        description = weather[0]["description"]
        will_rain = True
        break

if will_rain:
    client = Client(account_sid, auth_token)
    message = client.messages.create(
        from_="whatsapp:+14155238886",
        body=f"There will be {description} today at {est_hour}. Remember to bring an ☔",
        to="whatsapp:+18572588770"
    )
    print(message.status)
