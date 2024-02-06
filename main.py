#Code 25.11.24 (edit), By LedsHack@
import json
from flask import Flask, request
from sendPacket import send
from configurateOrder import Order as generateOrder
from tradeChanel import search as TradeChanelSearch
from worker import search as WorkerSearch
from user import search as UserSearch
from user import create as UserCreate
from setID import set as OrderAddCRMid
from setID import search as OrederCrmSearch
import logerTG as log
from extern import head

app = Flask(__name__)

@app.route('/', methods=['POST'])
def index():
    data = json.loads(request.get_data().decode('utf-8'))
    #print(json.dumps(data_dict, indent=4, ensure_ascii=False))
    if(data["info"]["webhookEvent"] == "status_change"):
        #print(json.dumps(data, indent=4, ensure_ascii=False))
        client_info = {}

        client_info["phone"] = data["data"]["contacts"][0]["phone"][0]

        if(data["data"]["contacts"][0]["fName"] == None):
            data["data"]["contacts"][0]["fName"] = ""
        else:
            data["data"]["contacts"][0]["fName"] = " " + data["data"]["contacts"][0]["fName"]
        if(data["data"]["contacts"][0]["lName"] == None):
            data["data"]["contacts"][0]["lName"] = ""
        else:
            data["data"]["contacts"][0]["lName"] = " " + data["data"]["contacts"][0]["lName"]
        if(data["data"]["contacts"][0]["mName"] == None):
            data["data"]["contacts"][0]["mName"] = ""
        else:
            data["data"]["contacts"][0]["mName"] = " " + data["data"]["contacts"][0]["mName"]

        client_info["pib"] = ""
        client_info["pib"] += data["data"]["contacts"][0]["fName"]
        client_info["pib"] += data["data"]["contacts"][0]["lName"]
        client_info["pib"] += data["data"]["contacts"][0]["mName"]

        client_info["data_create"] = data["data"]["orderTime"] #Дата + час оформлення замовлення
        client_info["manager"] = data["meta"]["fields"]["userId"]["options"][0]["text"] #Менеджер
        client_info["order"] = data["data"]["products"] #Інформація про замовлені товари
        client_info["order_id"] = str(data["data"]["id"])
        client_info["tradeChanel"] = data["meta"]["fields"]["resurs"]["options"][0]["text"]
        client_info["mark"] = "Тут буде примітка!"
        print(json.dumps(client_info, indent=4, ensure_ascii=False))
        #process(client_info)
    return "Request received", 200

def CreateSeleOrder(meta, product, saveType=0):
    packet = {
        "action": "saveObject",
        "params": {
            "saveType": saveType,
            "header": meta,
            "tableParts": {
                "tpGoods": product
            }
        },
    }
    res = send(packet)
    print("Ok> "  + str(res))
    return(res)

def process(client_info):
    meta = {}
    #Пошук заявки за айди з црм в порівнянні доп поля dilovod
    buffer = OrederCrmSearch(client_info["order_id"])
    if(len(buffer) == 1):
        buffer = buffer[0]
        print("Заявка є: " + str(buffer))
        meta["id"] = buffer["id"]
        meta["state"] = head["state"]
        buffer = CreateSeleOrder(meta, generateOrder(client_info["order"], client_info["phone"]), 2) #Збереження зі скасуванням проведення
        if ("result" not in buffer):
            log.send_message("Помилка при перенесенні!\nНомер: <code>" + client_info["phone"] + "</code>\nПеренесення СКАСОВАНО!" + "\nВідповідь сервера: " + str(buffer))
            return
        if (buffer["result"] != "ok"):
            log.send_message("Помилка при перенесенні!\nНомер: <code>" + client_info["phone"] + "</code>\nПеренесення СКАСОВАНО!" + "\nВідповідь сервера: " + str(buffer))
            return

    else:
        meta["date"] = client_info["data_create"]
        #Перенесення клієнта
        buffer = UserSearch(client_info["phone"].replace("+", "").replace("38", ""))

        if(len(buffer) == 0):
            buffer = UserCreate(client_info["pib"], client_info["phone"])
        elif(len(buffer) > 1):
            log.send("Помилка перенесення 2 клієнта на одному номері телефону: <code>" + client_info["phone"] + "</code>\nПеренесення СКАСОВАНО !")
            return
        else:
            buffer = buffer[0]
        meta["person"] = buffer["id"]

        #Перенесення менеджера
        buffer = WorkerSearch(client_info["manager"])
        if(len(buffer) == 0):
            log.send_message("Перенесення за номером: <code>" + client_info["phone"] + "</code>\nНе знайдено менеджера: <b>" + client_info["manager"] + "</b> \nПеренесення продовжено без фіксації за менджером!")
            buffer = {"id": ""}
        elif(len(buffer) > 1):
            log.send_message("Перенесення за номером: <code>" + client_info["phone"] + "</code>\nЗнайдено більше чим 1 менеджер: <b>" + client_info["manager"] + "</b> \nПеренесення продовжено без фіксації за менджером!")
            buffer = {"id": ""}
        else:
            buffer = buffer[0]
        meta["manager"] = buffer["id"]

        #Канал продажів
        buffer = TradeChanelSearch(client_info["tradeChanel"])
        if(len(buffer) == 0):
            log.send_message("Перенесення за номером: <code>" + client_info["phone"] + "</code>\nНе знайдено каналу продажів: <b>" + client_info["tradeChanel"] + "</b> \nПеренесення продовжено без каналу продажів!")
            buffer = {"id": ""}
        elif(len(buffer) > 1):
            log.send_message("Перенесення за номером: <code>" + client_info["phone"] + "</code>\nЗнайдено більше чим 1 канал продажу: <b>" + client_info["tradeChanel"] + "</b> \nПеренесення продовжено без каналу продажів!")
            buffer = {"id": ""}
        else:
            buffer = buffer[0]
        meta["tradeChanel"] = buffer["id"]

        #Додавання внутріщньої примітки
        meta["remark"] = client_info["mark"]

        #Створення замовлення
        buffer = CreateSeleOrder({**head, **meta}, generateOrder(client_info["order"], client_info["phone"]))

        #Присвоєння айди с CRM
        if("result" not in buffer):
            log.send_message("Помилка при перенесенні!\nНомер: <code>" + client_info["phone"] + "</code>\nПеренесення СКАСОВАНО!" + "\nВідповідь сервера: " + str(buffer))
            return
        if(buffer["result"] != "ok"):
            log.send_message("Помилка при перенесенні!\nНомер: <code>" + client_info["phone"] + "</code>\nПеренесення СКАСОВАНО!" + "\nВідповідь сервера: " + str(buffer))
            return
        OrderAddCRMid(buffer["id"], client_info["order_id"])


app.run(host='0.0.0.0', port=19199)