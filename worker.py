#Code 25.11.s24 (edit), By LedsHack@
from sendPacket import send

#Поиск работника по имени (Стейджу)
def search(stage):
    packet = {
        'action': 'request',
        'params': {
            'from': 'catalogs.employees',
            'fields': {
                "name": "name",
                "id": "id",
            },
            "filters": [
                {
                    "alias": "name",
                    "operator": "=",
                    "value": stage
                }
            ]
        }
    }
    return(send(packet))

# [{'name': 'Назар', 'id': '1101700000001001', 'id__pr': 'Назар'}] <- Найдено
# [] <- Не найдено