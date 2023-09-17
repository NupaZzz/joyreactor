import requests
from bs4 import BeautifulSoup
from aiogram import Bot, types, Dispatcher
from aiogram.enums import ParseMode
from aiogram.filters import CommandStart
from aiogram.types import Message
import asyncio
import json
from config import token

headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/116.0.0.0 Safari/537.36",
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7"
}
url = "https://reactor.cc"
visited_links = set()
dp = Dispatcher()

def get_url():
    response = requests.get(url=url, headers=headers)
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
            if href not in visited_links:
                visited_links.add(href)
                href_list.append(href)
    return href_list

@dp.message(CommandStart())
async def command_start_handler(message: Message):
    while True:
        get_url()
        links = get_links()
        if links:
            for link in links:
                await message.answer(f"{url}{link}")
                await asyncio.sleep(10)
        await asyncio.sleep(10)

async def main():
    bot = Bot(token.TOKEN, parse_mode=ParseMode.HTML)
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())