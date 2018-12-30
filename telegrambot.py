import telebot
from telebot import types
import const
from geopy.distance import geodesic
bot = telebot.TeleBot(const.API_TOKEN)

markup_menu = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=1)
btn_address = types.KeyboardButton('Aдрес магазина', request_location=True)
btn_paymant = types.KeyboardButton('Способы оплаты')
btn_about_us = types.KeyboardButton('О нас')
markup_menu.add(btn_address, btn_paymant, btn_about_us)

markup_inline_paymant = types.InlineKeyboardMarkup(row_width=1)
btn_in_cash = types.InlineKeyboardButton("Готівка", callback_data='cash')
btn_in_card = types.InlineKeyboardButton("Картка", callback_data='card')
btn_in_invoice = types.InlineKeyboardButton("Банківськаий перерахунок", callback_data='invoice')
markup_inline_paymant.add(btn_in_card, btn_in_cash, btn_in_invoice)

@bot.message_handler(commands=['start','help'])
def start(message):
    bot.send_message(message.chat.id, "Привіт, я Telegram бот створений Демянчуком Денисом", reply_markup=markup_menu)

@bot.message_handler(func=lambda message: True)
def echo_all(message):
    if message.text == 'Aдрес магазина':
        bot.send_message(message.chat.id, 'К сожелению, у нас еще нету адреса', reply_markup=markup_menu)
    elif message.text == 'Способы оплаты':
        bot.send_message(message.chat.id, "У наших магазиах доступні наступні способи оплати", reply_markup=markup_inline_paymant)
    elif message.text == 'О нас':
        bot.send_message(message.chat.id, 'Бот создан @Admiral_Den', reply_markup=markup_menu)
    else:
        bot.send_message(message.chat.id, 'Я не понимаю тебя ', reply_markup=markup_menu)

@bot.message_handler(func=lambda message: True, content_types=['location'])
def magazine_location(message):
    lon = message.location.longitude
    lat = message.location.latitude
    print('Ширина {} Долгота {}' .format(lon, lat))

    distance = []
    for m in const.MAGAZINS:
        result = geodesic((m['latm'],m['lonm']), (lat, lon)).kilometers
        distance.append(result)
    index = distance.index(min(distance))
    bot.send_message(message.chat.id, 'Ближаччший к вам магазин')
    bot.send_venue(message.chat.id, const.MAGAZINS[index]['latm'], const.MAGAZINS[index]['lonm'], const.MAGAZINS[index]['title'], const.MAGAZINS[index]['address'])

@bot.callback_query_handler(func=lambda call: True)
def call_back_payant(call):
    if call.data == 'cash':
        bot.send_message(call.message.chat.id, text='Налична оплата проосходит кассе магазина', reply_markup=markup_inline_paymant)

bot.polling()