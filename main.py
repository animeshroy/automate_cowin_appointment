
#Import Libraries
from cowin_session import check_vaccine_slots_pincode, check_vaccine_slots_state

PINCODE  = "110075"
#Public API source is Cowin API - https://apisetu.gov.in/public/api/cowin

if __name__ =="__main__":
    #check_vaccine_slots_pincode(PINCODE, AGE_LIMT)
    check_vaccine_slots_state(state_code=16, district_id_inp=265, AGE_LIMT=18)#Karnataka Bangalore Urban
    #check_vaccine_slots_state(state_code=34, district_id_inp=637, AGE_LIMT=18)#UP Bariely
