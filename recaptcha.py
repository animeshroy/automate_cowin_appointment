import json, requests, re

def fetch_captcha(bearer_token):
    RECAPTCHA_URL = "https://cdn-api.co-vin.in/api/v2/auth/getRecaptcha"
    try:
        with requests.session() as session:
            headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/56.0.2924.76 Safari/537.36', 'Authorization':'Bearer '+ bearer_token}
            response = session.get(RECAPTCHA_URL, headers=headers)
            if response.status_code == 200:
                response = response.json()
                #print(f"\nCongratulations your appointment is booked with appointment_confirmation_no{response['appointment_confirmation_no']}")
                xml_data = response['captcha']
                xml_data = re.sub(r"[\]","",xml_data)
                file_name = "_captcha.html"
                with open(file_name,"w+") as fw:
                    fw.write(xml_data)
                captcha_text = input(f"\nPlease enter the captcha text found @{file_name}")
                return captcha_text
            else:
                raise Exception
    except:
        fetch_captcha(bearer_token)