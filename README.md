# automate_cowin_appointment
1. Create account at https://pushover.net/ and then create API token with any name,description at https://pushover.net/apps/build
2. Install pushover app from playstore/app store in mobile and login.
3. Open .env file in notepad and Add "Your User Key" from https://pushover.net/ in PO_USER and the API token in PO_TOKEN in config.env
4. To test if its working, it should send "Program Started" message when you run docker-compose up flipkartbot
5. Make sure you set "Battery Optimization" for pushover app to "Dont Optimize", otherwise you may miss notifcations

6. For Running the script do the following steps:

7. pip3 install -r requirments.txt
8. Python3 main.py

Note: check_vaccine_slots_state(state_code=16, district_id_inp=265, AGE_LIMT=18)
give input for state_code, district_code, minimum_age_limt
state_code and district codes can found at ~\Resources\Postman API Collection GET States and GET District
