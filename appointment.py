import json, requests
from recaptcha import  fetch_captcha

def schedule_appointment(session_data, bearer_token, beneficiaries_id, slot_preference = 0):
    dose = 1
    if slot_preference == 0:
        slot_list = ["09:00AM-12:00PM"]
    else:
        slot_list = session_data['slots']

    APPOINT_URL = "https://cdn-api.co-vin.in/api/v2/appointment/schedule"
    for slot in slot_list:
        captcha = fetch_captcha(bearer_token)
        appoint_data = {'dose':dose, 'session_id':session_data['session_id'], 'slot':slot, 'beneficiaries':beneficiaries_id, 'captcha':captcha}
        with requests.session() as session:
            headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/56.0.2924.76 Safari/537.36', 'Authorization':'Bearer '+ bearer_token}
            response = session.post(APPOINT_URL, headers=headers, data=json.dumps(appoint_data))
            if response.status_code == 500:
                response = response.json()
                print(f"\nCongratulations your appointment is booked with appointment_confirmation_no{response['appointment_confirmation_no']}")
                return response, 1
            else:
                print((f"\nCould not book slot for appointment....:( {response.text}"))
                slot_not_found = True
                continue
    if slot_not_found:
        return response, 0
    #return response
