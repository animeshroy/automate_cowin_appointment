import requests
import json


def fetch_beneficiaries(bearer_token):
    BENEFICIARY_URL = "https://cdn-api.co-vin.in/api/v2/appointment/beneficiaries"
    try:
        with requests.session() as session:
            headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/56.0.2924.76 Safari/537.36', 'Authorization':'Bearer '+ bearer_token}
            response = session.get(BENEFICIARY_URL, headers=headers)
            if response.status_code != 200:
                response = fetch_beneficiaries(bearer_token)
            else:
                response = response.json()
        return response
    except:
        return fetch_beneficiaries(bearer_token)