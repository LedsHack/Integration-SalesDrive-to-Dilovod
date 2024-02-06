#Code 25.11.24, By LedsHack@

from sendPacket import send
from setting import setting

#Установка значения (айди с CRM)
def set(id, value):
    packet = {
        'action': 'saveObject',
        'params': {
            'header': {
                'id': 'informationRegisters.propValues',
                "object": id,
                "propKind": setting["propKind"],
                "strValue": value
            }
        }
    }
    return(send(packet))
#{'error': 'cant set value of header.object: bad value, or field doesnt exist', 'clientMessages': []} <- Помилка(не вірний Айди)
#{'result': 'ok', 'id': 0} <- Усіх


#Поиск обєкта заявки за знанчением доп поля в заявках
def search(value):
    packet = {
        'action': 'request',
        'params': {
            'from': 'informationRegisters.propValues',
            'fields': {
                "object": "id",
                "strValue": "strValue",
                "propKind": "propKind"
            },
            "filters": [
                {
                    "alias": "strValue",
                    "operator": "=",
                    "value": value
                },
                {
                    "alias": "propKind",
                    "operator": "=",
                    "value": setting["propKind"]
                }
            ]
        }
    }
    return(send(packet))

# [{'id': '1109100000001002', 'id__pr': '20.01.2024 Замовлення 0000000002', 'strValue': 'huy', 'propKind': '1114600000001001', 'propKind__pr': '[access restricted]'}] <- Знайдено
# [] <- Не знайдено