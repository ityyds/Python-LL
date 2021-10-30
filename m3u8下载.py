import asyncio
import aiohttp
import aiofiles
import time
import os
from Crypto.Cipher import AES

async def dl(url, name, sem, wjj):
    async with sem:
        async with aiohttp.ClientSession() as session:
            async with await session.get(url) as resp:
                async with aiofiles.open(f"{wjj}/{name}.ts", mode="wb") as f:
                    await f.write(await resp.content.read())
    print(name, "wc")



async def qaq():
    k = []
    wjj = "pictureorvideo/picture/电影"
    if not os.path.exists(wjj): # 判断有没有这个文件夹，如果没有，新建一个文件夹
        os.mkdir(wjj)
        print(wjj+"-完成")
    sem = asyncio.Semaphore(15)

    with open("pictureorvideo/fstttw.m3u8", mode="r", encoding="utf-8") as f:
        for a in f:
            if "#" in a:
                continue
            url = a.strip()
            name = url.split("key=")[-1]
            b = asyncio.create_task(dl(url, name, sem, wjj))
            k.append(b)
        await asyncio.wait(k)


async def aes(name):
    e = "821a4c50abbfdf9a"
    ace = AES.new(key=e.encode(), IV=b"0000000000000000", mode=AES.MODE_CBC)
    async with aiofiles.open(f"pictureorvideo/picture/{name}", mode="rb") as f1:
        bs = await f1.read()
    async with aiofiles.open(f"pictureorvideo/picture/{name}", mode="wb") as f2:
        await f2.write(ace.decrypt(bs))
    print(name, "JMwc")



async def op():
    k = []
    with open("pictureorvideo/fstttw.m3u8", mode="r", encoding="utf-8") as f:
        for a in f:
            if "#" in a:
                continue
            url = a.strip()
            name = url.split("/")[-1]
            b = asyncio.create_task(aes(name))
            k.append(b)
        await asyncio.wait(k)




def hb():
    with open("pictureorvideo/fstttw.m3u8", mode="r", encoding="utf-8") as f:
        for a in f:
            if "#" in a:
                continue
            a = a.strip()
            a = a.split("key=")[-1]
            with open(f"pictureorvideo/picture/电影/{a}.ts", mode="rb") as r:
                bs = r.read()
            with open("pictureorvideo/picture/h.mp4", mode="ab") as k:
                k.write(bs)

if __name__ == '__main__':
    asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())
    # asyncio.run(qaq())
    # asyncio.run(op())
    hb()

