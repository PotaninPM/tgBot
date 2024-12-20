from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, InlineKeyboardMarkup, InlineKeyboardButton

btnProfile = KeyboardButton('👤ПРОФИЛЬ')
btnDes = KeyboardButton('📋ОПИСАНИЕ УСЛУГ')
btnBuy = KeyboardButton('💵КУПИТЬ ПОДПИСКУ')
btnBuyQ = KeyboardButton('➕КУПИТЬ ЗАПРОСЫ')
#btnMark = KeyboardButton('🌟ОЦЕНИТЬ БОТА')
btnPromo = KeyboardButton('🎂ПРОМОКОД')
btnWhat = KeyboardButton('ЧТО ЭТО❓')

btnP = KeyboardButton('👤ПРОФИЛЬ')
btnIP = KeyboardButton('ИНФА ПО НИКУ🔍')
btnGS = KeyboardButton('ВЫДАТЬ ПОДПИСКУ✅')
btnGQ = KeyboardButton('ВЫДАТЬ ЗАПРОСЫ📫')
btnDS = KeyboardButton('УДАЛИТЬ ПОДПИСКУ❌')
btnDQ = KeyboardButton('УДАЛИТЬ ЗАПРОСЫ🚫')

queries_markup = InlineKeyboardMarkup(row_width=1)
btnBuyDop = InlineKeyboardButton(text = "60 запросов = 75 рублей✅", callback_data='buydop')
btnBuyDop1 = InlineKeyboardButton(text = "150 запросов = 165 рублей✅", callback_data='buydop1')
btnBuyDop2 = InlineKeyboardButton(text = "240 запросов = 265 рублей✅", callback_data='buydop2')
btnBuyDop3 = InlineKeyboardButton(text = "330 запросов = 355 рублей✅", callback_data='buydop3')
queries_markup.insert(btnBuyDop)
queries_markup.insert(btnBuyDop1)
queries_markup.insert(btnBuyDop2)
queries_markup.insert(btnBuyDop3)

queries_markup1 = InlineKeyboardMarkup(row_width=1)
btnDop_1 = InlineKeyboardButton(text = "1 запрос✅", callback_data='dop_1')
btnDop = InlineKeyboardButton(text = "60 запросов✅", callback_data='dop')
btnDop1 = InlineKeyboardButton(text = "150 запросов✅", callback_data='dop1')
btnDop2 = InlineKeyboardButton(text = "240 запросов✅", callback_data='dop2')
btnDop3 = InlineKeyboardButton(text = "330 запросов✅", callback_data='dop3')
queries_markup1.insert(btnDop_1)
queries_markup1.insert(btnDop)
queries_markup1.insert(btnDop1)
queries_markup1.insert(btnDop2)
queries_markup1.insert(btnDop3)

mark_markup = InlineKeyboardMarkup(row_width=1)
btnMark0 = InlineKeyboardButton(text = "5 = все идеально🌟", callback_data='mark5')
btnMark1 = InlineKeyboardButton(text = "4 = хорошо, но есть недочеты😀", callback_data='mark4')
btnMark2 = InlineKeyboardButton(text = "3 = есть проблемы😕", callback_data='mark3')
btnMark3 = InlineKeyboardButton(text = "2 = просто ужасно😡", callback_data='mark2')
mark_markup.insert(btnMark0)
mark_markup.insert(btnMark1)
mark_markup.insert(btnMark2)
mark_markup.insert(btnMark3)

#оценка ответа бота
mark_YN = InlineKeyboardMarkup(row_width=2)
btnMarkYes = InlineKeyboardButton(text = "Да✅", callback_data='markY')
btnMarkNo = InlineKeyboardButton(text = "Нет❌", callback_data='markN')
mark_YN.insert(btnMarkYes)
mark_YN.insert(btnMarkNo)

sub_markup = InlineKeyboardMarkup(row_width=1)
btnNew = InlineKeyboardButton(text = "Заглянувший = 75 рублей✅", callback_data='buysub')
btnInter = InlineKeyboardButton(text = "Интересующийся = 165 рублей✅", callback_data='buysub1')
btnPro = InlineKeyboardButton(text = "Продвинутый = 265 рублей✅", callback_data='buysub2')
btnExp = InlineKeyboardButton(text = "Эксперт = 355 рублей✅", callback_data='buysub3')
sub_markup.insert(btnNew)
sub_markup.insert(btnInter)
sub_markup.insert(btnPro)
sub_markup.insert(btnExp)

sub_markup1 = InlineKeyboardMarkup(row_width=1)
btnNew1 = InlineKeyboardButton(text = "Заглянувший✅", callback_data='sub')
btnInter1 = InlineKeyboardButton(text = "Интересующийся✅", callback_data='sub1')
btnPro1 = InlineKeyboardButton(text = "Продвинутый✅", callback_data='sub2')
btnExp1 = InlineKeyboardButton(text = "Эксперт✅", callback_data='sub3')
sub_markup1.insert(btnNew1)
sub_markup1.insert(btnInter1)
sub_markup1.insert(btnPro1)
sub_markup1.insert(btnExp1)

mainMenu1 = ReplyKeyboardMarkup(resize_keyboard=True)
mainMenu1.add(btnP,btnIP, btnGS, btnGQ, btnDS, btnDQ)

mainMenu = ReplyKeyboardMarkup(resize_keyboard=True)
mainMenu.add(btnProfile,btnDes,btnPromo, btnBuy, btnBuyQ, btnWhat)