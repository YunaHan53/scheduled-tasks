import os
import requests
from twilio.rest import Client
from twilio.http.http_client import TwilioHttpClient

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
print(f"HTTP Status: {status}")

will_rain = False

weather_list = data["list"]
for item in weather_list:
    date_time = item["dt_txt"]
    date = date_time.split(" ")[0]
    time = date_time.split(" ")[1]
    weather = item["weather"]
    weather_id = weather[0]["id"]

    if weather_id < 700:
        description = weather[0]["description"]
        will_rain = True

if will_rain:
    proxy_client = TwilioHttpClient()
    proxy_client.session.proxies = {'https': os.environ['https_proxy']}

    client = Client(account_sid, auth_token, http_client=proxy_client)
    message = client.messages.create(
        from_="whatsapp:+14155238886",
        body=f"There will be {description} today. Remember to bring an ☔",
        to="whatsapp:+18572588770"
    )
    print(message.status)
