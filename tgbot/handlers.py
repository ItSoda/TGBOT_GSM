import logging
import telebot
from django.conf import settings
from telebot import types

from .models import Admin, Brand, Category, Product, UserBot, News

logger = logging.getLogger("main")

# Вставляем токен бота
bot = telebot.TeleBot(settings.TELEGRAM_BOT_TOKEN)


##################################################### CLIENT PART #######################################################################
# Обработчик команды /start
@bot.message_handler(commands=["start"])
def handle_start(message):
    user_id = message.chat.id
    username = message.from_user.username
    first_name = message.from_user.first_name
    last_name = message.from_user.last_name
    markup = types.ForceReply(selective=False)
    try:
        if UserBot.objects.get(user_id=user_id):
            bot.send_message(
                message.chat.id,
                f"Привет, {first_name}! \nЭто компания МАСТЕР GSM ИСТРА. \n\nВоспользуйся /help для подробной информации или /catalog чтобы посмотреть наши товары.",
                reply_markup=markup,
            )

    except UserBot.DoesNotExist:
        UserBot.objects.create(
            user_id=user_id,
            username=username,
            first_name=first_name,
            last_name=last_name,
        )
        bot.send_message(
            message.chat.id,
            f"Привет, {first_name}! Это компания МАСТЕР GSM ИСТРА. \n\nВоспользуйся /help для подробной информации или /catalog чтобы посмотреть наши товары.",
            reply_markup=markup,
        )


@bot.message_handler(commands=["help"])
def help(message):
    markup = types.ForceReply(selective=False)
    text = "Команды:\n\n/start - Перезапуск бота \n\n/help - Помощь \n\n/catalog - Список наших товаров \n\n/contacts - Наши контакты \n\n/about_us - О нас"
    bot.send_message(
        message.chat.id,
        f"Приветствую {message.from_user.first_name}\n \n{text}",
        parse_mode="html",
        reply_markup=markup,
    )


@bot.message_handler(commands=["catalog"])
def product_catalog(message):
    categories = Category.objects.all()

    keyboard = types.ReplyKeyboardMarkup(row_width=1, resize_keyboard=True)

    for category in categories:
        products = Product.objects.filter(category=category)
        button = types.KeyboardButton(text=f"{category.name} ({products.count()})")
        keyboard.add(button)

    bot.send_message(
        message.chat.id,
        "МАСТЕР GSM ИСТРА. \nТЕЛЕФОН: 89670831183 \nНОВЫЕ ТОПОВЫЕ ТЕЛЕФОНЫ ПО РАЗУМНЫМ ЦЕНАМ! ДЛЯ ЗАКАЗА ПИШИТЕ СООБЩЕНИЯ В ЛИЧКУ. \n Внимание!!!\nГарантия на продукцию Apple 🇺🇸/🇯🇵/🇪🇺- 5 ДНЕЙ (проверка заводского брака). \nСрок гарантии указан с даты покупки телефона. \nПри наличии косметических дефектов гарантия распространяется \nтолько на неактивированные устройства. \nПри наличии брака принимаем устройства ТОЛЬКО в первоначальном виде.",
        reply_markup=keyboard,
    )
    bot.send_message(
        message.chat.id,
        "Выберите одну из наших категорий товаров!",
        reply_markup=keyboard,
    )
    bot.register_next_step_handler(message, proccess_product_category)


def proccess_product_category(message):
    category_name = message.text.split("(", 1)[0].strip()
    try:
        category = Category.objects.get(name=category_name)
        brands = Brand.objects.filter(category=category)

        keyboard = types.ReplyKeyboardMarkup(row_width=1, resize_keyboard=True)

        for brand in brands:
            button = types.KeyboardButton(text=brand.name)
            keyboard.add(button)

        back_button = types.KeyboardButton(text="Назад")
        keyboard.add(back_button)

        bot.send_message(message.chat.id, "Выберите вендора:", reply_markup=keyboard)
        bot.register_next_step_handler(message, proccess_product_brand, category)
    except Category.DoesNotExist:
        bot.send_message(
            message.chat.id,
            "Введите еще раз /catalog и выберите категорию из предложенных! Если вы хотите выйти из выбора категории, то отправьте вашу команду еще раз.",
        )


def proccess_product_brand(message, category):
    brand_name = message.text
    try:
        brands = Brand.objects.filter(category=category, name=brand_name)
        brand = brands.first()
        products = Product.objects.filter(category=category, brand=brand)

        keyboard = types.ReplyKeyboardMarkup(row_width=1, resize_keyboard=True)
        button = types.KeyboardButton(text="Назад")
        keyboard.add(button)

        products_text = ""
        for product in products:
            products_text += f"{product.name} - {product.price}{product.currency}\n\n"

        if products_text:
            bot.send_message(message.chat.id, text=products_text, reply_markup=keyboard)
    except Brand.DoesNotExist:
        bot.send_message(message.chat.id, "Такого вендора нет!")
    except Product.DoesNotExist:
        bot.send_message(
            message.chat.id, "Нет продуктов для выбранной категории и вендора."
        )


@bot.message_handler(func=lambda message: message.text == "Назад")
def go_back(message):
    product_catalog(message)


@bot.message_handler(commands=["about_us"])
def help(message):
    markup = types.ForceReply(selective=False)
    text = "Компания - МАСТЕР GSM ИСТРА. \n\nНОВЫЕ ТОПОВЫЕ ТЕЛЕФОНЫ ПО РАЗУМНЫМ ЦЕНАМ! ДЛЯ ЗАКАЗА ПИШИТЕ СООБЩЕНИЯ В ЛИЧКУ.  \n\nВнимание!!! Гарантия на продукцию Apple 5 ДНЕЙ (проверка заводского брака). Срок гарантии указан с даты покупки телефона. При наличии косметических дефектов гарантия распространяется только на неактивированные устройства. При наличии брака принимаем устройства ТОЛЬКО в первоначальном виде."
    bot.send_message(message.chat.id, text=text, parse_mode="html", reply_markup=markup)


@bot.message_handler(commands=["contacts"])
def help(message):
    markup = types.ForceReply(selective=False)
    photo_path = "./media/photo_tg_bot.jpg"
    bot.send_photo(message.chat.id, open(photo_path, "rb"))
    bot.send_message(
        message.chat.id,
        f"Наш телефон: 89670831183 \n\nАдрес: город Истра , ул. Главного конструктора Адасько, д.7 корпус 2. (Ориентир: рядом аптека Столичка и парикмахерская Цирюльник, в одном офисе с пунктом выдачи Яндекс Маркет и Ювелирным  магазином).",
        parse_mode="html",
        reply_markup=markup,
    )


# ##################################################### ADMIN PART #######################################################################

# Рассылка всем пользователям от лица админа
@bot.message_handler(commands=["send_message"])
def send_message(message):
    user = Admin.objects.filter(UUID=int(message.chat.id)).first()
    if user:
        markup = types.ForceReply(selective=False)
        bot.send_message(
            message.chat.id,
            "Введите текст сообщения, которое хотите отправить:",
            reply_markup=markup,
        )
        bot.register_next_step_handler(message, process_text)
    else:
        bot.send_message(message.chat.id, "Вы не администратор")


def process_text(message):
    text = message.text.strip()
    markup = types.ForceReply(selective=False)
    bot.send_message(
        message.chat.id,
        "Теперь отправьте фотографию для этого сообщения: \nЕсли не хотите то '-'",
        reply_markup=markup,
    )
    bot.register_next_step_handler(message, process_photo, text)


def process_photo(message, text):
    if message.photo:
        photo = message.photo[-1].file_id  # Получаем file_id фотографии
        users = UserBot.objects.all()

        for user in users:
            try:
                bot.send_photo(user.user_id, photo, caption=text)
                News.objects.create(text=text, photo=photo)
            except Exception as e:
                print(f"Произошла ошибка {e}")
        else:
            bot.send_message(message.chat.id, "Рассылка завершена")
    else:
        users = UserBot.objects.all()

        for user in users:
            try:
                bot.send_message(user.user_id, text)
                News.objects.create(
                    text=text,
                )
            except Exception as e:
                print(f"Произошла ошибка {e}")

# Добавление администратора
@bot.message_handler(commands=["admin_add"])
def send_message(message):
    user = Admin.objects.filter(UUID=int(message.chat.id)).first()
    if user:
        markup = types.ForceReply(selective=False)
        bot.send_message(
            message.chat.id,
            "Введите ID аккаунта, нового администратора",
            reply_markup=markup,
        )
        bot.register_next_step_handler(message, process_text_admin)
    else:
        bot.send_message(message.chat.id, "Вы не администратор")


def process_text_admin(message):
    id_admin = message.text.strip()
    markup = types.ForceReply(selective=False)
    try:
        Admin.objects.create(UUID=id_admin)
        bot.send_message(
            message.chat.id,
            "Отлично! Админ добавлен",
            reply_markup=markup,
        )
    except Exception as e:
        bot.send_message(
            message.chat.id,
            "Админ уже создан или ID ошибочный",
            reply_markup=markup,
        )


# Повышение цены товара
@bot.message_handler(commands=["price_up_all"])
def priceUpAll(message):
    markup = types.ForceReply(selective=False)
    bot.send_message(
        message.chat.id,
        "Пришлите процент повышения товара! Пример: 10",
        reply_markup=markup,
    )
    bot.register_next_step_handler(message, proccess_price_up_all)


def proccess_price_up_all(message):
    products = Product.objects.all()
    procent = message.text
    try:
        for product in products:
            product.price += int(product.price) * int(procent) // 100
            product.save()

        bot.send_message(message.chat.id, text="Список обновлен!")
    except Exception as e:
        bot.send_message(message.chat.id, f"Ошибка! Неправильный формат процента.")


# Повышение цен товаров с определенной стоимостью
@bot.message_handler(commands=["price_up_with_price"])
def priceUpWithPrice(message):
    bot.send_message(message.chat.id, "Напишите минимальную сумму! Пример: 4000")
    bot.register_next_step_handler(message, proccess_priceUp_with_price)


def proccess_priceUp_with_price(message):
    min_price = message.text
    try:
        keyboard = types.ReplyKeyboardMarkup(row_width=1, resize_keyboard=True)
        back_button = types.KeyboardButton(text="Вернуться к предыдущему шагу")
        keyboard.add(back_button)

        bot.send_message(
            message.chat.id,
            "Напишите максимальную сумму! Пример: 5000",
            reply_markup=keyboard,
        )
        bot.register_next_step_handler(
            message, proccess_priceUp_with_price_2, min_price
        )
    except Exception:
        bot.send_message(message.chat.id, "Ошибка минимальной суммы!")


def proccess_priceUp_with_price_2(message, min_price):
    max_price = message.text
    try:
        keyboard = types.ReplyKeyboardMarkup(row_width=1, resize_keyboard=True)
        back_button = types.KeyboardButton(text="Вернуться к предыдущему шагу")
        keyboard.add(back_button)

        bot.send_message(
            message.chat.id, "Теперь напишите процент!", reply_markup=keyboard
        )
        bot.register_next_step_handler(
            message, proccess_priceUp_with_price_2_price_up, min_price, max_price
        )
    except Exception:
        bot.send_message(message.chat.id, "Ошибка максимальной суммы!")


def proccess_priceUp_with_price_2_price_up(message, min_price, max_price):
    procent = message.text
    try:
        markup = types.ForceReply(selective=False)
        products = Product.objects.filter(price__gte=min_price, price__lte=max_price)
        for product in products:
            product.price += int(product.price) * int(procent) // 100
            product.save()

        bot.send_message(message.chat.id, text="Список обновлен!", reply_markup=markup)
    except Exception as e:
        bot.send_message(message.chat.id, f"Ошибка! Неправильный формат процента.")


@bot.message_handler(
    func=lambda message: message.text == "Вернуться к предыдущему шагу"
)
def go_back(message):
    priceUpWithPrice(message)


# повышение цен определенных товаров
@bot.message_handler(commands=["price_up"])
def priceUp(message):
    categories = Category.objects.all()

    keyboard = types.ReplyKeyboardMarkup(row_width=1, resize_keyboard=True)

    for category in categories:
        button = types.KeyboardButton(text=category.name)
        keyboard.add(button)

    bot.send_message(
        message.chat.id, "Выберите одну из категорий товаров!", reply_markup=keyboard
    )
    bot.register_next_step_handler(message, proccess_brand)


def proccess_brand(message):
    category_name = message.text
    try:
        category = Category.objects.get(name=category_name)
        brands = Brand.objects.filter(category=category)

        keyboard = types.ReplyKeyboardMarkup(row_width=1, resize_keyboard=True)

        for brand in brands:
            button = types.KeyboardButton(text=brand.name)
            keyboard.add(button)

        back_button = types.KeyboardButton(text="Шаг назад")
        keyboard.add(back_button)

        bot.send_message(
            message.chat.id,
            "Выберите вендора! Если хотите поднять цены на всю категорию то пришлите '-'",
            reply_markup=keyboard,
        )
        bot.register_next_step_handler(message, proccess_price_brand, category)
    except Exception:
        bot.send_message(message.chat.id, "Ошибка выбора вендора!")


def proccess_price_brand(message, category):
    brand_name = message.text
    markup = types.ForceReply(selective=False)
    try:
        if brand_name == "-":
            bot.send_message(message.chat.id, "Отправьте процент:", reply_markup=markup)
            bot.register_next_step_handler(
                message, proccess_procent_only_category, category
            )
        else:
            brand = Brand.objects.get(category=category, name=brand_name)
            products = Product.objects.filter(category=category, brand=brand)
            bot.send_message(message.chat.id, "Отправьте процент:", reply_markup=markup)
            bot.register_next_step_handler(message, proccess_procent_brand, products)
    except Exception:
        bot.send_message(
            message.chat.id, "Нет продуктов для выбранной категории и вендора."
        )


def proccess_procent_only_category(message, category):
    procent = message.text
    try:
        markup = types.ForceReply(selective=False)
        products = Product.objects.filter(category=category)
        for product in products:
            product.price += int(product.price) * int(procent) // 100
            product.save()

        bot.send_message(message.chat.id, text="Список обновлен!", reply_markup=markup)
    except Exception as e:
        bot.send_message(message.chat.id, f"Ошибка! Неправильный формат процента.")


def proccess_procent_brand(message, products):
    procent = message.text
    try:
        markup = types.ForceReply(selective=False)
        for product in products:
            product.price += int(product.price) * int(procent) // 100
            product.save()

        bot.send_message(message.chat.id, text="Список обновлен!", reply_markup=markup)
    except Exception as e:
        bot.send_message(message.chat.id, f"Ошибка! Напишите разработчику {str(e)}")


@bot.message_handler(func=lambda message: message.text == "Шаг назад")
def go_back(message):
    priceUp(message)

# Понижение процент товара
@bot.message_handler(commands=["price_down"])
def priceDown(message):
    categories = Category.objects.all()

    keyboard = types.ReplyKeyboardMarkup(row_width=1, resize_keyboard=True)

    for category in categories:
        button = types.KeyboardButton(text=category.name)
        keyboard.add(button)

    bot.send_message(
        message.chat.id, "Выберите одну из категорий товаров!", reply_markup=keyboard
    )
    bot.register_next_step_handler(message, proccess_brand_down)


def proccess_brand_down(message):
    category_name = message.text
    try:
        category = Category.objects.get(name=category_name)
        brands = Brand.objects.filter(category=category)

        keyboard = types.ReplyKeyboardMarkup(row_width=1, resize_keyboard=True)

        for brand in brands:
            button = types.KeyboardButton(text=brand.name)
            keyboard.add(button)

        back_button = types.KeyboardButton(text="Отмена")
        keyboard.add(back_button)

        bot.send_message(
            message.chat.id,
            "Выберите вендора! Если хотите опустить цены на всю категорию то пришлите '-'",
            reply_markup=keyboard,
        )
        bot.register_next_step_handler(message, proccess_price_brand_down, category)
    except Exception:
        bot.send_message(message.chat.id, "Ошибка выбора вендора!")


def proccess_price_brand_down(message, category):
    brand_name = message.text
    markup = types.ForceReply(selective=False)
    try:
        if brand_name == "-":
            bot.send_message(message.chat.id, "Отправьте процент:", reply_markup=markup)
            bot.register_next_step_handler(
                message, proccess_procent_only_category_down, category
            )
        else:
            brand = Brand.objects.get(category=category, name=brand_name)
            products = Product.objects.filter(category=category, brand=brand)
            bot.send_message(message.chat.id, "Отправьте процент:", reply_markup=markup)
            bot.register_next_step_handler(message, proccess_procent_brand_down, products)
    except Exception:
        bot.send_message(
            message.chat.id, "Нет продуктов для выбранной категории и вендора."
        )


def proccess_procent_only_category_down(message, category):
    procent = message.text
    try:
        markup = types.ForceReply(selective=False)
        products = Product.objects.filter(category=category)
        for product in products:
            product.price -= int(product.price) * int(procent) // 100
            product.save()

        bot.send_message(message.chat.id, text="Список обновлен!", reply_markup=markup)
    except Exception as e:
        bot.send_message(message.chat.id, f"Ошибка! Неправильный формат процента.")


def proccess_procent_brand_down(message, products):
    procent = message.text
    try:
        markup = types.ForceReply(selective=False)
        for product in products:
            product.price -= int(product.price) * int(procent) // 100
            product.save()

        bot.send_message(message.chat.id, text="Список обновлен!", reply_markup=markup)
    except Exception as e:
        bot.send_message(message.chat.id, f"Ошибка! Неправильный формат процента.")


@bot.message_handler(func=lambda message: message.text == "Отмена")
def go_back(message):
    priceDown(message)


# Добавление товара
@bot.message_handler(commands=["product_add"])
def product_add(message):
    user = Admin.objects.filter(UUID=int(message.chat.id)).first()
    if user:
        markup = types.ForceReply(selective=False)
        bot.send_message(
            message.chat.id,
            "Введите название и полное описание товара",
            reply_markup=markup,
        )
        bot.register_next_step_handler(message, process_price)
    else:
        bot.send_message(message.chat.id, "Вы не администратор")


def process_price(message):
    name = message.text.strip()
    markup = types.ForceReply(selective=False)
    bot.send_message(
        message.chat.id,
        "Теперь введите цену товара. Пример: 10000",
        reply_markup=markup,
    )
    bot.register_next_step_handler(message, process_currency, name)


def process_currency(message, name):
    price = message.text.strip()
    markup = types.ForceReply(selective=False)
    bot.send_message(
        message.chat.id,
        "Теперь введите валюту цены (знак). Пример: ₽",
        reply_markup=markup,
    )
    bot.register_next_step_handler(message, process_category, name, price)


def process_category(message, name, price):
    currency = message.text.strip()
    categories = Category.objects.all()

    keyboard = types.ReplyKeyboardMarkup(row_width=1, resize_keyboard=True)

    for category in categories:
        button = types.KeyboardButton(text=category.name)
        keyboard.add(button)

    bot.send_message(
        message.chat.id,
        "Выберите название категории или напишите вручную если хотите создать новую",
        reply_markup=keyboard,
    )
    bot.register_next_step_handler(message, process_brand, name, price, currency)


def process_brand(message, name, price, currency):
    category_name = message.text
    try:
        category = Category.objects.get(name=category_name)
    except Category.DoesNotExist:
        category = None
    if not category:
        category = Category.objects.create(name=category_name)
    brands = Brand.objects.filter(category=category)
    keyboard = types.ReplyKeyboardMarkup(row_width=1, resize_keyboard=True)

    for brand in brands:
        button = types.KeyboardButton(text=brand.name)
        keyboard.add(button)

    bot.send_message(
        message.chat.id,
        "Напишите название производителя, если ее не существует или это новая категория, то она создается автоматически",
        reply_markup=keyboard,
    )
    bot.register_next_step_handler(
        message, process_end, name, price, currency, category
    )


def process_end(message, name, price, currency, category):
    brand_name = message.text
    try:
        brands = Brand.objects.filter(name=brand_name)
        brand = brands.first()
        brand.category.set([category])
    except Brand.DoesNotExist:
        brand = None
    except Exception:
        brand = None
    if not brand:
        brand = Brand.objects.create(name=brand_name)
        brand.category.set([category])
    markup = types.ForceReply(selective=False)
    try:
        Product.objects.create(
            name=name, price=price, currency=currency, category=category, brand=brand
        )

        bot.send_message(
            message.chat.id,
            "Товар создан, проверьте список!",
            reply_markup=markup,
        )
    except Exception as e:
        bot.send_message(
            message.chat.id,
            f"Попробуйте заново, вы где-то ошиблись!",
            reply_markup=markup,
        )


# Ловит любое сообщение
@bot.message_handler()
def info(message):
    if message.text.lower() == "id":
        bot.reply_to(message, f"ID: {message.from_user.id}")
        admin_id = Admin.objects.filter(UUID=message.from_user.id)
        if admin_id:
            bot.reply_to(
                message,
                f"Вы администратор! Вам доступны особенные команды. \n\n/admin_add - Добавление админа\n\n/product_add - Добавление товара \n\n/price_up_with_price - Повышение цены по определенной цене \n\n/price_up - Повышение цены по определенной категории и бренду \n\n/price_up_all - Повышение цены для всех товаров \n\n/price_down - Понижение цены по определенной категории или вендору \n\n/send_message - Рассылка сообщения всем юзерам",
            )
    bot.reply_to(message, f"Лучше закажите у нас!")


def start_bot():
    bot.polling(non_stop=True)


def stop_bot():
    bot.stop_polling()
