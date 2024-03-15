import requests
import os
from dotenv import load_dotenv
from datetime import datetime

load_dotenv()

# ----------------------- Syndigo nutrition API ----------------------- #
# The syndigo API can turn natural language into an exercise with duration, calories burned

app_id = os.getenv('APP_ID')
api_key = os.getenv('API_KEY')
api_endpoint = 'https://trackapi.nutritionix.com/v2/natural/exercise'

user_activity = input("What activity did you do?: ")

exercise_config = {
    "query": user_activity
}
header = {
    "x-app-id": app_id,
    "x-app-key": api_key
}

response = requests.post(url=api_endpoint, headers=header, json=exercise_config)
data = response.json()

# ----------------------- Sheety API ----------------------- #
# The Sheety API can post data into Google Sheets, so
# user natural lanuguage -> Syndigo API -> Google Sheets workout info
sheety_url = os.getenv("SHEETY_URL")

for exercise in data["exercises"]:
    today = datetime.now()
    header = {
        "Authorization": os.getenv("SHEETY_AUTH")
    }
    workout_parameters = {
        "workout": {
            "date": today.strftime('%x'),
            "time": today.strftime('%X'),
            "exercise": exercise['user_input'].title(),
            "duration": exercise['duration_min'],
            "calories": exercise['nf_calories']
        }
    }
    response = requests.post(url=sheety_url, headers=header, json=workout_parameters)
    print(response.text)