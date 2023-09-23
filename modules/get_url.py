from bs4 import BeautifulSoup
import aiohttp

async def get_url(user_id, url, headers):
    async with aiohttp.ClientSession() as session:
        async with session.get(url=url, headers=headers) as response:
            soup = BeautifulSoup(await response.text(), "html.parser")
            with open(f'page_data_{user_id}.json', 'w', encoding="utf-8") as file:
                file.write(str(soup))

if __name__ == '__main__':
    asyncio.run(get_url())
    