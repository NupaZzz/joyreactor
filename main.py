import requests
from bs4 import BeautifulSoup
from aiogram import Bot, types, Dispatcher, F
from aiogram.enums import ParseMode
from aiogram.filters import CommandStart, Command, CommandObject
from aiogram.types import Message
import asyncio
from config import variables
import json

headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/116.0.0.0 Safari/537.36",
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7"
}

def save_configs(user_configs):
    with open('user_configs.json', 'w') as f:
        json.dump(user_configs, f, indent=4)

def load_configs():
    try:
        with open('user_configs.json', 'r') as f:
            return json.load(f)
    except FileNotFoundError:
        return {}
    
user_configs = load_configs()
dp=Dispatcher()

def get_url():
    response = requests.get(url=variables.url, headers=headers)
    soup = BeautifulSoup(response.text, "html.parser")
    with open('page_data.json', 'w', encoding="utf-8") as file:
        file.write(str(soup))

def get_links():
    with open('page_data.json', 'r', encoding='utf-8') as file:
        data = file.read()
    soup = BeautifulSoup(data, "html.parser")
    href_list = []
    for link_wr in soup.find_all(class_='link_wr'):
        for link in link_wr.find_all('a'):
            href = link.get('href')
            if href not in variables.visited_links:
                variables.visited_links.add(href)
                href_list.append(href)
    return href_list

@dp.message(Command('joy_url'))
async def joy_url_start(message: types.Message):
    user_id = str(message.from_user.id)
    url_type = message.text.split()[1]
    if not url_type:
        await message.answer("Некорректная команда. Укажите URL после /joy_url.")
        return
    if url_type == 'default':
        user_configs[user_id] = variables.url
    elif url_type == 'm':
        user_configs[user_id] = variables.url_m
    elif url_type == 'old':
        user_configs[user_id] = variables.url_old
    else:
        await message.answer("Некорректный URL")
        return
    save_configs(user_configs)
    await message.answer(f"Установлен URL: {user_configs[user_id]}")

@dp.message(Command('joy'))
async def joy_start(message: types.Message):
    user_id = str(message.from_user.id)
    while True:
        get_url()
        links = get_links()
        if links:
            for link in links:
                await message.answer(f"{user_configs[user_id]}{link}")
                await asyncio.sleep(10)
            await asyncio.sleep(10)

async def main():
    bot = Bot(variables.TOKEN, parse_mode=ParseMode.HTML)
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())