#Code 25.11.24(edit), By LedsHack@
from sendPacket import send

#Пошук обєкта покупця за номер телефона
def search(phone):
    packet = {
        'action': 'request',
        'params': {
            'from': 'catalogs.persons',
            'fields': {
                "name": "name",
                "id": "id",
                "phone": "phone"
            },
            "filters": [
                {
                    "alias": "name",
                    "operator": "%",
                    "value": phone #Tелефон записано в назву замовлення
                }
            ]
        }
    }
    return(send(packet))
# [{'name': '0985971234 Валентина Іващенко', 'id': '1100100000001022', 'id__pr': '0985971234 Валентина Іващенко', 'phone': '0985971234'}] <- Знайдено
# [] <- Не знайдено

def create(pib, phone, email = ""):
    packet = {
        'action': "saveObject",
        'params': {
            'header': {
                'id': 'catalogs.persons',
                'name':{
                    'uk':  phone + " " + pib,
                    'ru':  phone + " " + pib #Нехай учать, уже прийшов той час
                },
                "details": "{\"phones\":[{\"pr\":\""+phone+"\",\"kind\":\"phone\"}],\"emails\":[{\"pr\":\""+email+"\",\"kind\":\"email\"}],\"messengers\":[],\"urls\":[],\"attributes\":[],\"notes\":[]}"

            }
        }
    }
    return (send(packet))
# {'result': 'ok', 'id': '1100100000001026'} <- Успіх
# Ну я навіть не знаю що потрібно робити щоб була помилка