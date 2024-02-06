import requests, json
from key import api_dilovod

def send(packet):
    url = "https://api.delovod.ua"

    header = {
        'Content-type': 'application/x-www-form-urlencoded'
    }

    setting = {
        'version': '0.2',
        'key': api_dilovod
    }

    packet = "packet=" + str(json.dumps({**packet, **setting}))
    return(json.loads(requests.post(url=url, data=packet, headers=header).text))