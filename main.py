from aiogram import Bot, types, Dispatcher, F
from aiogram.enums import ParseMode
from aiogram.filters import CommandStart, Command, CommandObject
from aiogram.types import Message
from bs4 import BeautifulSoup
import json
import asyncio
import aiofiles
import aiohttp
import requests
import logging
from variables import variables
from modules import user_configs

dp=Dispatcher()
visited_links = set()
configs = user_configs.load_configs()

def get_links(user_id):
    with open(f'page_data.json', 'r', encoding='utf-8') as file:
        data = file.read()
    soup = BeautifulSoup(data, "html.parser")
    href_list = []
    for link_wr in soup.find_all(class_='link_wr'):
        for link in link_wr.find_all('a'):
            href = link.get('href')
            if href not in visited_links:
                visited_links.add(href)
                href_list.append(href)
    
    # Загрузка уже сохраненных ссылок
    try:
        with open(f'{user_id}_links.json', 'r', encoding='utf-8') as file:
            saved_links = json.load(file)
    except FileNotFoundError:
        saved_links = []

    # Добавление новых ссылок, если они еще не сохранены
    new_links = [link for link in href_list if link not in saved_links]
    saved_links.extend(new_links)

    # Сохранение обновленного списка ссылок
    with open(f'{user_id}_links.json', 'w', encoding='utf-8') as file:
        json.dump(saved_links, file)

    return new_links

@dp.message(CommandStart())
async def joy_start(message: Message):
    await message.answer(f"Добро пожаловать на joyreactor в телеграмме {message.from_user.full_name}."
                         "\nЧтобы начать, вам нужно задать URL в вашем привычном формате, для этого введите /joy_url с выбранным значением: m, old, default. Пример: /joy_url m "
                         "\nЗатем введите команду /joy, чтобы начать сбор данных. В последствии URL можно будет менять на ходу.")

@dp.message(Command('joy_url'))
async def joy_url_start(message: types.Message):
    user_id = str(message.from_user.id)
    command_parts = message.text.split()
    if len(command_parts) < 2:
        await message.answer("Пожалуйста, введите /joy_url с выбранным значением: m, old, default. Пример: /joy_url m")
        return
    url_type = command_parts[1]
    if url_type == 'default':
        configs[user_id] = variables.url
    elif url_type == 'm':
        configs[user_id] = variables.url_m
    elif url_type == 'old':
        configs[user_id] = variables.url_old
    else:
        await message.answer("Некорректный URL")
        return
    user_configs.save_configs(configs)
    await message.answer(f"Установлен URL: {configs[user_id]}")

@dp.message(Command('news_type'))
async def news_type_start(message: types.Message):
    user_id = str(message.from_user.id)
    command_parts = message.text.split()
    if len(command_parts) < 2:
        await message.answer("Пожалуйста, введите /news_type с выбранным типом новостей. Пример: /news_type best")
        return
    news_type = command_parts[1]
    if news_type == 'лучшее' or news_type == 'best':
        configs["chapter"] = variables.url_best
    elif news_type == 'хорошее' or news_type == 'good':
        configs["chapter"] = variables.url
    elif news_type == 'новое' or news_type == 'new':
        configs["chapter"] = variables.url_new
    user_configs.save_configs(configs)
    await message.answer(f"Установлен тип новостей: {configs['chapter']}")

@dp.message(Command('joy'))
async def joy_start(message: types.Message):
    user_id = str(message.from_user.id)
    if user_id not in configs and "chapter" not in configs:
        await message.answer("Пожалуйста, выберите URL с помощью комманды /joy_url со следующими из значений: m, old, default. Пример: /joy_url m")
        return
    running = True
    def get_url():
        response = requests.get(url=configs["chapter"], headers=variables.headers)
        soup = BeautifulSoup(response.text, "html.parser")
        with open(f'page_data.json', 'w', encoding="utf-8") as file:
            file.write(str(soup))
    while running:
        get_url()
        links = get_links(user_id)
        if links:
            for link in links:
                await message.answer(f"{variables.url}{link}")
                await asyncio.sleep(5)
        await asyncio.sleep(10)
        if not running:
            break

async def main():
    bot = Bot(token=variables.TOKEN, parse_mode=ParseMode.HTML)
    await dp.start_polling(bot)

if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    asyncio.run(main())