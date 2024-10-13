import asyncio
import aiohttp
from time import time
import ssl
import certifi
import requests
import logging

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s [%(levelname)s] %(message)s',
    datefmt='%Y-%m-%d %H:%M:%S'
)

url_list = [
            'https://www.python.org/', 'https://www.wikipedia.org/', 'https://www.github.com/',
            'https://www.stackoverflow.com/', 'https://www.example.com/', 'https://www.reddit.com/',
            'https://www.medium.com/', 'https://www.bbc.com/', 'https://www.cnn.com/'
            ]
def timer(func) :
    def wrapper(*args, **kwargs):
        t0 = time()
        func(*args, **kwargs)
        res = time() - t0
        print(f'\nTime: {round(res, 2)}\n')
        return res
    return wrapper

def get_data(urls): # synchronous function
    for url in urls:
        response = requests.get(url)
        logging.info(f'Downloaded from {response.url}')

async def fetch_data(session, url):
    try:
        async with session.get(url) as response:
            response.raise_for_status()
            content = await response.text()
            logging.info(f"Загружено содержимое с {url}")
            return content
    except Exception as e:
        logging.error(f"Ошибка при загрузке {url}: {e}")
        return None

async def main(urls):
    ssl_context = ssl.create_default_context(cafile=certifi.where())
    async with aiohttp.ClientSession(connector=aiohttp.TCPConnector(ssl=ssl_context)) as session:
        tasks = []
        for url in urls:
            task = asyncio.create_task(fetch_data(session, url))
            tasks.append(task)
        contents = await asyncio.gather(*tasks)
    return contents

@timer
def goer_1():
    asyncio.run(main(url_list))

@timer
def goer_2():
    get_data(url_list)

if __name__ == '__main__':
    g1 = goer_1()
    g2 = goer_2()
    if g2 >= g1:
        print(f'Asynchronous code faster than non-asynchronous on {g2 - g1}')
    else:
        logging.info('Asynchronous coding is unusefull :)')

