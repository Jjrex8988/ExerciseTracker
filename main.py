## https://docs.google.com/document/d/1_q-K-ObMTZvO0qUEAxROrN3bwMujwAN25sLHwJzliK0/edit#

import requests
from datetime import datetime
import os

GENDER = 'FEMALE'
WEIGHT_KG = 50
HEIGHT_CM = 165
AGE = 25

APP_ID = os.environ["NT_APP_ID"]  ## Sample only, please change it by register yourself via
# https://developer.nutritionix.com/
API_KEY = os.environ["NT_API_KEY"]  ## Register and get API keys

exercise_endpoint = "https://trackapi.nutritionix.com/v2/natural/exercise"
sheet_endpoint = os.environ["SHEET_ENDPOINT"]  ## Create your own project https://dashboard.sheety.co/login

exercise_text = input("Tell me which exercises you did: ")

headers = {
    "x-app-id": APP_ID,
    "x-app-key": API_KEY,
}

parameters = {
    "query": exercise_text,
    "gender": GENDER,
    "weight_kg": WEIGHT_KG,
    "height_cm": HEIGHT_CM,
    "age": AGE
}

response = requests.post(exercise_endpoint, json=parameters, headers=headers)
result = response.json()
print(result)

today_date = datetime.now().strftime("%d/%m/%Y")
now_time = datetime.now().strftime("%X")

for exercise in result["exercises"]:  # https://sheety.co/docs/requests
    sheet_inputs = {
        "workout": {
            "date": today_date,
            "time": now_time,
            "exercise": exercise["name"].title(),
            "duration": exercise["duration_min"],
            "calories": exercise["nf_calories"]
        }
    }

    # No Auth
    sheet_response = requests.post(sheet_endpoint, json=sheet_inputs)

    # Basic Auth (https://sheety.co/docs/authentication.html)
    sheet_response = requests.post(
        sheet_endpoint,
        json=sheet_inputs,
        auth=(
            os.environ["USERNAME"],
            os.environ["PASSWORD"],
        )
    )

    # Bearer Token (https://sheety.co/docs/authentication.html)
    bearer_headers = {
        "Authorization": f"Bearer {os.environ['TOKEN']}"
    }
    sheet_response = requests.post(
        sheet_endpoint,
        json=sheet_inputs,
        headers=bearer_headers
    )

    print(sheet_response.text)
