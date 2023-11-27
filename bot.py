import pandas as pd
import joblib
import telebot
from telebot import types

# Токен бота (ключ для доступа и программирования бота)
TOKEN = '6834482404:AAE9B-HxF9cRn8xHI8J2VeC5eoXCnwq9wOE' 
bot = telebot.TeleBot(TOKEN)

# Загрузка модели, которую будем использовать для предсказания
catboost = joblib.load('CatBoostRegressor.pkl')

# Загружаем набор данных для рекомендаций
df = pd.read_csv('Цены_на_недвижимость_обработанный_набор.csv')





# Обработчик команды /start (что сделать чтобы начать работать с ботом)
@bot.message_handler(commands=['start'])
def handle_start(message):

    # Отправляем сообщение без клавиатуры
    bot.send_message(message.chat.id, """Добро пожаловать! 
Я - ваш персональный помощник по предсказанию стоимости квартир, а так же по поиску актуальных объявлений в соответствии с вашим запросом.               
Для перехода в режим предсказания, введите /predict. 
Для получения дополнительной информации и информации как пользоваться ботом, введите /help.""")





# Обработчик команды /help (помощь с работой бота)
@bot.message_handler(commands=['help'])
def handle_help(message):

    # Отправляем сообщение без клавиатуры
    bot.send_message(message.chat.id, """
*Инструкция по использованию бота для предсказания стоимости квартир*

*Начало работы*
Для начала работы с ботом отправьте команду /start.
Бот приветствует вас и предоставляет доступ к функциональности.
                     
*Предсказание стоимости*
Чтобы предсказать стоимость квартиры, отправьте команду /predict.
Бот будет задавать вам вопросы о характеристиках квартиры, таких как площадь, количество комнат, расположение и другие. Отвечайте на вопросы бота, предоставляя необходимые данные. По завершении опроса, бот предоставит оценку стоимости квартиры.

*Инструкции*
Чтобы получить инструкцию по использованию бота, отправьте команду /help.
Бот предоставит вам краткую справку о доступных командах и их функциональности.          

*Информация о проекте*
Если вас интересует информация о проекте, отправьте команду /about.
Бот предоставит вам обзор проекта, его целей и особенностей.   

*Завершение диалога*
Для завершения текущего диалога с ботом и возврата в главное меню, используйте команду /stop.

*Обратная связь и поддержка*
Вы можете отправить обратную связь, предложения или комментарии о работе бота, используя команду /feedback.
""", parse_mode="Markdown")




# Обработсик команды /about (Информация о проекте)
@bot.message_handler(commands=['about'])
def handle_about(message):
    bot.send_message(message.chat.id, """ 
Этот бот - ваш персональный помощник в оценке стоимости квартир, работающий на основе передовых технологий искусственного интеллекта. Просто введите ключевые параметры, запрошенные ботом, и получите мгновенную оценку стоимости. Наш алгоритм обучен на обширной базе данных рыночных цен на недвижимость, что делает наши прогнозы точными и надежными.

Кроме того, в зависимости от ваших критериев поиска, бот поможет вам найти актуальные объявления о продаже квартир, предоставляя вам прямые ссылки для удобства просмотра и сравнения.

Автор бота - @black_style_27_27_27

Ваша обратная связь очень важна (/feedback). Не стесняйтесь делиться этим ботом для большего охвата аудиторий и получения большего количества оценок.""")




# Обработчик команды /stop
@bot.message_handler(commands=['stop'])
def handle_stop(message):
    # Ваш код для завершения текущего диалога или возвращения в главное меню
    bot.send_message(message.chat.id, "Вы завершили текущий диалог. Вы можете выполнить другие команды.")






# Создаем DataFrame для хранения отзывов
feedback_df = pd.DataFrame(columns=["Отзывы"])

# Обработчик команды /feedback
@bot.message_handler(commands=['feedback'])
def handle_feedback_start(message):
    # Посылаем сообщение с просьбой ввести отзыв
    bot.send_message(message.chat.id, "Пожалуйста, введите ваш отзыв:")

    # Регистрируем следующий шаг - ожидание ввода отзыва
    bot.register_next_step_handler(message, get_feedback)

# Функция для обработки ввода отзыва
def get_feedback(message):
    user_feedback = message.text

    if user_feedback.lower() == "/stop":
        # Пользователь хочет прервать операцию
        handle_stop(message)
        return

    # Добавляем отзыв в DataFrame
    feedback_df.loc[len(feedback_df)] = user_feedback

    # Сохранение отзыва
    feedback_df.to_csv('Отзывы.csv')

    # Сообщаем пользователю, что отзыв был успешно отправлен
    bot.send_message(message.chat.id, "Ваш отзыв был успешно отправлен. Спасибо за ваше мнение!")





# Обработчик команды /predict (для предсказания цен на квартиры)

# Список для хранения ответов пользователя
user_responses = []

# Обработчик команды /predict для начала предсказания
@bot.message_handler(commands=['predict'])
def handle_predict_start(message):
    # Очищаем список ответов от предыдущих значений
    user_responses.clear()

    # Задаем варианты ответа в виде кнопок
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
    button1 = types.KeyboardButton("Вторичное")
    button2 = types.KeyboardButton("Новостройка")
    markup.add(button1, button2)

    # Тип квартиры
    bot.send_message(message.chat.id, "Выберите тип квартиры:", reply_markup=markup)
    bot.register_next_step_handler(message, get_apartment_type)

# Функция для обработки выбора пользователя о типе квартиры
def get_apartment_type(message):
    user_response = message.text

    if user_response.lower() == "/stop":
        # Пользователь хочет прервать операцию
        handle_stop(message)
        return
    
    if user_response not in ["Вторичное", "Новостройка"]:
        # Если введенное значение не соответствует ожидаемым, повторяем ввод
        bot.send_message(message.chat.id, "Пожалуйста, выберите один из предложенных вариантов.")
        bot.register_next_step_handler(message, get_apartment_type)
        return
    
    user_responses.append(user_response)

    # Площадь квартиры
    bot.send_message(message.chat.id, "Введите площадь квартиры (в квадратных метрах):")
    bot.register_next_step_handler(message, get_area)

# Функция для обработки ответа пользователя о площади квартиры
def get_area(message):
    user_response = message.text

    if user_response.lower() == "/stop":
        # Пользователь хочет прервать операцию
        handle_stop(message)
        return
    try:
        # Попытка преобразовать введенный текст в число
        area = float(user_response)  
        user_responses.append(area)  # Добавляем число в список
    except ValueError:
        # Если не удалось преобразовать в число, сообщаем об ошибке
        bot.send_message(message.chat.id, "Пожалуйста, введите число")
        bot.register_next_step_handler(message, get_area)  # Повторяем вопрос о площади
        return

    # Минут до метро
    bot.send_message(message.chat.id, "Введите количество минут от квартиры до метро:")
    bot.register_next_step_handler(message, get_metro_min)

# Функция для обработки минут до метро 
def get_metro_min(message):
    user_response = message.text

    if user_response.lower() == "/stop":
        # Пользователь хочет прервать операцию
        handle_stop(message)
        return

    try:
        # Попытка преобразовать введенный текст в число
        min = float(user_response)  
        user_responses.append(min)  # Добавляем число в список
    except ValueError:
        # Если не удалось преобразовать в число, сообщаем об ошибке
        bot.send_message(message.chat.id, "Пожалуйста, введите число")
        bot.register_next_step_handler(message, get_metro_min)  # Повторяем вопрос о минутах
        return


    # Станция метро
    bot.send_message(message.chat.id, "Введите станцию метро:")
    bot.register_next_step_handler(message, get_metro_station)

# Станция метро
def get_metro_station(message):
    user_response = message.text.lower() # Преобразовываем станцию метро, чтобы была с маленькой буквы

    if user_response.lower() == "/stop":
        # Пользователь хочет прервать операцию
        handle_stop(message)
        return

    if user_response not in ['опалиха', 'павшино', 'мякинино', 'строгино', 'нахабино',
       'красногорская', 'тушинская', 'аникеевка', 'волоколамская',
       'пенягино', 'митино', 'пятницкое шоссе', 'чеховская', 'арбатская',
       'фили', 'белорусская', 'кропоткинская', 'спортивная',
       'алексеевская', 'ростокино', 'китай-город', 'вднх', 'динамо',
       'филатов луг', 'раменки', 'минская', 'аминьевская', 'давыдково',
       'фрунзенская', 'улица 1905 года', 'кунцевская', 'шелепиха',
       'молодёжная', 'беговая', 'бауманская', 'славянский бульвар',
       'новокузнецкая', 'парк культуры', 'смоленская', 'пушкинская',
       'комсомольская', 'серпуховская', 'трубная', 'народное ополчение',
       'киевская', 'технопарк', 'преображенская площадь', 'павелецкая',
       'красные ворота', 'тверская', 'петровский парк', 'аэропорт',
       'площадь ильича', 'краснопресненская', 'курская', 'третьяковская',
       'охотный ряд', 'деловой центр', 'полянка',
       'волгоградский проспект', 'выставочная', 'тестовская',
       'сходненская', 'прокшино', 'окружная', 'рабочий посёлок',
       'селигерская', 'ломоносовский проспект', 'саларьево', 'бибирево',
       'печатники', 'новогиреево', 'бульвар рокоссовского',
       'филёвский парк', 'проспект мира', 'рязанский проспект',
       'профсоюзная', 'ботанический сад', 'панфиловская', 'беломорская',
       'цветной бульвар', 'парк победы', 'багратионовская',
       'нагатинский затон', 'крылатское', 'щукинская', 'цска',
       'библиотека и ленина', 'марьина роща', 'баррикадная', 'боровицкая',
       'добрынинская', 'маяковская', 'новослободская', 'чистые пруды',
       'таганская', 'шаболовская', 'балтийская', 'мнёвники',
       'кутузовская', 'тульская', 'хорошёво', 'тургеневская',
       'новаторская', 'зил', 'международная', 'менделеевская',
       'автозаводская', 'коммунарка', 'университет', 'кантемировская',
       'полежаевская', 'театральная', 'проспект вернадского', 'калужская',
       'академическая', 'александровский сад', 'октябрьское поле',
       'коломенская', 'бульвар дмитрия донского', 'спартак', 'сокол',
       'матвеевская', 'стрешнево', 'речной вокзал', 'водный стадион',
       'нагорная', 'кузнецкий мост', 'войковская', 'новые черёмушки',
       'сретенский бульвар', 'дмитровская', 'ленинский проспект',
       'пролетарская', 'стахановская', 'аэропорт внуково',
       'выставочный центр', 'свиблово', 'ясенево', 'тимирязевская',
       'щёлковская', 'солнцево', 'зябликово', 'новопеределкино',
       'карамышевская', 'рижская', 'угрешская', 'локомотив', 'пражская',
       'рассказовка', 'гражданская', 'подольск', 'перерва', 'сокольники',
       'царицыно', 'бунинская аллея', 'улица старокачаловская',
       'черкизовская', 'ольховая', 'калитники', 'курьяново',
       'бульвар адмирала ушакова', 'первомайская', 'хорошёвская',
       'юго-западная', 'ховрино', 'физтех', 'бескудниково', 'москворечье',
       'волжская', 'электрозаводская', 'говорово', 'медведково',
       'савёловская', 'мичуринский проспект', 'владыкино', 'тропарёво',
       'чкаловская', 'красный балтиец', 'зюзино', 'сухаревская', 'окская',
       'красносельская', 'нижегородская', 'андроновка', 'семёновская',
       'зеленоград — крюково', 'озёрная', 'бутырская', 'некрасовка',
       'коптево', 'римская', 'лихоборы', 'кузьминки',
       'улица скобелевская', 'выхино', 'нахимовский проспект', 'бутово',
       'авиамоторная', 'южная', 'силикатная', 'внуково', 'трикотажная',
       'тёплый стан', 'лесопарковая', 'братиславская',
       'шоссе энтузиастов', 'улица горчакова', 'москва-товарная',
       'алтуфьево', 'новокосино', 'новохохловская',
       'улица академика янгеля', 'чертановская', 'коньково',
       'красногвардейская', 'орехово', 'пыхтино', 'остафьево',
       'бабушкинская', 'юго-восточная', 'люблино', 'новодачная',
       'алма-атинская', 'планерная', 'зорге', 'верхние лихоборы',
       'фонвизинская', 'крымская', 'красный строитель', 'севастопольская',
       'лефортово', 'площадь гагарина', 'санино', 'каховская', 'вешняки',
       'текстильщики', 'марксистская', 'улица академика королёва','варшавская', 'студенческая', 'достоевская', 'октябрьская',
       'лужники', 'площадь революции', 'лианозово', 'воробьёвы горы',
       'очаково', 'воронцовская', 'терехово', 'нагатинская',
       'кожуховская', 'щербинка', 'дегунино', 'депо', 'новоподрезково',
       'яхромская', 'румянцево', 'дубровка', 'хлебниково',
       'соколиная гора', 'верхние котлы', 'отрадное', 'сетунь',
       'лухмановская', 'покровское', 'щелковская', 'каширская',
       'хорошево', 'домодедовская', 'молодежная', 'марьино',
       'улица дмитриевского', 'перово', 'шипиловская', 'тропарево',
       'белокаменная', 'кленовый бульвар', 'беляево', 'савеловская',
       'новые черемушки', 'борисово', 'боровское шоссе', 'жулебино',
       'аннино', 'измайловская', 'марьина роща (шереметьевская)',
       'лермонтовский проспект', 'немчиновка', 'теплый стан',
       'варшавская (коломенское)', 'пионерская', 'новоясеневская',
       'филевский парк', 'воробьевы горы', 'измайлово', 'битцевский парк',
       'партизанская', 'семеновская', 'крестьянская застава', 'марк',
       'косино', 'долгопрудная', 'петровско-разумовская', 'лубянка',
       'библиотека им. ленина', 'терехово (мнёвники)', 'сколково',
       'битца', 'котельники']:
        # Если введенное значение не соответствует ожидаемым, повторяем ввод
        bot.send_message(message.chat.id, "Пожалуйста, введите другую станцию метро")
        bot.register_next_step_handler(message, get_metro_station)
        return
    
    user_responses.append(user_response)

    # Регион
    # Задаем варианты ответа в виде кнопок
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
    button1 = types.KeyboardButton("Москва")
    button2 = types.KeyboardButton("Московская область")
    markup.add(button1, button2)

    bot.send_message(message.chat.id, "Выберете регион:", reply_markup=markup)
    bot.register_next_step_handler(message, get_region)

# Функция для обработки выбора пользователя о регионе
def get_region(message):
    user_response = message.text

    if user_response.lower() == "/stop":
        # Пользователь хочет прервать операцию
        handle_stop(message)
        return

    if user_response not in ["Москва", "Московская область"]:
        # Если введенное значение не соответствует ожидаемым, повторяем ввод
        bot.send_message(message.chat.id, "Пожалуйста, выберите один из предложенных вариантов.")
        bot.register_next_step_handler(message, get_region)
        return
    
    user_responses.append(user_response)

    # Количество комнат
    bot.send_message(message.chat.id, "Введите количество комнат:")
    bot.register_next_step_handler(message, get_room)

# функция для обработки количества комнат
def get_room(message):
    user_response = message.text

    if user_response.lower() == "/stop":
        # Пользователь хочет прервать операцию
        handle_stop(message)
        return

    try:
        # Попытка преобразовать введенный текст в число
        room = float(user_response)  
        user_responses.append(room)  # Добавляем число в список
    except ValueError:
        # Если не удалось преобразовать в число, сообщаем об ошибке
        bot.send_message(message.chat.id, "Пожалуйста, введите число")
        bot.register_next_step_handler(message, get_room)  # Повторяем вопрос о минутах
        return

    # Площадь кухни
    bot.send_message(message.chat.id, "Введите площадь кухни (в квадратных метрах):")
    bot.register_next_step_handler(message, get_kitchen)

# Обработка площади кухни
def get_kitchen(message):
    user_response = message.text

    if user_response.lower() == "/stop":
        # Пользователь хочет прервать операцию
        handle_stop(message)
        return

    try:
        # Попытка преобразовать введенный текст в число
        kitchen = float(user_response)  
        user_responses.append(kitchen)  # Добавляем число в список
    except ValueError:
        # Если не удалось преобразовать в число, сообщаем об ошибке
        bot.send_message(message.chat.id, "Пожалуйста, введите число")
        bot.register_next_step_handler(message, get_kitchen)  # Повторяем вопрос о минутах
        return

    # Этаж
    bot.send_message(message.chat.id, "Введите этаж на котором буде находится квартира:")
    bot.register_next_step_handler(message, get_floor)

# Функция для обработки этажа на которм квартира 
def get_floor(message):
    user_response = message.text

    if user_response.lower() == "/stop":
        # Пользователь хочет прервать операцию
        handle_stop(message)
        return

    try:
        # Попытка преобразовать введенный текст в число
        floor = float(user_response)  
        user_responses.append(floor)  # Добавляем число в список
    except ValueError:
        # Если не удалось преобразовать в число, сообщаем об ошибке
        bot.send_message(message.chat.id, "Пожалуйста, введите число")
        bot.register_next_step_handler(message, get_floor)  # Повторяем вопрос о минутах
        return

    # Количество этажей в доме всего
    bot.send_message(message.chat.id, "Введите сколько всего этажей в доме:")
    bot.register_next_step_handler(message, get_floor_count)

# Обработка всего количество этажей 
def get_floor_count(message):
    user_response = message.text

    if user_response.lower() == "/stop":
        # Пользователь хочет прервать операцию
        handle_stop(message)
        return

    try:
        # Попытка преобразовать введенный текст в число
        floor_count = float(user_response)  
        user_responses.append(floor_count)  # Добавляем число в список
    except ValueError:
        # Если не удалось преобразовать в число, сообщаем об ошибке
        bot.send_message(message.chat.id, "Пожалуйста, введите число")
        bot.register_next_step_handler(message, get_floor_count)  # Повторяем вопрос о минутах
        return
    
    # Ремонт 
    # Задаем варианты ответа в виде кнопок
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
    button1 = types.KeyboardButton("Косметический")
    button2 = types.KeyboardButton("Евроремонт")
    button3 = types.KeyboardButton("Без ремонта")
    button4 = types.KeyboardButton("Дизайнерский")
    markup.add(button1, button2, button3, button4)

    bot.send_message(message.chat.id, "Выберете тип ремонта:", reply_markup=markup)
    bot.register_next_step_handler(message, get_repair)

# Получение типа ремонта и преобразование ответов пользователя 
def get_repair(message):
    user_response = message.text

    if user_response.lower() == "/stop":
        # Пользователь хочет прервать операцию
        handle_stop(message)
        return
    
    if user_response not in ['Косметический', 'Евроремонт', 'Без ремонта', 'Дизайнерский']:
        # Если введенное значение не соответствует ожидаемым, повторяем ввод
        bot.send_message(message.chat.id, "Пожалуйста, выберите один из предложенных вариантов.")
        bot.register_next_step_handler(message, get_repair)
        return
    
    user_responses.append(user_response)
    print(user_responses)

    # После получения списка переходим к созданию DataFrame
    data = pd.DataFrame()
    data['Тип квартиры'] = [user_responses[0]] 
    data['Станция метро']  = [user_responses[3]]
    data['Минут до метро'] = [user_responses[2]]
    data['Регион'] = [user_responses[4]]
    data['Количество комнат'] = [user_responses[5]]
    data['Площадь'] = [user_responses[1]]
    data['Кухня площадь'] = [user_responses[6]]
    data['Этаж'] = [user_responses[7]]
    data['Количество этажей'] = [user_responses[8]]
    data['Ремонт'] = [user_responses[9]]

    
    # Вызываем функцию для предсказания
    predicted_values = make_prediction(data)
    
    # Форматирование числа с разделением пробелами
    predicted_values = ', '.join(['{:,.0f}'.format(value).replace(',', ' ') for value in predicted_values])
    print(predicted_values)
    
    # Отправка предсказания
    bot.send_message(message.chat.id, f"Цена квартиры по заданным параметрам: {predicted_values}")



    # Рекомендации 
    ans = recommendations(df, user_responses[3], user_responses[5])
    if len(ans) >= 5:
        links = list(ans.sort_values(by='Цена')['Ссылка'].head(5))
        formatted_links = "\n".join(links)
        bot.send_message(message.chat.id, f"Список квартир по вашему запросу: {formatted_links }")
    elif len(ans) == 0:
        bot.send_message(message.chat.id, "По вашему запросу не найдено рекомендаций")
    else :
        links = list(ans.sort_values(by='Цена')['Ссылка'])
        formatted_links = "\n".join(links)
        bot.send_message(message.chat.id, f"Список квартир по вашему запросу: {formatted_links}")


# Функция для рекомендации жилья
def recommendations(df, metro, num_room):
    res = df[(df['Станция метро'] == metro) &\
             (df['Количество комнат'] == num_room)]  

    return res

# Функция предсказания
def make_prediction(data):
    pred = catboost.predict(data)
    return pred




# Включение бота 
bot.polling(none_stop=True)