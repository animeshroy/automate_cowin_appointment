import requests
import json
import time
import datetime
import pandas as pd
from flatten_json import flatten
from login import confirm_otp
from beneficiary import fetch_beneficiaries
from appointment import schedule_appointment
from push_notify import send_push_notify

today = time.strftime("%d/%m/%Y")
def check_vaccine_slots_pincode(PINCODE, AGE_LIMT):
    while True:
        #Start a session
        PINCODE_URL = f"https://cdn-api.co-vin.in/api/v2/appointment/sessions/public/calendarByPin?pincode={PINCODE}&date={today}"
        message_string =f"{today} Alert!\n\n"
        with requests.session() as session:
            headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/56.0.2924.76 Safari/537.36'}
            response = session.get(PINCODE_URL, headers=headers)

            #Receive the response
            response = response.json()
            for center in response['centers']:
                for session in center['sessions']:

                    #For Age not equal to 45 and capacity is above zero
                    if (session['min_age_limit'] == AGE_LIMT) & (session['available_capacity'] > 0) & (session['available_capacity_dose1'] > 0):
                        message_string=f"\nAvailable - {session['available_capacity']} in {center['name']} on {session['date']} for the age {session['min_age_limit']}+"
                        send_push_notify(message_string)
                        bearer_token = confirm_otp()
                        benficiary_data =  fetch_beneficiaries(bearer_token['token'])
                        session_data = session
                        benficiaries_id_list = [benficiary_data['beneficiary_reference_id'] for benef in benficiary_data]
                        response_appoint =schedule_appointment(session_data, bearer_token, benficiaries_id_list)
                        send_push_notify(json.dumps(response_appoint))
            time.sleep(1000)

def fetch_state_district(state_code):
    url_state = f"https://cdn-api.co-vin.in/api/v2/admin/location/districts/{state_code}"
    with requests.session() as session:
            headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/56.0.2924.76 Safari/537.36'}
            response = session.get(url_state, headers=headers)
            response = response.json()
    return response['districts']

def generate_msg_district_wise(slot_df, district_id=None, top=10):
    if district_id == None:
        top_df = slot_df.sort_values(by="available_capacity")
        district_id = list(top_df.head(1)['district_id'])[0]
    if slot_df.shape[0] == 0:
        return f"{today} No Slots available!!\n\n", None
    else:
        message_string = f"{today} Alert!\n\n"
    dist_df = slot_df[slot_df['district_id']==district_id]
    dist_df = dist_df.sort_values(by="available_capacity")
    dist_df = dist_df.head(top)
    if dist_df.shape[0] == 0:
        return f"{today} No Slots available!!\n\n", None
    else:
        message_string = f"{today} Alert!\n\n"
        session_ids = dist_df[["session_id","slots_0","slots_1","slots_2"]]

    for row_index in dist_df.index:
            message_string+=f"\nAvailable - {dist_df.loc[row_index, 'available_capacity']} in {dist_df.loc[row_index, 'district_name']}>{dist_df.loc[row_index, 'name']} on {dist_df.loc[row_index, 'date']} for the age {dist_df.loc[row_index, 'min_age_limit']}+"
    return message_string, session_ids

def book_appoinment(session_ids):
    bearer_token = confirm_otp()
    bearer_token = bearer_token['token']
    benficiary_data =  fetch_beneficiaries(bearer_token)
    for index, row in session_ids.iterrows():
        session_data = {"session_id":row["session_id"], "slots":[row["slots_0"], row["slots_1"], row["slots_2"]]}
        benficiaries_id_list = [benef['beneficiary_reference_id'] for benef in benficiary_data['beneficiaries']]
        response_appoint, status = schedule_appointment(session_data, bearer_token, benficiaries_id_list)
        if status:
            send_push_notify(json.dumps(response_appoint))
            break
    return

def check_vaccine_slots_state(state_code, AGE_LIMT, district_id_inp=None):
    if district_id_inp is None:
        districts_data = fetch_state_district(state_code)
    else:
        districts_data = [{'district_id':district_id_inp, 'district_name':district_id_inp}]
    while True:
        #Start a session
        slots_data=[]
        for district in districts_data:
            district_id = district['district_id']
            url_district = f"https://cdn-api.co-vin.in/api/v2/appointment/sessions/public/calendarByDistrict?district_id={district_id}&date={today}"
            with requests.session() as session:
                headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/56.0.2924.76 Safari/537.36'}
                response = session.get(url_district, headers=headers)

                #Receive the response
                response = response.json()
                for center in response['centers']:
                    center['district_name'] = district['district_name']
                    center['district_id'] = district['district_id']
                    for session in center['sessions']:
                        if (session['min_age_limit'] == AGE_LIMT) & (session['available_capacity'] > 0) & (session['available_capacity_dose1'] > 0):
                            session_data = {**center, **session}
                            del session_data['sessions']
                            session_data = flatten(session_data)
                            slots_data.append(session_data)
        slot_df = pd.DataFrame.from_dict(slots_data)
        slot_df.to_csv('slot_data.csv')
        message_string, session_ids = generate_msg_district_wise(slot_df, district_id=district_id_inp)
        send_push_notify(message_string)
        if session_ids is not None:
            send_push_notify("Booking appointment!!!")
            book_appoinment(session_ids)
        time.sleep(60)