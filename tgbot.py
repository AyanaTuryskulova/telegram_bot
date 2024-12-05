import os  # Добавлен импорт модуля os
import django
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes
from asgiref.sync import sync_to_async
import logging
import sys


sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..')))


os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'mybot.settings')

import django
django.setup()

from bot.models import Product


logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    await update.message.reply_text("Добро пожаловать! Вы можете использовать команду /products для просмотра продуктов или /add для добавления.")


async def list_products(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    try:

        products = await sync_to_async(list)(Product.objects.all())
        if products:
            response = "\n".join([f"{product.id}. {product.name} - {product.price}₸" for product in products])
        else:
            response = "Продукты отсутствуют."
        await update.message.reply_text(response)
    except Exception as e:
        logging.error(f"Ошибка при получении списка продуктов: {str(e)}")
        await update.message.reply_text("Произошла ошибка при получении списка продуктов.")


async def add_product(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    try:
        args = context.args
        if len(args) != 2:
            await update.message.reply_text("Используйте: /add <название> <цена>")
            return

        name, price = args
    
        product = await sync_to_async(Product.objects.create)(name=name, price=float(price))
        await update.message.reply_text(f"Продукт {product.name} добавлен с ценой {product.price}₽.")
    except Exception as e:
        logging.error(f"Ошибка при добавлении продукта: {str(e)}")
        await update.message.reply_text(f"Ошибка: {str(e)}")


def main():
    application = ApplicationBuilder().token("7440502249:AAHctuylGa8FbJHhZ7AoxtQrfJTaAs65e5I").build()


    application.add_handler(CommandHandler("start", start))
    application.add_handler(CommandHandler("products", list_products))
    application.add_handler(CommandHandler("add", add_product))


    application.run_polling()

if __name__ == '__main__':
    main()
