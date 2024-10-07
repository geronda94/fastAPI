import datetime
from enum import Enum
import time
from aiogram import Bot, Dispatcher, F, types
from aiogram.filters import Filter, Command, CommandStart
import asyncio
import logging #импортируем библиотеку логирования
from aiogram.types import BotCommand, BotCommandScopeChat, BotCommandScopeDefault #Узнать про скопы

from aiogram.types import Message

from apscheduler.schedulers.asyncio import AsyncIOScheduler
from apscheduler.triggers.interval import IntervalTrigger

from aiogram.client.default import DefaultBotProperties
from aiogram.enums import ParseMode
from config import TG_TOKEN
from database import get_async_session
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import text, update
from sqlalchemy.future import select

import time
from orders.schemas import OrderRead, SiteRead, SiteCreate, OrderStatus, TelegramNotification
from orders.models import Order, Site

from aiogram.fsm.state import StatesGroup, State
from aiogram.fsm.context import FSMContext
from aiogram.filters import StateFilter 
#Блок инициализации#############################

TOKEN = TG_TOKEN
SUPER_ADMIN = '6857394634'

################################################


dp = Dispatcher()


# Состояния FSM для добавления сайта
class AddSite(StatesGroup):
    add_site = State()
    add_owner_id = State()
    add_owner_email = State()  # Добавляем новое состояние для email
    add_description = State()
    add_category = State()


# Функция для проверки наличия сайта в базе данных
async def check_site_exists(session: AsyncSession, site_name: str) -> bool:
    # Запрос к базе данных
    result = await session.execute(
        select(Site).filter_by(site_name=site_name)
    )
    return result.scalar() is not None


@dp.message(Command("new_domain"))
async def start_adding_site(message: Message, state: FSMContext):
    await message.answer("Введите название сайта:")
    await state.set_state(AddSite.add_site)


@dp.message(AddSite.add_site)
async def check_site_name(message: Message, state: FSMContext):
    site_name = message.text

    # Получаем сессию
    session_generator = get_async_session()
    session = await anext(session_generator)

    # Проверяем наличие сайта с таким именем
    exists = await check_site_exists(session, site_name)

    if exists:
        await message.answer(f"Сайт с именем {site_name} уже существует.")
        await state.clear()
    else:
        await state.update_data(site_name=site_name)
        await message.answer("Введите Telegram ID владельца:")
        await state.set_state(AddSite.add_owner_id)


@dp.message(AddSite.add_owner_id)
async def get_owner_id(message: Message, state: FSMContext):
    owner_id = message.text
    await state.update_data(owner_id=owner_id)
    await message.answer("Введите email владельца:")
    await state.set_state(AddSite.add_owner_email)  # Переходим к новому состоянию


@dp.message(AddSite.add_owner_email)
async def get_owner_email(message: Message, state: FSMContext):
    owner_email = message.text
    await state.update_data(owner_email=owner_email)  # Сохраняем email
    await message.answer("Введите описание сайта:")
    await state.set_state(AddSite.add_description)


@dp.message(AddSite.add_description)
async def get_description(message: Message, state: FSMContext):
    description = message.text
    await state.update_data(description=description)
    await message.answer("Введите категорию сайта:")
    await state.set_state(AddSite.add_category)


@dp.message(AddSite.add_category)
async def get_category(message: Message, state: FSMContext):
    category = message.text
    user_data = await state.get_data()

    site_name = user_data['site_name']
    owner_id = user_data['owner_id']
    owner_email = user_data['owner_email']  # Получаем email
    description = user_data['description']

    # Получаем сессию
    session_generator = get_async_session()
    session = await anext(session_generator)

    # Создаем новый объект Site
    new_site = Site(
        site_name=site_name,
        owner_telegram=owner_id,  # Убедитесь, что вы добавили это поле в предыдущие шаги
        owner_email=owner_email,  # Добавляем email владельца
        site_description=description,
        site_category=category
    )

    try:
        # Добавляем новый сайт в базу данных
        session.add(new_site)
        await session.commit()  # Подтверждаем изменения

        # Уведомляем пользователя об успешном добавлении
        await message.answer(f"Сайт добавлен!\n\n"
                             f"Название: {site_name}\n"
                             f"ID Владельца: {owner_id}\n"
                             f"Email Владельца: {owner_email}\n"  # Уведомляем email
                             f"Описание: {description}\n"
                             f"Категория: {category}")

    except Exception as e:
        await session.rollback()  # Откат изменений в случае ошибки
        await message.answer("Произошла ошибка при добавлении сайта. Пожалуйста, попробуйте еще раз.")
        print(f"Ошибка при добавлении сайта: {e}")  # Выводим ошибку в консоль для отладки

    finally:
        await session.close()  # Закрываем сессию

    await state.clear()







# Глобальная переменная для кэширования данных о сайтах
cached_sites = {}


async def cache_sites(session: AsyncSession):
    result = await session.execute(select(Site))
    sites = result.scalars().all()
    return {site.site_name: site for site in sites}  # Возвращаем кэш как словарь

        
async def update_cache():
    async for session in get_async_session():  # Используем асинхронный цикл для получения сессии
        global cached_sites
        cached_sites = await cache_sites(session)  # Обновляем кэш
        break  # Прерываем цикл после получения первой сессии

        
        

async def check_orders(bot: Bot):
    async for session in get_async_session():  # Используем асинхронный цикл для получения сессии
        try:
            # Кэшируем данные о сайтах
            await update_cache()
            # Извлекаем заказы со статусом "waiting"
            result = await session.execute(select(Order).where(Order.telegram_notification == TelegramNotification.waiting))
            orders = result.scalars().all()  # Извлекаем все заказы через схему

            # Обрабатываем заказы
            for order in orders:
                site_name = order.site_name  # Получаем имя сайта из заказа
                if site_name in cached_sites:
                    site = cached_sites[site_name]
                    owner_telegram_id = site.owner_telegram.strip()  # Удаляем лишние пробелы

                    # Проверяем, есть ли Telegram ID
                    if owner_telegram_id:
                        try:
                            # Создаем экземпляр OrderRead на основе заказа
                            order_data = OrderRead.model_validate(order)  # Используйте model_validate вместо from_orm
                            # Получаем сообщение через метод format_message
                            message = order_data.format_message()
                            # Отправляем сообщение владельцу сайта
                            await bot.send_message(owner_telegram_id, message)
                            
                            # Обновляем статус уведомления в заказе
                            stmt = update(Order).where(Order.id == order.id).values(telegram_notification=TelegramNotification.delivered)
                            await session.execute(stmt)
                        except Exception as send_ex:
                            # Если не удалось отправить сообщение, обновляем статус на ошибку
                            stmt = update(Order).where(Order.id == order.id).values(telegram_notification=TelegramNotification.delivered)
                            await session.execute(stmt)
                            await bot.send_message(SUPER_ADMIN, text=f'Не удалось отправить сообщение владельцу {owner_telegram_id}: {send_ex}')
                    else:
                        # Если ID отсутствует, обновляем статус заказа
                        stmt = update(Order).where(Order.id == order.id).values(telegram_notification=TelegramNotification.delivered)
                        await session.execute(stmt)
            # Не забудьте закоммитить изменения в базе данных
            await session.commit()
        except Exception as ex:
            await bot.send_message(SUPER_ADMIN, text='Ошибка отправки заказа')
            await bot.send_message(SUPER_ADMIN, text=str(ex))
        finally:
            await session.close()  # Закрываем сессию





async def set_admin_commands(bot: Bot):
    commands = [
        BotCommand(command='/new_domain', description='Добавить домен'),
        BotCommand(command='/start', description='Мой ID')
    ]
    
    # Устанавливаем команды только для администраторов чата
    await bot.set_my_commands(commands, scope=BotCommandScopeChat(chat_id=SUPER_ADMIN))


async def set_commands(bot: Bot):
    commands = [
        BotCommand(command='/start', description='Мой ID'),
    ]
    
    await bot.set_my_commands(commands, scope=BotCommandScopeDefault())
    
    
    
@dp.message(CommandStart,  StateFilter("*"))   
async def start_command(message: Message, state: FSMContext):
    # Проверяем, есть ли активное состояние
    current_state = await state.get_state()

    if current_state:
        # Если состояние есть, сбрасываем его
        await state.clear()
        await message.answer("Ваше состояние было сброшено.")

    # Отправляем пользователю его ID
    await message.answer(f"Ваш ID: {message.from_user.id}")



async def start_bot(bot: Bot, state: FSMContext = None):
    # Установка команд для администратора и пользователей
    await set_admin_commands(bot)
    await set_commands(bot)


    # Отправляем сообщение супер-администратору о запуске бота
    await bot.send_message(SUPER_ADMIN, text='Бот запущен!')
    

   
    
    
async def stop_bot(bot: Bot):
    await bot.send_message(SUPER_ADMIN, text='<s>Бот остановлен</s>')
    
    

#Тело бота#####################################
async def start():
    #logging.basicConfig(level=logging.INFO, format="%(asctime)s - [%(levelname)s] - %(name)s -(%(filename)s).%(funcName)s(%(lineno)d) - %(message)s")

    bot = Bot(token=TOKEN, default=DefaultBotProperties(parse_mode=ParseMode.HTML))
    dp.startup.register(start_bot) #Регистрируем хэндлер срабатывающий при запуске
    dp.shutdown.register(stop_bot)

    scheduler = AsyncIOScheduler()
    scheduler.add_job(update_cache, 'interval', seconds=120) 
    scheduler.add_job(check_orders, 'interval', seconds=4, args=(bot,))
    # scheduler.add_job(post_post, 'interval', seconds=60*60*12, args=(Message,))



    try:
        #Начало сессии
        scheduler.start()        
        await dp.start_polling(bot)
    finally:
        #Закрываем сессию
        await bot.session.close()
        



#Запускаем функцию Бота########################
if __name__ =="__main__":
    asyncio.run(start())

