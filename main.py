import os
import requests
from twilio.rest import Client

OWM_ENDPOINT = "https://api.openweathermap.org/data/2.5/onecall"

API_KEY = os.getenv("OWM_API_KEY")  # ✅ 환경변수명을 명확하게
ACCOUNT_SID = os.getenv("TWILIO_ACCOUNT_SID") or "ACb6660dee953c939f597514e4a767c01c"
AUTH_TOKEN = os.getenv("TWILIO_AUTH_TOKEN")

lat = 51.5085
lon = -0.1257

if not API_KEY:
    raise SystemExit("환경변수 OWM_API_KEY 가 없습니다. PowerShell에서 설정 후 다시 실행하세요.")
if not AUTH_TOKEN:
    raise SystemExit("환경변수 TWILIO_AUTH_TOKEN 가 없습니다.")

weather_params = {
    "lat": lat,
    "lon": lon,
    "appid": API_KEY,
    "exclude": "current,minutely,daily",
    "units": "metric",
}

response = requests.get(OWM_ENDPOINT, params=weather_params, timeout=20)
response.raise_for_status()
weather_data = response.json()

will_rain = any(hour["weather"][0]["id"] < 700 for hour in weather_data["hourly"][:48])

if will_rain:
    print("Bring an umbrella")
    client = Client(ACCOUNT_SID, AUTH_TOKEN)
    message = client.messages.create(
        body="It is going to rain today, bring an umbrella",
        from_="+12027967893",
        to="+447852234889",
    )
    print(message.status)
else:
    print("No rain expected")
