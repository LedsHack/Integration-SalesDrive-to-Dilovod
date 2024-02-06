#Code 25.11.24(edit), By LedsHack@
from sendPacket import send

#Пошук торговельних канлів за назвою
def search(name):
    packet = {
        'action': 'request',
        'params': {
            'from': 'catalogs.tradeChanels',
            'fields': {
                "name": "name",
                "id": "id"
            },
            "filters": [
                {
                    "alias": "name",
                    "operator": "%",
                    "value": name
                }
            ]
        }
    }
    return(send(packet))

# [{'name': 'Elitteplo', 'id': '1103200000001001', 'id__pr': 'Elitteplo'}] <- Успіх
# [] <- Не знайдено
