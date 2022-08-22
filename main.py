import telebot
from telebot import types
import json, random
from SimpleQIWI import *
from time import sleep

token2="a2b5b171868fdd13054b96a04b949732"
phone="79056368982"

api = QApi(token=token2, phone=phone)

kb = types.ReplyKeyboardMarkup(resize_keyboard=True)

replan = types.KeyboardButton("Пополнить")
withdraw = types.KeyboardButton("Вывести")
Help = types.KeyboardButton("Помощь")
listOfTms = types.KeyboardButton("Список активных турниров")
stats = types.KeyboardButton("Статистика")
kb.add(replan,withdraw, Help)
kb.add(listOfTms, stats)

token = "5519040811:AAGSaBnxNjTnW4ebOfVDuKlBXT_TJhGxCjQ"

bot = telebot.TeleBot(token, num_threads=5)

@bot.message_handler(commands=['start'])
def start(m):
    with open("data.json", "r", encoding="utf-8") as file:
        isFind = False
        data = json.loads(file.read())
        for name in data["users"].keys():
            if name == str(m.from_user.id):
                isFind = True
                break
        if isFind == False:
            with open("data.json", "w", encoding="utf-8") as f:
                data["users"][str(m.from_user.id)] = {
                    "balance": 0,
                    "bonus": 10,
                    "played": 0,
                    "tms": [
                        
                    ]
                }

                json.dump(data, f, ensure_ascii=False, indent=4)

    bot.send_message(m.from_user.id, "Приветствую! Вы находитесь в меню бота BSTM! Здесь вы можете вывести и пополнить свой счёт. Ссылка на основной канал: https://t.me/BSTMTournaments", reply_markup=kb)

@bot.message_handler(commands=["addtm"], func=lambda m: m.from_user.username == "t6nnng" or m.from_user.id == "m1krOo")
def addtm(m):
    text = m.text.split()
    try:
        f = open("data.json", "r", encoding="utf-8")
        data = json.loads(f.read())

        data["tms"][text[1]] = {
                "name": text[2],
                "date": text[3],
                "cost": int(text[4]),
                "win": int(text[5]),
                "last": 9
            }

        with open("data.json", "w", encoding="utf-8") as file:
            json.dump(data, file, ensure_ascii=False, indent=4)

        bot.send_message(m.from_user.id, "Успешно! Турнир " + text[2] + " добавлен!", reply_markup=kb)
        f.close()
    except:
        bot.send_message(m.from_user.id, "Ошибка! \n\nПравильное использование команды: /addtm -кодовое название турнира- -название турнира для участников- -дата и время- -стоимость участия- -выигрыш-\n\nПример: /addtm tm999 Мега_турнир 2077-08-14-20-00 100 500")
    
@bot.message_handler(commands=["deltm"], func=lambda m: m.from_user.username == "t6nnng" or m.from_user.username == "m1krOo")
def deltm(m):
    text = m.text.split()
    try:
        f = open("data.json", "r", encoding="utf-8")
        data = json.loads(f.read())
        del(data["tms"][text[1]])
        for user in data["users"]:
            mass = data["users"][user]["tms"]
            try:
                a = mass.index(text[1])
                del(mass[a])
                data["users"][user]["tms"] = mass
            except:
                pass
        with open("data.json", "w", encoding="utf-8") as file:
            json.dump(data, file, ensure_ascii=False, indent=4)
        bot.send_message(m.from_user.id, "Успешно! Турнир " + text[1] + " удалён!", reply_markup=kb)
        f.close()
    except:
        bot.send_message(m.from_user.id, "Ошибка! \n\nПравильное использование команды: /deltm -кодовое название турнира-\n\nПример: /deltm tm999")

@bot.message_handler(commands=["addbal"], func=lambda m: m.from_user.username == "t6nnng" or m.from_user.username == "m1krOo")
def addbal(m):
    text = m.text.split()
    try:
        f = open("data.json", "r", encoding="utf-8")
        data = json.loads(f.read())
        data["users"][text[1]]["balance"] += int(text[2])
        with open("data.json", "w", encoding="utf-8") as file:
            json.dump(data, file, ensure_ascii=False, indent=4)
        bot.send_message(m.from_user.id, "Успешно! Пользователю " + text[1] + " добавлены деньги!", reply_markup=kb)
        f.close()
    except:
        bot.send_message(m.from_user.id, "Ошибка! \n\nПравильное использование команды: /addbal -id пользователя- -кол-во денег-\n\nПример: /addbal 1347428034 100")

@bot.message_handler(commands=["bal"], func=lambda m: m.from_user.username == "t6nnng" or m.from_user.username == "m1krOo")
def bal(m):
    bot.send_message(m.from_user.id, str(api.balance[0]))

@bot.message_handler(content_types=['text'])
def message(m):
    if m.text.lower() == "помощь":
        bot.send_message(m.from_user.id, """Привет! Сейчас расскажу как пользоваться этим ботом.

Для того, чтобы вызвать это сообщение, нажми на кнопку "Помощь".

Для того, чтобы связаться с администрацией, напишите @m1krOo или @t6nnng.

Для того, чтобы пополнить свой баланс, нажми на кнопку "Пополнить" и введи сумму для пополнения.

Для того, чтобы вывести деньги со своего баланса, нажми на кнопку "Вывести" и введи необходимую тебе сумму.

Для того, чтобы узнать свою статистику, нажми на кнопку "Статистика".

Для того, чтобы записаться на турнир, нажми на кнопку "Список активных турниров" и выбери желаемый турнир.""", reply_markup=kb)
    elif m.text.lower() == "список активных турниров":
        message = "Список активных турниров:\n\n "
        with open("data.json", "r", encoding="utf-8") as file:
            data = json.loads(file.read())
            choose_tm = types.InlineKeyboardMarkup()
            for tm in data["tms"]:
                choose_tm.add(types.InlineKeyboardButton("Записаться на " + ''.join(data["tms"][tm]["name"].replace("_", " ")), callback_data=str(m.from_user.id) + "_go_on_" + tm + "_" + str(m.message_id)))
                message += "♦ " + ''.join(data["tms"][tm]["name"].replace("_", " ")) + ", дата и время проведения " + ''.join(data["tms"][tm]["date"].replace("_", " ")) + ", стоимость входа " + str(data["tms"][tm]["cost"]) + " рублей, выигрыш " + str(data["tms"][tm]["win"]) + " рублей, осталось " + str(data["tms"][tm]["last"]) + " мест.\n\n "
        bot.send_message(m.from_user.id, message, reply_markup=choose_tm)
    elif m.text.lower() == "статистика":
        with open("data.json", "r", encoding="utf-8") as file:
            data = json.loads(file.read())
            outkb = types.InlineKeyboardMarkup()
            message = f"Привет, {m.from_user.first_name}! Вот статистика твоего аккаунта:\n• Баланс: {str(data['users'][str(m.from_user.id)]['balance'])} рублей \n• Бонусный баланс: {str(data['users'][str(m.from_user.id)]['bonus'])} рублей \n• Сыграно {str(data['users'][str(m.from_user.id)]['played'])} турниров \n• Турниры на которые вы записывались: \n\n"
            for tm in data['users'][str(m.from_user.id)]['tms']:
                outkb.add(types.InlineKeyboardButton("Отписаться от " + ''.join(data['tms'][tm]['name'].replace('_', ' ')), callback_data=str(m.from_user.id) + "_out_of_" + tm + "_" + str(m.message_id)))
                message += f"♦ {''.join(data['tms'][tm]['name'].replace('_', ' '))}, дата проведения: {''.join(data['tms'][tm]['date'].replace('_', ' '))}\n\n"
            bot.send_message(m.from_user.id, message, reply_markup=outkb)
    elif m.text.lower() == "вывести":
        msg = bot.send_message(m.from_user.id, "Хорошо, отправь сообщение с суммой и номером телефона для вывода(только целое число, которое больше или равно 1). Вывод идет ТОЛЬКО на QIWI. Пример: 100 79998887766")
        bot.register_next_step_handler(msg, withdrawBal)
    elif m.text.lower() == "пополнить":
        msg = bot.send_message(m.from_user.id, "Напиши сколько хочешь закинуть на баланс(только целое число, которое больше или равно 1). Пример: 100")
        bot.register_next_step_handler(msg, replanish)
    else:
        bot.send_message(m.from_user.id, "Извини, не понял тебя! Попробуй написать снова!", reply_markup=kb)

def withdrawBal(m):
    text = m.text.split()
    with open("data.json", 'r', encoding="utf-8") as file: 
        data = json.loads(file.read())
        try:
            if int(text[0]) <= data["users"][str(m.from_user.id)]["balance"] and len(text[1]) == 11 and int(text[0]) >= 1:
                try:
                    api.pay(account=text[1], amount=text[0], comment="Вывод с бота BSTM на номер: "+text[1] )
                    data["users"][str(m.from_user.id)]["balance"] -= int(text[0])
                    with open("data.json", 'w', encoding='utf-8') as f:
                        json.dump(data, f, ensure_ascii=False, indent=4)
                    bot.send_message(m.from_user.id, text[0] + " рублей успешно выведены на QIWI +"+text[1])
                except:
                    bot.send_message(m.from_user.id, "У бота нет денег( Подожди денёк.")
            else:
                bot.send_message(m.from_user.id, "Либо у вас нет денег, либо вы написали некорректный номер телефона или сумму вывода!")    
        except:
            bot.send_message(m.from_user.id, "Только целые числа!")

def replanish(m):
    try: 
        price = int(m.text)
        if price >= 1:
            сom = api.bill(price, comment=str(m.from_user.id) + str(random.randint(100000, 999999)))
            api.start()
            check_kb = types.InlineKeyboardMarkup()
            bt = types.InlineKeyboardButton("Проверить платёж", callback_data="check_"+ сom +"_"+str(price)+'_'+str(m.from_user.id)+'_'+str(m.message_id))
            check_kb.add(bt)
            bot.send_message(m.from_user.id, f"Переведите на QIWI {str(price)} рублей с комментарием {сom} на номер +79056368982.", reply_markup=check_kb)
        else:
            bot.send_message(m.from_user.id, "Ну просил же... Пополнить баланс можно ТОЛЬКО на целое число, которое больше или равно 1.")
    except:
        bot.send_message(m.from_user.id, "Ну просил же... Пополнить баланс можно ТОЛЬКО на целое число.")
    

@bot.callback_query_handler(func=lambda call: True)
def callback_inline(call):
    text = call.data.split("_")
    if "go" in text:
        with open("data.json", "r", encoding="utf-8") as file:
            data = json.loads(file.read())
            tms = data["users"][text[0]]["tms"]
            if data["users"][text[0]]["bonus"] >= data["tms"][text[3]]["cost"] and text[3] not in tms and data["tms"][text[3]]["last"] > 0:
                data["users"][text[0]]["tms"].append(text[3])
                data["users"][text[0]]["bonus"] -= data["tms"][text[3]]["cost"]
                data["tms"][text[3]]["last"] -= 1
                bot.answer_callback_query(call.id, "Вы успешно записались! За час до турнира вам напишут модераторы.", cache_time=3)
                bot.delete_message(text[0], int(text[4]))
                bot.delete_message(text[0], int(text[4]) + 1)
                with open("data.json", "w", encoding="utf-8") as f:
                    json.dump(data, f, ensure_ascii=False, indent=4)
            elif data["users"][text[0]]["balance"] >= data["tms"][text[3]]["cost"] and text[3] not in tms and data["tms"][text[3]]["last"] > 0:
                data["users"][text[0]]["tms"].append(text[3])
                data["users"][text[0]]["balance"] -= data["tms"][text[3]]["cost"]
                data["tms"][text[3]]["last"] -= 1
                bot.answer_callback_query(call.id, "Вы успешно записались! За час до турнира вам напишут модераторы.", cache_time=3)
                bot.delete_message(text[0], int(text[4]))
                bot.delete_message(text[0], int(text[4]) + 1)
                with open("data.json", "w", encoding="utf-8") as f:
                    json.dump(data, f, ensure_ascii=False, indent=4)
            elif text[3] in tms:
                bot.answer_callback_query(call.id, "Вы уже записаны на этот турнир!", cache_time=3)
            elif data["tms"][text[3]]["last"] == 0:
                bot.answer_callback_query(call.id, "Свободных мест в турнире не осталось!", cache_time=3)
            else:
                bot.answer_callback_query(call.id, "К сожалению, вам не хватает средств, чтобы записаться на турнир. Пополните баланс.")
    elif "out" in text:
        with open("data.json", "r", encoding="utf-8") as file:
            data = json.loads(file.read())
            tms = data["users"][text[0]]["tms"]
            a = tms.index(text[3])
            del(tms[a])
            data["users"][text[0]]["tms"] = tms
            data["users"][text[0]]["bonus"] += data["tms"][text[3]]["cost"]
            data["tms"][text[3]]["last"] += 1
            bot.answer_callback_query(call.id, "Вы успешно отписались от турнира. Деньги возвращены.", cache_time=3)
            bot.delete_message(text[0], int(text[4]))
            bot.delete_message(text[0], int(text[4]) + 1)
            with open("data.json", "w", encoding="utf-8") as f:
                json.dump(data, f, ensure_ascii=False, indent=4)
    elif "check" in text:
        if api.check(text[1]):
            api.stop()
            bot.answer_callback_query(call.id, "Платёж получен! Деньги начислены.", cache_time=3)
            with open("data.json", 'r', encoding='utf-8') as file:
                data = json.loads(file.read())
                data["users"][text[3]]["balance"] += int(text[2])
                bot.delete_message(text[3], int(text[4]))
                bot.delete_message(text[3], int(text[4])+1)
                bot.delete_message(text[3], int(text[4])-1)
                bot.delete_message(text[3], int(text[4])-2)
                with open("data.json", 'w', encoding='utf-8') as f:
                    json.dump(data, f, ensure_ascii=False, indent=4)
        else:
            bot.answer_callback_query(call.id, "Платёж не найден.", cache_time=3)
              
bot.infinity_polling()