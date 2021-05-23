import requests
PO_TOKEN = "ajnubok1byk3xumzvu74xi8gifnp6r"
PO_USER  = "u1djcrmm8zhavb4586fwn81x6vr7vx"

def send_push_notify(text):
    if PO_USER == "yourpushoveruser" or PO_USER is None:
        print("No notifications since po is not setup")
        return
    try:
        r = requests.post("https://api.pushover.net/1/messages.json", data={
            "token": PO_TOKEN,
            "user": PO_USER,
            "message": text
        })
    except Exception as err:
        print(f"Failed in pinging push notifications {err}")