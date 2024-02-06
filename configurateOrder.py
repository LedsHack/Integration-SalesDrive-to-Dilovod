import logerTG as log
import json
from product import search as ProductSearch

def Order(get, phone):
    result = []
    if(len(get) == 0):
        log.send_message("Перенесення за номером: <code>" + phone + "</code>\nCRM не передала товарів\nПеренесення продовжено без додавання товарів!")
        return result
    for position in get:
        buffer = ProductSearch(str(position["parameter"]))
        if(len(buffer) == 0):
            log.send_message("Перенесення за номером: <code>" + phone + "</code>\nНе знайдено товар за арт. в діловоді!\nАрт: <code>" + position["parameter"] + "</code>\nНазва: <b>" + position["name"] + "</b>\nТовар не буде перенесно !")
        elif(len(buffer) > 1):
            log.send_message("Перенесення за номером: <code>" + phone + "</code>\nВ діловоді більше чим 1 товар за арт.\nАрт: <code>" + position["parameter"] + "</code>\nНазва: <b>" + position["name"] + "</b>\nТовар не буде перенесно !")
        else:
            buffer = buffer[0]
            pos = {}
            pos["good"] = buffer["id"]
            pos["qty"] = position["amount"]
            pos["unit"] = buffer["mainUnit"]
            pos["price"] = position["price"] #Ціна за позицію
            pos["amountCur"] = (position["price"] * position["amount"]) - position["discount"] #Ціна за позицію
            result.append(pos)
    return result