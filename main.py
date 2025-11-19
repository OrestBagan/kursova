import telebot
from token_bot import token
import json
import os

bot = telebot.TeleBot(token())

commands = [
    telebot.types.BotCommand("start", "Запустити бота"),
]

bot.set_my_commands(commands)

@bot.message_handler(commands=['start'])
def start(message):
    bot.send_message(message.chat.id, "привіт, я бот кав'ярні")
    keyboard = telebot.types.ReplyKeyboardMarkup(resize_keyboard=True)
    keyboard.add("Меню", "Корзина", "Контакти", "Адміністратор")
    bot.send_message(message.chat.id, "Обери:", reply_markup=keyboard)

@bot.message_handler(func=lambda message: message.text == "Меню")
def menu_main(message):
    markup_main = telebot.types.InlineKeyboardMarkup()
    in_keybord_main = {"Кава": "coffe", "Напої": "drinks", "Дисерти": "desserts"}

    for key in in_keybord_main.keys():
        button = telebot.types.InlineKeyboardButton(text=key, callback_data=in_keybord_main[key])
        markup_main.add(button)

    bot.send_message(message.chat.id, "Оберіть категорію, що саме Ви хотіли б замовити", reply_markup=markup_main)

@bot.callback_query_handler(func=lambda call: call.data in ["coffe", "drinks", "desserts", "Меню"])
def menu(call):
    bot.answer_callback_query(call.id)
    if call.data == "coffe":
        markup_coffe = telebot.types.InlineKeyboardMarkup()
        in_keybord_coffe = {"Еспресо": "espreso", "Американо": "americano", "Капучино": "capuchino", "Лате": "late", "Назад": "Меню"}
        
        for key in in_keybord_coffe.keys():
            button = telebot.types.InlineKeyboardButton(text=key, callback_data=in_keybord_coffe[key])
            markup_coffe.add(button)

        bot.send_message(call.message.chat.id, """Ось доступні варіанти кави із цінами:\n
• Еспресо — 35₴  
• Американо — 40₴  
• Капучино — 55₴  
• Лате — 60₴  
Добавити в корзину:""", reply_markup=markup_coffe)
        
    elif call.data == "drinks":
        markup_drinks = telebot.types.InlineKeyboardMarkup()
        in_keybord_drinks = {"Чай зелений": "tea_green", "Чай чорний": "tea_black", "Матча": "matcha", "Какао": "kackao", "Назад": "Меню"}

        for key in in_keybord_drinks.keys():
            button = telebot.types.InlineKeyboardButton(text=key, callback_data=in_keybord_drinks[key])
            markup_drinks.add(button)

        bot.send_message(call.message.chat.id, """Ось доступні варіанти наопоїв із цінами:\n
• Чай чорний/зелений — 35₴  
• Матча — 70₴  
• Какао — 50₴
Добавити в корзину:""", reply_markup=markup_drinks)
        
    elif call.data == "desserts":
        markup_desserts = telebot.types.InlineKeyboardMarkup()
        in_keybord_desserts = {"Чізкей": "cheesecake", "Тірамісу": "tiramisu ", "Макарони": "macaron", "Назад": "Меню"}

        for key in in_keybord_desserts.keys():
            button = telebot.types.InlineKeyboardButton(text=key, callback_data=in_keybord_desserts[key])
            markup_desserts.add(button)
            
        bot.send_message(call.message.chat.id, """Ось доступні варіанти дисертів із цінами:\n
• Чізкейк — 80₴  
• Тірамісу — 85₴  
• Макарони (2шт) — 45₴
Добавити в корзину:""", reply_markup=markup_desserts)
    
    elif call.data == "Меню":
        bot.send_message(call.message.chat.id, "Меню")

@bot.callback_query_handler(func=lambda call: call.data in ["espreso", "americano", "capuchino", "late", "tea_green", "tea_black", "matcha", "kackao", "cheesecake", "tiramisu", "macaron"])
def save_cart(call):
    filename = "bascet.json"

    prices = {
        "espreso": ("Еспресо", 35), "americano": ("Американо", 40), 
        "capuchino": ("Капучино", 55), "late": ("Лате", 60),
        "tea_green": ("Чай зелений", 35), "tea_black": ("Чай чорний", 35), 
        "matcha": ("Матча", 70), "kackao": ("Какао", 50),
        "cheesecake": ("Чізкейк", 80), "tiramisu": ("Тірамісу", 85), 
        "macaron": ("Макарони", 45)
    }

    data = {}

    if os.path.exists(filename) and os.path.getsize(filename) > 0:
        with open(filename, "r", encoding='utf-8') as f:
            try:
                data = json.load(f)
            except json.JSONDecodeError:
                print(f"Попередження: Файл {filename} містить невалідний JSON. Створюємо новий об'єкт.")
                data = {}

    user_cart = data.get(str(call.from_user.id), [])
    
    found_item = None
    corent_quontity = 0
    for i in user_cart:
        if i.get("id") == call.data:
            found_item = i
            corent_quontity = i.get("quantity")
            break
    
    if found_item:
        found_item["quantity"] = found_item.get("quantity", 0) + 1
    else:
        new_item = {
            "id": call.data,
            "name": prices[call.data][0],
            "price": prices[call.data][1],
            "quantity": 1
        }
        user_cart.append(new_item)

    data[str(call.from_user.id)] = user_cart

    with open(filename, "w", encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=4)

    bot.answer_callback_query(
        call.id,
        text=f"✅ {prices[call.data][0]} додано! Кількість: {corent_quontity + 1}", 
        show_alert=False
    )

bot.polling()