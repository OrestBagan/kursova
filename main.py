import telebot

bot = telebot.TeleBot('8523107390:AAFApLt1wIQ2_4kFyfSprjWdgspPzIY-gZQ')

commands = [
    telebot.types.BotCommand("start", "Запустити бота"),
    telebot.types.BotCommand("help", "Отримати допомогу"),
    telebot.types.BotCommand("menu", "Відкрити меню"),
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

@bot.callback_query_handler(func=lambda call: True)
def menu(call):
    if call.data == "coffe":
        bot.send_message(call.message.chat.id, """Ось доступні варіанти кави із цінами:\n
• Еспресо — 35₴  
• Американо — 40₴  
• Капучино — 55₴  
• Лате — 60₴  
• Флет Вайт — 65₴  """)
        
    elif call.data == "drinks":
        bot.send_message(call.message.chat.id, """Ось доступні варіанти наопоїв із цінами:\n
• Чай чорний/зелений — 35₴  
• Матча — 70₴  
• Какао — 50₴  """)
        
    elif call.data == "desserts":
        bot.send_message(call.message.chat.id, """Ось доступні варіанти дисертів із цінами:\n
• Чізкейк — 80₴  
• Тірамісу — 85₴  
• Макарони (2шт) — 45₴ """)

bot.polling()