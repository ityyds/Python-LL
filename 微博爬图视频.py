import requests
import asyncio
import aiohttp
import aiofiles
import os
import time

def pictureslinking(uid, cookies, zlst):
    pages = 1
    lst = [1]
    ua = {
        "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/95.0.4638.54 Safari/537.36",
        "cookie": cookies}
    f = requests.get(f"https://weibo.com/ajax/profile/info?uid={uid}", headers=ua).json()
    wjm = f"{f['data']['user']['screen_name']}-id-{f['data']['user']['idstr']}"
    folder = f"pictureorvideo/wb/{wjm}"
    if not os.path.exists(folder):
        os.mkdir(folder)
        print("\n" + folder + "文件夹创建成功""\n")
    for pages in lst:
        url = f"https://weibo.com/ajax/statuses/mymblog?uid={uid}&page={pages}&feature=0"
        resp = requests.get(url, headers=ua)
        if not resp:
            break
        resp = resp.json()['data']['list']
        for a in resp:
            if uid != str(a['user']['id']):
                continue
            if "pic_infos" in a and "url_struct" not in a:
                for b in a['pic_infos']:
                    print(a['pic_infos'][b]['mw2000']['url'])
                    zlst.append(a['pic_infos'][b]['mw2000']['url'])
        pages += 1
        lst.append(pages)
    return folder


async def xiaozai1(url, sem, luj):
    name = url.split("/")[-1]
    async with sem:
        async with aiohttp.ClientSession() as resp:
            async with await resp.get(url) as f1:
                async with aiofiles.open(f"{luj}/{name}", mode="wb") as f2:
                    await asyncio.sleep(1)
                    await f2.write(await f1.content.read())
    print(name, "下载完成!")

async def xiazai(lst, folders):
    lsts = []
    sem = asyncio.Semaphore(5)
    for a in lst:
        b = asyncio.create_task(xiaozai1(a, sem, folders))
        lsts.append(b)
    await asyncio.wait(lsts)


if __name__ == '__main__':
    uid = "2120256690"
    cookie = "SUB=_2AkMW1gewf8NxqwJRmP4Ry2jiaIV1zg3EieKgivZrJRMxHRl-yT9jqkMbtRB6PVYpXxViPAKYIp7tQ2kXQu-D45zWa8QM; SUBP=0033WrSXqPxfM72-Ws9jqgMF55529P9D9WWBieFl77uOxGxjXK8ebI2T; XSRF-TOKEN=bhmK3KUPv0xHKFM4IIVMkJaf; WBPSESS=kErNolfXeoisUDB3d9TFHwWcGQv4gOvHeT59kGhOdbhDsk2XmKshS3kZ8B1tdTj_WXzT9ZZMXEXZ3e0P92KZ74fzdJTE4danQrbSigMb1yuN_hkg7YO-s-BsNhJlx74_6EUbshjoGimjMEIop9gmQrc6hEtGWi0o3nHKtuzYF5s="
    zlst = []
    folder = pictureslinking(uid, cookie, zlst)
    # asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())
    # asyncio.run(xiazai(zlst, folder))
