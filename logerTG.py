from key import tgapi_key
import requests
def send_message(text):
    token = tgapi_key
    chat_id = '-1002015970910'

    url = f"https://api.telegram.org/bot{token}/sendMessage"

    params = {
       "chat_id": chat_id,
       "text": text,
       "parse_mode": "HTML"
    }
    requests.get(url, params=params)
