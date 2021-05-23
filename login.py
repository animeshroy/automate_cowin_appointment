import requests,sys
import json, hashlib

from beneficiary import fetch_beneficiaries
MOBILE_NUMBER = "8851291302"
SECRET = "U2FsdGVkX19c2O9OPUj6mWKByx2VtEUJl4tsdCfHD3t4L4r5Nm1qIQRL7y6JhEf3vf6NBZveF00tMfHnP/16Og==" #Check from browser network @https://cdn-api.co-vin.in/api/v2/auth/generateMobileOTP call

def generate_otp():
    GENERATE_URL = "https://cdn-api.co-vin.in/api/v2/auth/generateMobileOTP"
    with requests.session() as session:
        headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/56.0.2924.76 Safari/537.36'}
        data = {'mobile':MOBILE_NUMBER, 'secret':SECRET}
        response = session.post(GENERATE_URL, headers=headers, data=json.dumps(data))
        response = response.json()
    print(response)
    return response

def confirm_otp(retry = 0):
    CONFIRM_OTP = "https://cdn-api.co-vin.in/api/v2/auth/validateMobileOtp"
    data = generate_otp()
    print("OTP send to your registered mobile number")
    otp_number = input("\nEnter OTP:: ")
    otp_number = hashlib.sha256(str(otp_number).encode())
    enrcypted_otp = otp_number.hexdigest()
    with requests.session() as session:
        headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/56.0.2924.76 Safari/537.36'}
        otp = {'otp':enrcypted_otp}
        otp_data ={**data, **otp}
        response = session.post(CONFIRM_OTP, headers=headers, data=json.dumps(otp_data))
        if response.status_code == 401:
            print("incorrect OTP retry again..")
            if retry > 2:
                print("3 Retires exhuasted..try again later")
                sys.exit()
            response = confirm_otp(retry+1)
        else:
            response = response.json()
    print(response)
    return response

