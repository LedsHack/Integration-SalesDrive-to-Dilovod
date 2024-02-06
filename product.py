#Code 25.11.24(edit), By LedsHack@
from sendPacket import send

#Пошук продукту за його артикулем
def search(productNum):
    packet = {
        'action': 'request',
        'params': {
            'from': 'catalogs.goods',
            'fields': {
                "productNum": "productNum",
                "id": "id",
                "mainUnit": "mainUnit",
            },
            "filters": [
                {
                    "alias": "productNum",
                    "operator": "=",
                    "value": productNum
                }
            ]
        }
    }
    return(send(packet))

# [{'productNum': '123', 'id': '1100300000001002', 'id__pr': 'Тепла підлога', 'mainUnit': '1103600000000001', 'mainUnit__pr': '[access restricted]'}] <- Знайдено
# [] <- не знайдено