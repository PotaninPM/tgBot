import openai
import asyncio
import markups as nav
import logging
import config
from aiogram import Bot, types
from aiogram.dispatcher import Dispatcher
from aiogram.utils import executor
from db import Database
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.types.message import ContentType

import time
import datetime

from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, InlineKeyboardMarkup, InlineKeyboardButton
messages  = [
    {"role": "system", "content": "you are a personal learning assistant who helps you do whatever you are asked to do."},
]

def update(messages, role, content):
    messages.append({"role": role, "content": content})
    return messages
PAYMENTS_TOKEN = "1744374395:TEST:46a69684b6ea9ed7d292"
#API ключ OpenAI
openai.api_key = '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'
# Токен телеграмм бота от BotFather
bot = Bot(token='6262271892:AAHbrysP9XhiZXUt4QweC2b0KsL7bkN7D0U')

dp = Dispatcher(bot)
#база даннх Sqlite
db = Database('database.db')

#перевод дней в секунды
def days_to_seconds(days):
    return days * 24 * 3600
#расчет оставшегося времени подписки
def time_sub_day(get_time):
    time_now = int(time.time())
    middle_time = int(get_time) - time_now
    time_end = middle_time // (3600 * 24)
    if(middle_time <= 0):
        return False
    else:
        dt = str(datetime.timedelta(seconds=middle_time))
        dt = dt.replace("days", "дней")
        return dt
#при старте
@dp.message_handler(commands=['start'])
async def start(message: types.Message):
    if(not db.user_exists(message.from_user.id)):
        db.add_user(message.from_user.id)
        em1 = 'potanin_08@list.ru'
        em = 'example@gmail.com'
        await bot.send_message(message.from_user.id, "Здраствуйте!👋 Прямо сейчас Вы находитесь в Личном Учебном Ассистенте. Этот бот может помочь вам с тем чем вы хотите. В его функционал входит : написание некоторых творческих работ, поиск полезной информации, решение некоторых задач и так далее. После регистрации вы можете сделать 2 пробных запроса, чтобы удостоверится в полезносте бота. Для дальнейшего использования бота необходимо приобрести подписку(подробности по всем кнопкам в разделе ЧТО ЭТО❓). Почта техподдержки: " + em1 + ". Удачного пользования!🍀")
        await bot.send_message(message.from_user.id, "Пожалуйста создайте Ваш логин, написав его в сюда(это нужно для дальнейшей работы)👑")
    elif(db.get_nickname(message.from_user.id) == "setnickname"):
        await bot.send_message(message.from_user.id, "Создайте Ваш логин, написав его сюда!!!")
    elif(db.get_email(message.from_user.id) == "setemail"):
        await bot.send_message(message.from_user.id, "Укажите вашу электронную почту📬 для полной регистрации (это обязательно❗️❗️❗️")
    else: 
        if(db.get_sub(message.from_user.id) == "неактивна" and db.get_queries_pr(message.from_user.id) == '0'):
            talk = "Но так как ваша подписка неактивна, вы не можете общаться с ботом❌. Чтобы это исправить нажмите на кнопку 💵КУПИТЬ ПОДПИСКУ"
        elif(db.get_queries_pr(message.from_user.id) != '0'):
            talk = "У Вас есть еще " + db.get_queries_pr(message.from_user.id) + " бесплатных запроса и Вы можете писать боту вопросы✅.\n Просто пишите вопросы в чат и он будет отвечать на них.\n(на некоторые вопросы он может отвечать странно)"
        else:
            if(db.get_queries(message.from_user.id) != '0'):
                talk = "Ваша подписка активна и у Вас достаточное количество запросов для пользования ботом✅.\nПросто пишите вопросы в чат и он будет отвечать на них.\n(на некоторые вопросы он может отвечать странно)"
            elif(db.get_queries(message.from_user.id) == '0'):
                talk = "Ваша подписка активна,но у Вас недостаточное количество запросов для пользования ботом❌.\nЧтобы это справить нажмите на кнопку ➕ДОКУПИТЬ ЗАПРОСЫ"
        if(db.get_sub(message.from_user.id) == "Владелец"):
            await bot.send_message(message.from_user.id, "Добро пожаловать Владелец!👋\n", reply_markup= nav.mainMenu1)
        else:
            await bot.send_message(message.from_user.id, "Вы уже зарегистрированы!👋\n" + talk, reply_markup= nav.mainMenu)
#оплата вся
#оплата доп запросов
@dp.callback_query_handler(text='buydop')
async def buydop(call: types.CallbackQuery):
     await bot.delete_message(call.from_user.id, call.message.message_id)
     await bot.send_invoice(chat_id=call.from_user.id, title="Покупка дополнительных запросов", description="Запросы 60 штук", payload="queries60", provider_token=PAYMENTS_TOKEN,currency="RUB", start_parameter="bot", prices=[{"label": "Рубли", "amount":7500}])

@dp.callback_query_handler(text='buydop1')
async def buydop(call: types.CallbackQuery):
     await bot.delete_message(call.from_user.id, call.message.message_id)
     await bot.send_invoice(chat_id=call.from_user.id, title="Покупка дополнительных запросов", description="Запросы 150 штук", payload="queries150", provider_token=PAYMENTS_TOKEN,currency="RUB", start_parameter="bot", prices=[{"label": "Рубли", "amount":16500}])

@dp.callback_query_handler(text='buydop2')
async def buydop(call: types.CallbackQuery):
     await bot.delete_message(call.from_user.id, call.message.message_id)
     await bot.send_invoice(chat_id=call.from_user.id, title="Покупка дополнительных запросов", description="Запросы 240 штук", payload="queries240", provider_token=PAYMENTS_TOKEN,currency="RUB", start_parameter="bot", prices=[{"label": "Рубли", "amount":26500}])

@dp.callback_query_handler(text='buydop3')
async def buydop(call: types.CallbackQuery):
     await bot.delete_message(call.from_user.id, call.message.message_id)
     await bot.send_invoice(chat_id=call.from_user.id, title="Покупка дополнительных запросов", description="Запросы 330 штук", payload="queries330", provider_token=PAYMENTS_TOKEN,currency="RUB", start_parameter="bot", prices=[{"label": "Рубли", "amount":35500}])
#оплата подписок
@dp.callback_query_handler(text='buysub')
async def buysub(call: types.CallbackQuery):
     if(db.get_promo_user(call.from_user.id) != 'none'):
        disc1 = int(db.get_promo_disc(db.get_promo_user(call.from_user.id)))
        new = 75 - (75 * (disc1 / 100))
        new_price = int(round(new, 1) * 100)
     else:
         new_price = 7500
     await bot.delete_message(call.from_user.id, call.message.message_id)
     await bot.send_invoice(chat_id=call.from_user.id, title="Покупка подписки", description='Подписка "Заглянувший"', payload="subNew", provider_token=PAYMENTS_TOKEN,currency="RUB", start_parameter="bot", prices=[{"label": "Рубли", "amount": new_price}])

@dp.callback_query_handler(text='buysub1')
async def buysub(call: types.CallbackQuery):
     if(db.get_promo_user(call.from_user.id) != 'none'):
        disc1 = int(db.get_promo_disc(db.get_promo_user(call.from_user.id)))
        inter = 165 - (165 * (disc1 / 100))
        inter_price = int(round(inter, 1) * 100)
     else:
         inter_price = 16500
     await bot.delete_message(call.from_user.id, call.message.message_id)
     await bot.send_invoice(chat_id=call.from_user.id, title="Покупка подписки", description='Подписка "Интересующийся"', payload="subInter", provider_token=PAYMENTS_TOKEN,currency="RUB", start_parameter="bot", prices=[{"label": "Рубли", "amount":inter_price}])


@dp.callback_query_handler(text='buysub2')
async def buysub(call: types.CallbackQuery):
     if(db.get_promo_user(call.from_user.id) != 'none'):
        disc1 = int(db.get_promo_disc(db.get_promo_user(call.from_user.id)))
        pro = 265 - (265 * (disc1 / 100))
        pro_price = int(round(pro, 1) * 100)
     else:
         pro_price = 26500
     await bot.delete_message(call.from_user.id, call.message.message_id)
     await bot.send_invoice(chat_id=call.from_user.id, title="Покупка подписки", description='Подписка "Продвинутый"', payload="subPro", provider_token=PAYMENTS_TOKEN,currency="RUB", start_parameter="bot", prices=[{"label": "Рубли", "amount":pro_price}])

@dp.callback_query_handler(text='buysub3')
async def buysub(call: types.CallbackQuery):
     if(db.get_promo_user(call.from_user.id) != 'none'):
        disc1 = int(db.get_promo_disc(db.get_promo_user(call.from_user.id)))
        exp = 355 - (355 * (disc1 / 100))
        exp_price = int(round(exp, 1) * 100)
     else:
         exp_price = 35500
     await bot.delete_message(call.from_user.id, call.message.message_id)
     await bot.send_invoice(chat_id=call.from_user.id, title="Покупка подписки", description='Подписка "Эксперт"', payload="subExp", provider_token=PAYMENTS_TOKEN,currency="RUB", start_parameter="bot", prices=[{"label": "Рубли", "amount":exp_price}])
#проверка на наличие
@dp.pre_checkout_query_handler()
async def process_pre_checkout_query(pre_checkout_query: types.PreCheckoutQuery):
    await bot.answer_pre_checkout_query(pre_checkout_query.id, ok=True)
#проверка куда зачислять
@dp.message_handler(content_types=ContentType.SUCCESSFUL_PAYMENT)
async def process_pay(message: types.Message):

    if message.successful_payment.invoice_payload == "queries60":
        db.give_queries60(message.from_user.id)
        await bot.send_message(message.from_user.id, "Оплата прошла успешно✅.\n Запросы 60 штук зачислены на Ваш счет✅." + "\n У вас сейчас " + db.get_queries(message.from_user.id) + " запросов✅.")
    elif message.successful_payment.invoice_payload == "queries150":
        db.give_queries150(message.from_user.id)
        await bot.send_message(message.from_user.id, "Оплата прошла успешно✅.\n Запросы 150 штук зачислены на Ваш счет✅." + "\n У вас сейчас " + db.get_queries(message.from_user.id) + " запросов✅.")
    elif message.successful_payment.invoice_payload == "queries240":
        db.give_queries240(message.from_user.id)
        await bot.send_message(message.from_user.id, "Оплата прошла успешно✅.\n Запросы 240 штук зачислены на Ваш счет✅." + "\n У вас сейчас " + db.get_queries(message.from_user.id) + " запросов✅.")
    elif message.successful_payment.invoice_payload == "queries330":
        db.give_queries330(message.from_user.id)
        await bot.send_message(message.from_user.id, "Оплата прошла успешно✅.\n Запросы 330 штук зачислены на Ваш счет✅." + "\n У вас сейчас " + db.get_queries(message.from_user.id) + " запросов✅.")
    
    elif(message.successful_payment.invoice_payload == "subNew"):
        time_sub = int(time.time() + days_to_seconds(30))
        db.set_time_sub(message.from_user.id, time_sub)
        db.give_sub_new(message.from_user.id)
        db.give_queries60(message.from_user.id)
        await bot.send_message(message.from_user.id, 'Оплата прошла успешно✅.\nПодписка "👀Заглянувший👀" была выдана успешно✅.' + "\nВаш статус подписки " + '👀' + db.get_sub(message.from_user.id) + '👀' + '\n' + "Срок подписки истекает через 30 дней\n" + "Удачного использования!🍀\nДля участия в розыгрышах зайдите в эту группу: https://t.me/+C_p_bDWW5AhiMDk6")
        if(db.get_promo_user(message.from_user.id) != "none"):
            await bot.send_message(message.from_user.id, "Так как Вы использовали промокод, Вам было выдано +" + db.get_promo_queries(db.get_promo_user(message.from_user.id)) + " запросов🎉")
            db.give_queries_promo(message.from_user.id, db.get_promo_queries(db.get_promo_user(message.from_user.id)))
        db.delete_promo(message.from_user.id)
    elif(message.successful_payment.invoice_payload == "subInter"):
        time_sub = int(time.time() + days_to_seconds(30))
        db.set_time_sub(message.from_user.id, time_sub)
        db.give_queries150(message.from_user.id)
        db.give_sub_inter(message.from_user.id)
        await bot.send_message(message.from_user.id, 'Оплата прошла успешно✅.\nПодписка "🧐Интересующийся🧐" была выдана успешно✅.' + "\nВаш статус подписки " + '🧐' + db.get_sub(message.from_user.id) + '🧐' + '\n' + "Срок подписки истекает через 30 дней\n" + "Удачного использования!🍀\nДля участия в розыгрышах зайдите в эту группу: https://t.me/+C_p_bDWW5AhiMDk6")
        if(db.get_promo_user(message.from_user.id) != "none"):
            await bot.send_message(message.from_user.id, "Так как Вы использовали промокод, Вам было выдано +" + db.get_promo_queries(db.get_promo_user(message.from_user.id)) + " запросов🎉")
            db.give_queries_promo(message.from_user.id, db.get_promo_queries(db.get_promo_user(message.from_user.id)))
        db.delete_promo(message.from_user.id)
    elif(message.successful_payment.invoice_payload == "subPro"):
        time_sub = int(time.time() + days_to_seconds(30))
        db.set_time_sub(message.from_user.id, time_sub)
        db.give_queries240(message.from_user.id)
        db.give_sub_pro(message.from_user.id)
        await bot.send_message(message.from_user.id, 'Оплата прошла успешно✅.\nПодписка "🧩Продвинутый🧩" была выдана успешно✅.' + "\nВаш статус подписки " + '🧩' + db.get_sub(message.from_user.id) + '🧩' + '\n' + "Срок подписки истекает через 30 дней\n" + "Удачного использования!🍀\nДля участия в розыгрышах зайдите в эту группу: https://t.me/+MSOUBM5t16oxYzRi")
        if(db.get_promo_user(message.from_user.id) != "none"):
            await bot.send_message(message.from_user.id, "Так как Вы использовали промокод, Вам было выдано +" + db.get_promo_queries(db.get_promo_user(message.from_user.id)) + " запросов🎉")
            db.give_queries_promo(message.from_user.id, db.get_promo_queries(db.get_promo_user(message.from_user.id)))
        db.delete_promo(message.from_user.id)
    elif(message.successful_payment.invoice_payload == "subExp"):
        time_sub = int(time.time() + days_to_seconds(30))
        db.set_time_sub(message.from_user.id, time_sub)
        db.give_queries330(message.from_user.id)
        db.give_sub_exp(message.from_user.id)
        await bot.send_message(message.from_user.id, 'Оплата прошла успешно✅.\nПодписка "😎Эксперт😎" была выдана успешно✅.' + "\nВаш статус подписки " + '😎' + db.get_sub(message.from_user.id) + '😎' + '\n' + "Срок подписки истекает через 30 дней\n" + "Удачного использования!🍀\nДля участия в розыгрышах зайдите в эту группу: https://t.me/+MSOUBM5t16oxYzRi")
        if(db.get_promo_user(message.from_user.id) != "none"):
            await bot.send_message(message.from_user.id, "Так как Вы использовали промокод, Вам было выдано +" + db.get_promo_queries(db.get_promo_user(message.from_user.id)) + " запросов🎉")
            db.give_queries_promo(message.from_user.id, db.get_promo_queries(db.get_promo_user(message.from_user.id)))
        db.delete_promo(message.from_user.id)
#выдача подписки
@dp.callback_query_handler(text='sub')
async def sub(call: types.CallbackQuery):
    day_to_sec = 30 * 24 * 3600
    sub_time = int(time.time() + day_to_sec)
    time_now = int(time.time())
    #await bot.delete_message(call.from_user.id, call.message.message_id)
    us = db.get_give_nickname(call.from_user.id)
    await bot.send_message(call.from_user.id, 'Подписка "Заглянувший" успешно выдана пользователю - ' + db.get_give_nickname(call.from_user.id) + '✅')
    db.give_sub_new1(us)
    db.set_time_sub1(us, sub_time)
    db.set_give_nickname(call.from_user.id, "none")

@dp.callback_query_handler(text='sub1')
async def sub(call: types.CallbackQuery):
    day_to_sec = 30 * 24 * 3600
    sub_time = int(time.time() + day_to_sec)
    time_now = int(time.time())
    #await bot.delete_message(call.from_user.id, call.message.message_id)
    us = db.get_give_nickname(call.from_user.id)
    await bot.send_message(call.from_user.id, 'Подписка "Интересующийся" успешно выдана пользователю - ' + db.get_give_nickname(call.from_user.id) + '✅')
    db.give_sub_inter1(us)
    db.set_time_sub1(us, sub_time)
    db.set_give_nickname(call.from_user.id, "none")

@dp.callback_query_handler(text='sub2')
async def sub(call: types.CallbackQuery):
    day_to_sec = 30 * 24 * 3600
    sub_time = int(time.time() + day_to_sec)
    time_now = int(time.time())
    #await bot.delete_message(call.from_user.id, call.message.message_id)
    us = db.get_give_nickname(call.from_user.id)
    await bot.send_message(call.from_user.id, 'Подписка "Продвинутый" успешно выдана пользователю - ' + db.get_give_nickname(call.from_user.id) + '✅')
    db.give_sub_pro1(us)
    db.set_time_sub1(us, sub_time)
    db.set_give_nickname(call.from_user.id, "none")

@dp.callback_query_handler(text='sub3')
async def sub(call: types.CallbackQuery):
    day_to_sec = 30 * 24 * 3600
    sub_time = int(time.time() + day_to_sec)
    time_now = int(time.time())
    #await bot.delete_message(call.from_user.id, call.message.message_id)
    us = db.get_give_nickname(call.from_user.id)
    await bot.send_message(call.from_user.id, 'Подписка "Эксперт" успешно выдана пользователю - ' + db.get_give_nickname(call.from_user.id) + '✅')
    db.give_sub_exp1(us)
    db.set_time_sub1(us, sub_time)
    db.set_give_nickname(call.from_user.id, "none")
#выдача запросов
@dp.callback_query_handler(text='dop_1')
async def sub(call: types.CallbackQuery):
    us = db.get_give_nickname(call.from_user.id)
    await bot.send_message(call.from_user.id, "Запрос 1 штука успешно выданы пользователю - " + db.get_give_nickname(call.from_user.id) + '✅')
    db.give_queries_1(us)
    db.set_give_nickname(call.from_user.id, "none")

@dp.callback_query_handler(text='dop')
async def sub(call: types.CallbackQuery):
    us = db.get_give_nickname(call.from_user.id)
    await bot.send_message(call.from_user.id, "Запросы 60 штук успешно выданы пользователю - " + db.get_give_nickname(call.from_user.id) + '✅')
    db.give_queries60_1(us)
    db.set_give_nickname(call.from_user.id, "none")

@dp.callback_query_handler(text='dop1')
async def sub(call: types.CallbackQuery):
    us = db.get_give_nickname(call.from_user.id)
    await bot.send_message(call.from_user.id, "Запросы 150 штук успешно выданы пользователю - " + db.get_give_nickname(call.from_user.id) + '✅')
    db.give_queries150_1(us)
    db.set_give_nickname(call.from_user.id, "none")

@dp.callback_query_handler(text='dop2')
async def sub(call: types.CallbackQuery):
    us = db.get_give_nickname(call.from_user.id)
    await bot.send_message(call.from_user.id, "Запросы 240 штук успешно выданы пользователю - " + db.get_give_nickname(call.from_user.id) + '✅')
    db.give_queries240_1(us)
    db.set_give_nickname(call.from_user.id, "none")

@dp.callback_query_handler(text='dop3')
async def sub(call: types.CallbackQuery):
    us = db.get_give_nickname(call.from_user.id)
    await bot.send_message(call.from_user.id, "Запросы 330 штук успешно выданы пользователю - " + db.get_give_nickname(call.from_user.id) + '✅')
    db.give_queries330_1(us)
    db.set_give_nickname(call.from_user.id, "none")
#удовлетворение ответом
@dp.callback_query_handler(text='markY')
async def buydop(call: types.CallbackQuery):
    mark_answer = 'good'
    await bot.send_message(call.from_user.id, 'Мы очень рады🤗!!!')
    db.set_answer(call.from_user.id, mark_answer)

@dp.callback_query_handler(text='markN')
async def buydop(call: types.CallbackQuery):
    mark_answer = 'bad'
    await bot.send_message(call.from_user.id, 'Постараемся исправить😁')
    db.set_answer(call.from_user.id, mark_answer)
#сообщения
@dp.message_handler()
async def bot_message(message: types.Message):
    def days_to_seconds(days):
         return days * 24 * 3600
 #расчет оставшегося времени подписки
    def time_sub_day(get_time):
        time_now = int(time.time())
        middle_time = int(get_time) - time_now
        time_end = middle_time // (3600 * 24)
        db.set_time_sub_end(message.from_user.id, time_end)
        if(middle_time <= 0):
            db.del_sub(message.from_user.id)
            return False
        else:
            dt = str(datetime.timedelta(seconds=middle_time))
            dt = dt.replace("days", "дней")
            return dt
    if(db.get_sub(message.from_user.id) == "Владелец"):
        if(message.text == '👤ПРОФИЛЬ'):
            user_sub = time_sub_day(db.get_time_sub(message.from_user.id))
            if(user_sub == False):
                user_sub = "No time"
            else:
                user_sub = "Подписка активна еще: " + user_sub
            user_nickname = "Ваш логин: " + db.get_nickname(message.from_user.id)
            user_email = "Ваша почта: " + db.get_email(message.from_user.id)
            if(db.get_sub(message.from_user.id) == 'Заглянувший'):
                sub = "Ваш статус подписки: " + "👀" + db.get_sub(message.from_user.id) + "👀"
            elif(db.get_sub(message.from_user.id) == 'Интересующийся'):
                sub = "Ваш статус подписки: " + "🧐" + db.get_sub(message.from_user.id) + "🧐"
            elif(db.get_sub(message.from_user.id) == 'Продвинутый'):
                sub = "Ваш статус подписки: " + "🧩" + db.get_sub(message.from_user.id) + "🧩"
            elif(db.get_sub(message.from_user.id) == 'Эксперт'):
                sub = "Ваш статус подписки: " + "😎" + db.get_sub(message.from_user.id) + "😎"
            elif(db.get_sub(message.from_user.id) == 'Владелец'):
                sub = "Ваш статус подписки: " + '👨‍💻' + db.get_sub(message.from_user.id) + '👨‍💻'
            elif(db.get_sub(message.from_user.id) == 'неактивна'):
                sub = "Ваш статус подписки: " + db.get_sub(message.from_user.id) + '❌'
            await bot.send_message(message.from_user.id, user_nickname)
            await bot.send_message(message.from_user.id, user_email)
            await bot.send_message(message.from_user.id, sub)
            queries = "У Вас осталось " + db.get_queries(message.from_user.id) + " обычных запросов✅."
            await bot.send_message(message.from_user.id, queries)
            queries_pr = "У Вас осталось " + db.get_queries_pr(message.from_user.id) + " приветственных запросов.👋."
            await bot.send_message(message.from_user.id, queries_pr)
            if(user_sub != "Нет"):
                await bot.send_message(message.from_user.id, user_sub)
        elif(message.text == 'ИНФА ПО НИКУ🔍'):
            await bot.send_message(message.from_user.id, "Введите логин человека, о котором вы хотите узнать информацию:")
            db.change_action1(message.from_user.id)
        elif(message.text == 'ВЫДАТЬ ПОДПИСКУ✅'):
            await bot.send_message(message.from_user.id, "Введите логин человека, которому вы хотите выдать подписку:")
            db.change_action2(message.from_user.id)
        elif(message.text == 'ВЫДАТЬ ЗАПРОСЫ📫'):
            await bot.send_message(message.from_user.id, "Введите логин человека, которому вы хотите выдать запросы:")
            db.change_action3(message.from_user.id)
        elif(message.text == 'УДАЛИТЬ ПОДПИСКУ❌'):
            await bot.send_message(message.from_user.id, "Введите логин человека, у которого вы хотите удалить подписку:")
            db.change_action4(message.from_user.id)
        elif(message.text == 'УДАЛИТЬ ЗАПРОСЫ🚫'):
            await bot.send_message(message.from_user.id, "Введите логин человека, у которого вы хотите удалить запросы:")
            db.change_action5(message.from_user.id)
        elif(db.get_action(message.from_user.id) == 1):
                nickname = message.text
                email = db.get_email_per(nickname)
                state = db.get_sub_1(nickname)
                promo = db.get_promo_user_1(nickname)
                if(email != None):
                    await bot.send_message(message.from_user.id, "Почта юзера " + message.text + ':' + '\n' + email)
                    await bot.send_message(message.from_user.id, "Статус подписки юзера " + message.text + ':' + '\n' + state)
                    await bot.send_message(message.from_user.id, "Промокод юзера " + message.text + ':' + '\n' + promo)
                    await bot.send_message(message.from_user.id, "Скидка юзера " + message.text + ':' + '\n' + db.get_promo_disc(promo) + '%')
                else:
                    await bot.send_message(message.from_user.id, "Такого пользователя не существует❌")
        #выдача подписки
        elif(db.get_action(message.from_user.id) == 2):
            nickname = message.text
            email = db.get_email_per(nickname)
            if(email != None):
                nickname = message.text
                db.set_give_nickname(message.from_user.id, nickname)
                await bot.send_message(message.from_user.id, "Выберите подписку, которую нужно выдать пользователю - " + nickname, reply_markup=nav.sub_markup1)
        elif(db.get_action(message.from_user.id) == 3):
            nickname = message.text
            email = db.get_email_per(nickname)
            if(email != None):
                db.set_give_nickname(message.from_user.id, nickname)
                await bot.send_message(message.from_user.id, "Выберите сколько запросов выдать пользователю - " + nickname, reply_markup=nav.queries_markup1)
            else:
                await bot.send_message(message.from_user.id, "Такого пользователя не существует❌")
        elif(db.get_action(message.from_user.id) == 4):
            nickname = message.text
            email = db.get_email_per(nickname)
            if(email != None):
                db.del_sub_admin(nickname)
                await bot.send_message(message.from_user.id, f"Подписка у пользователя {nickname} была удалена успешно!😉")
            else:
                await bot.send_message(message.from_user.id, "Такого пользователя не существует❌")
        elif(db.get_action(message.from_user.id) == 5):
            nickname = message.text
            email = db.get_email_per(nickname)
            if(email != None):
                db.del_queries_admin(nickname)
                await bot.send_message(message.from_user.id, f"Запросы у пользователя {nickname} были удалены успешно!😉")
            else:
                await bot.send_message(message.from_user.id, "Такого пользователя не существует❌")
    else:
        if(message.chat.type == 'private'):
                if(message.text == '👤ПРОФИЛЬ'):
                    user_sub = time_sub_day(db.get_time_sub(message.from_user.id))
                    if(user_sub == False):
                        user_sub = "No"
                    else:
                        user_sub = "Подписка активна еще: " + user_sub
                    user_nickname = "Ваш логин: " + db.get_nickname(message.from_user.id)
                    user_email = "Ваша почта: " + db.get_email(message.from_user.id)
                    if(db.get_sub(message.from_user.id) == 'Заглянувший'):
                        sub = "Ваш статус подписки: " + "👀" + db.get_sub(message.from_user.id) + "👀"
                    elif(db.get_sub(message.from_user.id) == 'Интересующийся'):
                        sub = "Ваш статус подписки: " + "🧐" + db.get_sub(message.from_user.id) + "🧐"
                    elif(db.get_sub(message.from_user.id) == 'Продвинутый'):
                        sub = "Ваш статус подписки: " + "🧩" + db.get_sub(message.from_user.id) + "🧩"
                    elif(db.get_sub(message.from_user.id) == 'Эксперт'):
                        sub = "Ваш статус подписки: " + "😎" + db.get_sub(message.from_user.id) + "😎"
                    elif(db.get_sub(message.from_user.id) == 'Владелец'):
                        sub = "Ваш статус подписки: " + '👨‍💻' + db.get_sub(message.from_user.id) + '👨‍💻'
                    elif(db.get_sub(message.from_user.id) == 'неактивна'):
                        sub = "Ваш статус подписки: " + db.get_sub(message.from_user.id) + '❌'
                    await bot.send_message(message.from_user.id, user_nickname)
                    await bot.send_message(message.from_user.id, user_email)
                    await bot.send_message(message.from_user.id, sub)
                        
                    queries = "У Вас осталось " + db.get_queries(message.from_user.id) +" обычных запросов✅."
                    await bot.send_message(message.from_user.id, queries)
                    queries_pr = "У Вас осталось " + db.get_queries_pr(message.from_user.id) + " приветственных запросов👋."
                    await bot.send_message(message.from_user.id, queries_pr)
                    if(user_sub != "No"):
                        await bot.send_message(message.from_user.id, user_sub)
                elif(message.text == '💵КУПИТЬ ПОДПИСКУ'):
                    if(db.get_sub(message.from_user.id) == 'неактивна'):
                        if(db.get_promo_user(message.from_user.id) == 'none'):
                            await bot.send_message(message.from_user.id, 'Выберите подписку:\n(описание всех подписок можно найти, нажав кнопку 📋ОПИСАНИЕ УСЛУГ)', reply_markup=nav.sub_markup)
                        else:
                            disc1 = int(db.get_promo_disc(db.get_promo_user(message.from_user.id)))
                            new = 75 - (75 * (disc1 / 100))
                            new_rounded = round(new, 1)
                            new_str = str(new_rounded)

                            inter = 165 - (165 * (disc1 / 100))
                            inter_rounded = round(inter, 1)
                            inter_str = str(inter_rounded)

                            pro = 265 - (265 * (disc1 / 100))
                            pro_rounded = round(pro, 1)
                            pro_str = str(pro_rounded)

                            exp = new = 355 - (355 * (disc1 / 100))
                            exp_rounded = round(exp, 1)
                            exp_str = int(exp_rounded)

                            sub_markup4 = InlineKeyboardMarkup(row_width=1)
                            btnNew = InlineKeyboardButton(text = f"Заглянувший = {new_str} рублей✅", callback_data='buysub', parse_mode=types.ParseMode.MARKDOWN)
                            btnInter = InlineKeyboardButton(text = f"Интересующийся = {inter_str} рублей✅", callback_data='buysub1')
                            btnPro = InlineKeyboardButton(text = f"Продвинутый = {pro_str} рублей✅", callback_data='buysub2')
                            btnExp = InlineKeyboardButton(text = f"Эксперт = {exp_str} рублей✅", callback_data='buysub3')
                            sub_markup4.insert(btnNew)
                            sub_markup4.insert(btnInter)
                            sub_markup4.insert(btnPro)
                            sub_markup4.insert(btnExp)

                            await bot.send_message(message.from_user.id, 'Выберите подписку:\n(описание всех подписок можно найти, нажав кнопку 📋ОПИСАНИЕ УСЛУГ)', reply_markup=sub_markup4)

                    elif(db.get_sub(message.from_user.id) != 'неактивна'):
                        await bot.send_message(message.from_user.id, "У Вас уже есть Подписка, дождитесь окончания этой подписки и сможете купить новую")
                elif(message.text == '🎂ПРОМОКОД'):
                    if(db.get_promo_user(message.from_user.id) == 'none'):
                        await bot.send_message(message.from_user.id, "Введите специальный промокод🔑:")
                        db.set_promo_action(message.from_user.id, 1)
                    else:
                        await bot.send_message(message.from_user.id, "Промокод уже введен!!!")
                elif(message.text == '➕КУПИТЬ ЗАПРОСЫ'):
                    await bot.send_message(message.from_user.id, 'Хотите докупить запросы? Тогда выбирайте из списка сколько Вам нужно и смело оплачивате сразу, не выходя из бота⬇️\n ❗️❗️❗️Внимание❗️❗️❗️ \nЧтобы воспользоваться запросами, нужна любая подписка из доступных в боте, например Заглянувший', reply_markup=nav.queries_markup)
                elif(message.text == '📋ОПИСАНИЕ УСЛУГ'):
                    new = 'Подписка "👀Заглянувший👀":\n\nЕсли вы выбрали подписку "👀Заглянувший👀", то вы получите:\n\n1. Доступ к запросам, которые помогут вам решать задачи, выполнять домашние работы и многое другое📑.\n2. Вы сможете задать до 60 запросов в месяц🤟, на которые бот ответит немедленно.\n3. Вы также получите возможность участвовать в дальнейших розыгрышах и некоторых событиях в специальной группе только для тех, кто имеет подписку "👀Заглянувший👀" и "🧐Интересующийся🧐"🍀.\n\n(стоимость подписки: 75 рублей в месяц)'
                    inter = 'Подписка "🧐Интересующийся🧐":\n\nЕсли вы выбрали подписку "🧐Интересующийся🧐", то вы получите:\n\n1. Все преимущества подписки "👀Заглянувший👀".\n2. Также возможность задать до 150 запросов в месяц📬.\n3. Вы также получите возможность участвовать в дальнейших розыгрышах и некоторых событиях в специальной группе только для тех, кто имеет подписку "👀Заглянувший👀" и "🧐Интересующийся🧐"🍀.\n\n(стоимость подписки: 165 рублей в месяц)'
                    pro = 'Подписка "🧩Продвинутый🧩":\n\nЕсли вы выбрали подписку "🧩Продвинутый🧩", то вы получите:\n\n1. Все преимущества подписки "🧐Интересующийся🧐".\n2. Также возможность задать до 240 запросов в месяц😎.\n3. Мы также предоставим наиболее быстрый ответ в момент сильной нагрузки на бота.\n4. Вы также получите возможность участвовать в дальнейших розыгрышах и некоторых событиях в специальной группе только для тех, кто имеет подписку "🧩Продвинутый🧩" и "😎Эксперт😎"🍀.(призы намного дороже чем в группе "👀Заглянувший👀" и "🧐Интересующийся🧐")\n\n(стоимость подписки: 265 рублей в месяц)'
                    exp = 'Подписка "😎Эксперт😎":\n\nЕсли вы выбрали подписку "😎Эксперт😎", то вы получите:\n\n1. Все преимущества подписки "🧩Продвинутый🧩".\n2. А также возможность задать до 330 запросов в месяц🤯.\n3. Вы также получите возможность участвовать в дальнейших розыгрышах и некоторых событиях в специальной группе только для тех, кто имеет подписку "🧩Продвинутый🧩" и "😎Эксперт😎"🍀 + дополнительные розыгрыши только для "😎Эксперт😎".(призы намного дороже чем в группе "👀Заглянувший👀" и "🧐Интересующийся🧐")\n\n(стоимость подписки: 355 рублей в месяц)'
                    await bot.send_message(message.from_user.id, 'Все подписки:')
                    await bot.send_message(message.from_user.id, new)
                    await bot.send_message(message.from_user.id, inter)
                    await bot.send_message(message.from_user.id, pro)
                    await bot.send_message(message.from_user.id, exp)
                    await bot.send_message(message.from_user.id, "Запросы:")
                    await bot.send_message(message.from_user.id, "60 запросов = 75 рублей✅\n150 запросов = 165 рублей✅\n240 запросов = 265 рублей✅\n330 запросов = 355 рублей✅\n(запросы выдаются навсегда)")
                elif(message.text == 'ЧТО ЭТО❓'):
                    what = "Здраствуйте!👋 \nПрямо сейчас Вы находитесь в Личном Учебном Ассистенте. Этот бот может помочь вам с вашими вопросами и многим другим. В его функционал входит: написание некоторых творческих работ, сочинений, поиск полезной информации, решение некоторых задачь и так далее. При регистрации выдается 2 бесплатных запроса, чтобы опробывать функциональность бота. Для дальнейшего использования бота необходимо приобрести подписку(подробности по кнопке 💵КУПИТЬ ПОДПИСКУ) или докупить запросы(если они закончились, по кнопке ➕ДОКУПИТЬ ЗАПРОСЫ). Запрос - это каждый вопрос, который Вы задаете боту. Также Вы можете посмотреть сколько запросов осталось у Вас, какой статус у Вашей подписки и какой у Вас ник, нажав на кнопку 👤ПРОФИЛЬ. \nПочта техподдержки: Valentinefukalov@gmail.com.\n Удачного пользования!🍀"
                    await bot.send_message(message.from_user.id, what)
                else:
                    nickname = message.text
                    if(db.get_nickname(message.from_user.id) == 'setnickname'):
                        if(len(message.text) > 15):
                            await bot.send_message(message.from_user.id, "Логин не должен превышать 15 символов")
                        elif(len(message.text) < 4):
                            await bot.send_message(message.from_user.id, "Логин должен быть больше 3 символов")
                        elif('@' in message.text or '/' in message.text):
                            await bot.send_message(message.from_user.id, "Логин не должен содержать запрещенные символы, такие как @ и /")
                        elif(db.nickname_exists(nickname) == True):
                            await bot.send_message(message.from_user.id, "Пользователь с таким логином уже существует")
                        else:
                            nickname = message.text
                            db.set_nickname(message.from_user.id, nickname)
                            if(db.get_nickname(message.from_user.id) != 'setnickname'):
                                await bot.send_message(message.from_user.id, "Логин успешно установлен✅")
                                #await bot.send_message(message.from_user.id, "Укажите вашу электронную почту📬 для полной регистрации (это обязательно❗️❗️❗️)")
                            else:
                                await bot.send_message(message.from_user.id, "Логин не установлен")
                            if(db.get_email(message.from_user.id) != "setemail" and db.get_nickname(message.from_user.id) != 'setnickname'):
                                db.set_signup(message.from_user.id, 'done')
                                await bot.send_message(message.from_user.id, "Регистрация прошла успешно!🎉🎉🎉\nВам выдались 2 приветственных запроса и теперь Вы можете задавать боту вопросы✅.\nПросто пишите вопросы в чат и он будет отвечать на них.", reply_markup= nav.mainMenu)
                            elif(db.get_email(message.from_user.id) == 'setemail'):
                                await bot.send_message(message.from_user.id, "Введите вашу почту📬 для полной регистрации(это обязательно❗️❗️❗️)")
                            else:
                                await bot.send_message(message.from_user.id, "Введите ваш логин!")
                    elif(db.get_email(message.from_user.id) == 'setemail'):
                        if(len(message.text) > 40):
                            await bot.send_message(message.from_user.id, "Почта не должна быть больше 40 символов")
                        elif(not '@' in message.text or not ('.com' in message.text or '.ru' in message.text)):
                            await bot.send_message(message.from_user.id, "Почта должна содержать символы такие как @ и (.com или .ru)")
                        else:
                            db.set_email(message.from_user.id, message.text)
                            await bot.send_message(message.from_user.id, "Почта успешно установлена✅")
                            await bot.send_message(message.from_user.id, "Регистрация прошла успешно!🎉🎉🎉\nВам выдались 2 приветственных запроса и теперь Вы можете задавать боту вопросы✅.\nПросто пишите вопросы в чат и он будет отвечать на них.", reply_markup= nav.mainMenu)
                    elif(db.get_promo_action(message.from_user.id) == '1'):
                        disc = db.get_promo_disc(message.text)
                        queries = db.get_promo_queries(message.text)
                        if(db.get_promo_name(message.text) != None):
                            await bot.send_message(message.from_user.id, f'Промокод был успешно установлен✅!\nВаша скидка на оплату подписки составляет {disc}%.🌟\nИ так же +{queries} при оплате подписки.🔔')
                            db.set_promo(message.from_user.id, message.text)
                        else:
                            await bot.send_message(message.from_user.id, 'Не удалось найти такого промокода❌')
                        db.set_promo_action(message.from_user.id, 0)
                    else:
                        user_sub = time_sub_day(db.get_time_sub(message.from_user.id))
                        if(((db.get_sub(message.from_user.id) != 'неактивна') and (db.get_queries(message.from_user.id) != '0') and (user_sub != False)) or db.get_queries_pr(message.from_user.id) != '0'):
                            if(db.get_sub(message.from_user.id) == "Заглянувший" or db.get_queries_pr(message.from_user.id) != '0'):
                                queries = db.get_queries(message.from_user.id)
                                update(messages, "user", message.text)

                                response = openai.ChatCompletion.create(
                                    model="gpt-3.5-turbo",  # Новая модель с контекстом
                                    messages=messages,   # База данных на основе словаря
                                    max_tokens=2000,
                                )

                                await message.answer(response['choices'][0]['message']['content'] + '\n\n' + 'Вы удовлетворены ответом бота?', reply_markup= nav.mark_YN, parse_mode="markdown")
                                if(db.get_queries_pr(message.from_user.id) != '0'):
                                    db.del_queries_pr(message.from_user.id)
                                    await bot.send_message(message.from_user.id, "У Вас осталось " + db.get_queries_pr(message.from_user.id) + " бесплатных запросов")
                                else:
                                    db.del_queries(message.from_user.id)
                                    await bot.send_message(message.from_user.id, "У Вас осталось " + db.get_queries(message.from_user.id) + " запросов")
                            elif(db.get_sub(message.from_user.id) == "Интересующийся"):
                                queries = db.get_queries(message.from_user.id)
                                update(messages, "user", message.text)

                                response = openai.ChatCompletion.create(
                                    model="gpt-3.5-turbo",  # Новая модель с контекстом
                                    messages=messages,   # База данных на основе словаря
                                    max_tokens=2000,
                                )

                                await message.answer(response['choices'][0]['message']['content'] + '\n\n' + 'Вы удовлетворены ответом бота?', reply_markup= nav.mark_YN, parse_mode="markdown")
                                if(db.get_queries_pr(message.from_user.id) != '0'):
                                    db.del_queries_pr(message.from_user.id)
                                    await bot.send_message(message.from_user.id, "У Вас осталось " + db.get_queries_pr(message.from_user.id) + " бесплатных запросов")
                                else:
                                    db.del_queries(message.from_user.id)
                                    await bot.send_message(message.from_user.id, "У Вас осталось " + db.get_queries(message.from_user.id) + " запросов")
                            elif(db.get_sub(message.from_user.id) == "Продвинутый"):
                                queries = db.get_queries(message.from_user.id)
                                update(messages, "user", message.text)

                                response = openai.ChatCompletion.create(
                                    model="gpt-3.5-turbo",  # Новая модель с контекстом
                                    messages=messages,   # База данных на основе словаря
                                    max_tokens=2000,
                                )

                                await message.answer(response['choices'][0]['message']['content'] + '\n\n' + 'Вы удовлетворены ответом бота?', reply_markup= nav.mark_YN, parse_mode="markdown")
                                if(db.get_queries_pr(message.from_user.id) != '0'):
                                    db.del_queries_pr(message.from_user.id)
                                    await bot.send_message(message.from_user.id, "У Вас осталось " + db.get_queries_pr(message.from_user.id) + " бесплатных запросов")
                                else:
                                    db.del_queries(message.from_user.id)
                                    await bot.send_message(message.from_user.id, "У Вас осталось " + db.get_queries(message.from_user.id) + " запросов")
                            elif(db.get_sub(message.from_user.id) == "Эксперт"):
                                queries = db.get_queries(message.from_user.id)
                                update(messages, "user", message.text)

                                response = openai.ChatCompletion.create(
                                    model="gpt-3.5-turbo",  # Новая модель с контекстом
                                    messages=messages,   # База данных на основе словаря
                                    max_tokens=2000,
                                )

                                await message.answer(response['choices'][0]['message']['content'] + '\n\n' + 'Вы удовлетворены ответом бота?', reply_markup= nav.mark_YN, parse_mode="markdown")
                                if(db.get_queries_pr(message.from_user.id) != '0'):
                                    db.del_queries_pr(message.from_user.id)
                                    await bot.send_message(message.from_user.id, "У Вас осталось " + db.get_queries_pr(message.from_user.id) + " бесплатных запросов")
                                else:
                                    db.del_queries(message.from_user.id)
                                    await bot.send_message(message.from_user.id, "У Вас осталось " + db.get_queries(message.from_user.id) + " запросов")
                            elif(db.get_sub(message.from_user.id) == "Владелец"):
                                queries = db.get_queries(message.from_user.id)
                                update(messages, "user", message.text)

                                response = openai.ChatCompletion.create(
                                    model="gpt-3.5-turbo",  # Новая модель с контекстом
                                    messages=messages,   # База данных на основе словаря
                                    max_tokens=2000,
                                )

                                await message.answer(response['choices'][0]['message']['content'] + '\n\n' + 'Вы удовлетворены ответом бота?', reply_markup= nav.mark_YN, parse_mode="markdown")
                                if(db.get_queries_pr(message.from_user.id) != '0'):
                                    db.del_queries_pr(message.from_user.id)
                                    await bot.send_message(message.from_user.id, "У Вас осталось " + db.get_queries_pr(message.from_user.id) + " бесплатных запросов")
                                else:
                                    db.del_queries(message.from_user.id)
                                    await bot.send_message(message.from_user.id, "У Вас осталось " + db.get_queries(message.from_user.id) + " запросов")
                        elif(db.get_sub(message.from_user.id) == 'неактивна'):
                            await bot.send_message(message.from_user.id, "Ваша подписка неактивна❌. Чтобы пользоваться ботом купите подписку, нажав на кнопку 💵КУПИТЬ ПОДПИСКУ.", reply_markup= nav.mainMenu)
                        elif(db.get_queries(message.from_user.id) == '0'):
                            await bot.send_message(message.from_user.id, "У Вас закончились запросы❌. Чтобы докупить запросы, нажмите на кнопку ➕ДОКУПИТЬ ЗАПРОСЫ", reply_markup= nav.mainMenu)
        
if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)
