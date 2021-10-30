# 源代码提取视频链接下载
"""
import requests
import urllib.parse
import re

headers = {
    "referer": "https://www.douyin.com/",
    "cookie": "cookie: MONITOR_WEB_ID=ad127d3f-4197-45eb-a9fb-11c4e2d790f7; msToken=5lVMnWk_WrZpmZi_yoXkxswxc02BKu5apg5bqjm-712SMdUFy6ksrtEHKJMJjCG11zSHUIp4D-WfaGW15fISOdWjePVM9YuFEAVi-MWQf8B5",
    "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/94.0.4606.81 Safari/537.36"
}

def page(url):
    obj = re.compile(r'type="application/json">(?P<lj>.*?)</script>', re.S)
    obj1 = re.compile(r'{"src":(?P<lj1>.*?)a=', re.S)
    name = re.compile(r'"desc":"(?P<bnc>.*?)",', re.S)
    resp = requests.get(url, headers=headers).text
    resp = obj.search(resp).group("lj")
    resp = urllib.parse.unquote(resp)
    b = name.search(resp).group('bnc')
    resp = obj1.search(resp).group("lj1").replace('"', "http:")
    print(resp, b)
    with open(f"pictureorvideo/{b}.mp4", mode="wb") as f:
        f.write(requests.get(resp, headers=headers).content)



if __name__ == '__main__':
    url = "https://www.douyin.com/video/7019097374651911424"
    page(url)

"""

# 分享链接提取视频下载链接
"""
import requests

ua = {
    "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/94.0.4606.81 Safari/537.36"
}

def GGSMD(url):
    urls = url.split("/")[-2]
    urls = "https://v.douyin.com/" + urls
    resp = requests.get(urls).url
    resp = resp.split("video/")[-1]
    resp = resp.split("?previous")[0]
    return resp

def GG(url):
    url = url.split(":/ ")[-1]
    url = url.split("http")[0]
    return url.strip()

def gg(id, name):
    url = "https://www.iesdouyin.com/web/api/v2/aweme/iteminfo/?item_ids=" + id
    resp = requests.get(url, headers=ua).json()["item_list"][0]['video']['vid']
    urlv = "https://aweme.snssdk.com/aweme/v1/play/?video_id=" + resp + "&ratio=720p&line=0"
    respv = requests.get(urlv, headers=ua)
    with open(f"pictureorvideo/{name}.mp4", mode="wb") as f:
        f.write(respv.content)
    print(name, "下载完成!!")

if __name__ == '__main__':
    url = input('输入分享链接:')
    id = GGSMD(url)
    name = GG(url)
    gg(id, name)
"""

#主页批量下载视频

import requests
import json
import os
import asyncio
import aiohttp
import aiofiles

headers = {
    "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/94.0.4606.81 Safari/537.36"
}

async def down(name, url, dir_file, sem):
    b = url.split("/")[5]
    name = name.replace(":", "")
    if b == 'video':
        async with sem:
            async with aiohttp.ClientSession() as session:
                async with await session.get(url, headers=headers) as f1:
                    async with aiofiles.open(f"{dir_file}/{name}.mp4", 'wb') as f2:
                        await f2.write(await f1.content.read())
    print(name + "-下载完成~")


# 获取主页下所有视频
async def getlist(sec_id, dir_file):
    # 用户id
    sec_uid = sec_id
    # 返回数，最多是34
    count = 34
    # 下一页
    max_cursor = 0
    # 判断是否还有下一页
    has_more = True

    ksk = []

    while has_more:
        #https://www.iesdouyin.com/web/api/v2/aweme/post/?sec_uid=MS4wLjABAAAAZ-GK3PVFTElChwP_F6BmCRqOlgWvKr0tFowzYqJuJ0I&count=34&max_cursor=0&aid=1128&_signature=z1epBAAArxEnjYt5fPWXJs9XqR&dytk=
        url = f"https://www.iesdouyin.com/web/api/v2/aweme/post/?sec_uid={sec_uid}&count={count}&max_cursor={max_cursor}&aid=1128&_signature=z1epBAAArxEnjYt5fPWXJs9XqR&dytk="
        r = requests.get(url, headers=headers)
        r.encoding = 'utf-8'
        da = json.loads(r.text)

        aweme_list = da['aweme_list']
        has_more = da['has_more']

        sem = asyncio.Semaphore(5)
        for i in aweme_list:
            title = i['desc']
            video_url = i['video']['play_addr']['url_list'][0]
            b = asyncio.create_task(down(title, video_url, dir_file, sem))
            ksk.append(b)
        if has_more:
            max_cursor = da['max_cursor']
        else:
            break
    await asyncio.wait(ksk)
    JSQ = len(ksk)
    print(f"总计{JSQ}个视频，已全部下载完毕!")

def hqname(id):
    url = f"https://www.iesdouyin.com/web/api/v2/aweme/post/?sec_uid={id}&count=34&max_cursor=0&aid=1128&_signature=z1epBAAArxEnjYt5fPWXJs9XqR&dytk="
    try:
        resp = requests.get(url, headers=headers).json()
        id = resp['aweme_list'][1]['author']['unique_id']
        if id == "":
            id = resp['aweme_list'][1]['author']['short_id']
        name = resp['aweme_list'][1]['author']['nickname']
        resp = f"{name}-id-{id}"
    except:
        print("出问题了!")
        resp = '新建文件夹'
    return resp


if __name__ == '__main__':
    sec_id = input("shuru:")
    name = hqname(sec_id)
    dir_file = f"pictureorvideo/picture/{name}"                   # 保存地址
    if not os.path.exists(dir_file): # 判断有没有这个文件夹，如果没有，新建一个文件夹
        os.mkdir(dir_file)
        print("\n"+dir_file+"文件夹创建成功""\n")
    asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())
    asyncio.run(getlist(sec_id, dir_file))