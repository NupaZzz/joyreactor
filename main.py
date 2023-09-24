from aiogram import Bot, types, Dispatcher, F
from aiogram.enums import ParseMode
from aiogram.filters import CommandStart, Command, CommandObject
from aiogram.types import Message
import asyncio
import logging
from variables import variables
from modules import user_configs
from modules.get_links import get_links
from modules.get_url import get_url

dp=Dispatcher()
configs = user_configs.load_configs()
running = {}

@dp.message(CommandStart())
async def joy_info(message: Message):
    await message.answer(f"Добро пожаловать на joyreactor в телеграмме {message.from_user.full_name}."
                         "\nЧтобы начать, вам нужно задать URL в вашем привычном формате, для этого введите /joy_url с выбранным значением: m, old, default. Пример: /joy_url m "
                         "\nЗатем введите команду /joy, чтобы начать сбор данных. В последствии URL можно будет менять на ходу.")

@dp.message(Command('joy_url'))
async def joy_url(message: types.Message):
    user_id = str(message.from_user.id)
    command_parts = message.text.split()
    if len(command_parts) < 2:
        await message.answer("Пожалуйста, введите /joy_url с выбранным значением: m, old, default. Пример: /joy_url m")
        return
    url_type = command_parts[1]
    if not user_id in configs:
        configs[user_id] = {}
    if url_type == 'default':
        configs[user_id]['url'] = variables.url
    elif url_type == 'm':
        configs[user_id]['url'] = variables.url_m
    elif url_type == 'old':
        configs[user_id]['url'] = variables.url_old
    else:
        await message.answer("Некорректный URL")
        return
    user_configs.save_configs(configs)
    await message.answer(f"Установлен URL: {configs[user_id]['url']}")

@dp.message(Command('news_type'))
async def news_type(message: types.Message):
    user_id = str(message.from_user.id)
    command_parts = message.text.split()
    if len(command_parts) < 2:
        await message.answer("Пожалуйста, введите /news_type с выбранным типом новостей. Пример: /news_type best")
        return
    news_type = command_parts[1]
    if not user_id in configs:
        configs[user_id] = {}
    if news_type == 'лучшее' or news_type == 'best':
        configs[user_id]["chapter"] = variables.url_best
    elif news_type == 'хорошее' or news_type == 'good':
        configs[user_id]["chapter"] = variables.url
    elif news_type == 'новое' or news_type == 'new':
        configs[user_id]["chapter"] = variables.url_new
    user_configs.save_configs(configs)
    await message.answer(f"Установлен тип новостей: {configs[user_id]['chapter']}")

@dp.message(Command('joy'))
async def joy_start(message: types.Message):
    user_id = str(message.from_user.id)
    if user_id not in configs and "chapter" not in configs:
        await message.answer("Пожалуйста, выберите URL с помощью комманды /joy_url со следующими из значений: m, old, default. Пример: /joy_url m")
        return
    if 'visible_tags' not in configs[user_id]:
        await message.answer("Пожалуйста, установите видимость тегов с помощью команды /visible_tags.")
        return
    await message.answer ("Парсинг активирован")
    running[user_id] = True
    while running[user_id]:
        await get_url(user_id, configs[user_id]["chapter"], variables.headers)
        links = get_links(user_id)
        if links:
            for link in links:
                if configs[user_id]['visible_tags'] == True:
                    tags = links[link]['tags']
                    await message.answer(f"{tags}\n{configs[user_id]['url']}{link}")
                    await asyncio.sleep(5)
                else:
                    await message.answer(f"{configs[user_id]['url']}{link}")
                    await asyncio.sleep(5)

        await asyncio.sleep(10)
        if not running[user_id]:
            break

@dp.message(Command('stop'))
async def stop_parsing(message: types.Message):
    user_id = str(message.from_user.id)
    if user_id in running:
        running[user_id] = False
        await message.answer("Парсинг остановлен")
    else:
        await message.answer("Парсинг еще не был запущен")

@dp.message(Command('visible_tags'))
async def visible_tags(message: types.Message):
    user_id = str(message.from_user.id)
    if not user_id in configs:
        configs[user_id] = {}   
    configs[user_id]['visible_tags'] = not configs[user_id].get('visible_tags', False)
    user_configs.save_configs(configs)
    if configs[user_id]['visible_tags'] == True:
        await message.reply (f'Теперь вы будете видеть теги.')
    else:
        await message.reply (f'Теперь вы не будете видеть теги.')

async def main():
    bot = Bot(token=variables.TOKEN, parse_mode=ParseMode.HTML)
    await dp.start_polling(bot)

if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    asyncio.run(main())