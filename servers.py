import time
import aiohttp

async def get_server_info_masters():
    url = 'https://api.ip-games.ru/method/server.get?address=185.97.254.214:7744&key=682DNYTNSGGZ6LNQSHIYQXA0DAPBFEYHVKR6YPMD&cache_reset=' + str(int(time.time()))
    async with aiohttp.ClientSession() as session:
        async with session.get(url) as response:
            data = await response.json()
            return data

async def get_server_info_hzd():
    url = 'https://api.ip-games.ru/method/server.get?address=185.97.254.214:7144&key=682DNYTNSGGZ6LNQSHIYQXA0DAPBFEYHVKR6YPMD&cache_reset=' + str(int(time.time()))
    async with aiohttp.ClientSession() as session:
        async with session.get(url) as response:
            data = await response.json()
            return data
        
async def get_server_info_massacre():
    url = 'https://api.ip-games.ru/method/server.get?address=185.97.254.214:7444&key=682DNYTNSGGZ6LNQSHIYQXA0DAPBFEYHVKR6YPMD&cache_reset=' + str(int(time.time()))
    async with aiohttp.ClientSession() as session:
        async with session.get(url) as response:
            data = await response.json()
            return data