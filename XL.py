import aiohttp
import asyncio

ua = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/95.0.4638.54 Safari/537.36"
}

async def main():
   async with aiohttp.ClientSession() as session:
       async with session.get('https://www.tadu.com/book/844240/96191693/', headers=ua) as response:
           print(await response.text())


if __name__ == '__main__':
   asyncio.get_event_loop().run_until_complete(main())







