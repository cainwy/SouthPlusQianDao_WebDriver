from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
import json
from bs4 import BeautifulSoup
import requests
import time
import os
import asyncio
from telegram import Bot

# 获取系统变量serverKey
serverKey = os.environ.get('serverKey')

botToken=os.environ.get('BOTTOKEN')
chatId=os.environ.get('CHATID')

# 获取 COOKIE 环境变量
cookie_json = os.environ.get('COOKIE')

#print(f"cookie_json type: {type(cookie_json)}")
#print(f"cookie_json: {cookie_json}")
# 获取 COOKIE 环境变量并解析为 JSON 列表


if cookie_json:
    try:
        # 解析 JSON 字符串
        cookie_datas = json.loads(cookie_json)
        #print(f"cookie_data:{cookie_data}")
    except json.JSONDecodeError:
        print("错误：无法解析 COOKIE 环境变量为 JSON。")
else:
    print("错误：COOKIE 环境变量未设置。")

chrome_options = Options()
chrome_options.add_argument("--headless")  # 如果你在无头模式下运行
chrome_options.add_argument("--no-sandbox")  # 解决一些权限问题
chrome_options.add_argument("--disable-dev-shm-usage")  # 解决共享内存问题


service = Service(rf'/usr/local/bin/chromedriver')  # 确保路径正确

def Lingqu(web,i):
    mes=""
    try:
        # 切换到进行中的任务
        web.find_element(By.XPATH, '//*[@id="main"]/table/tbody/tr/td[1]/div[2]/table/tbody/tr[3]/td').click()
        # 点击进行中的任务
        # 完成日常
        time.sleep(2)
        try:
            web.find_element(By.XPATH, '//*[@id="both_15"]/a/img').click()
            print('日常领取成功')
            # 用urlencode编码中文内容
            mes+=f"index {i}:日常领取成功\n"
            messagecontent = '日常领取成功'
            messagecontent = requests.utils.quote(messagecontent)
        except:
            print('日常领取失败')
        try:
            # 尝试点击周常,没有就跳了
            web.find_element(By.XPATH, '//*[@id="both_14"]/a/img').click()
            print('周常领取成功')
            mes+=f"index {i}:周常领取成功\n"
            messagecontent = '周常领取成功'
            messagecontent = requests.utils.quote(messagecontent)
        except:
            pass
    except:
        # 用urlencode编码中文内容
        mes+=f"index {i}:日常领取失败\n"
    finally:
        return mes
mes=""    
for i in cookie_datas:
    url = 'https://www.south-plus.net/plugin.php?H_name-tasks.html.html'
    web = webdriver.Chrome(service=service, options=chrome_options)
    web.get(url)

    time.sleep(1)
    # 将cookies添加到webdriver中
    for cookie in cookie_datas[i]:
        web.add_cookie(cookie)

    # 重新加载页面
    web.get(url)
    time.sleep(3)
    # 领取周常
    soup = BeautifulSoup(web.page_source, 'html.parser')
    weekly_task_1 = soup.find('span', id='p_15')
    weekly_task_2 = soup.find('span', id='p_14')
    print(weekly_task_1, weekly_task_2)

    if weekly_task_1 and weekly_task_2:
        web.find_element(By.XPATH, '//*[@id="p_14"]/a/img').click()
        web.find_element(By.XPATH, '//*[@id="p_15"]/a/img').click()
        print('任务已领取')
        mse+=Lingqu(web,i)

    elif weekly_task_1:
        web.find_element(By.XPATH, '//*[@id="p_15"]/a/img').click()
        mse+=Lingqu(web,i)

    elif weekly_task_2:
        web.find_element(By.XPATH, '//*[@id="p_14"]/a/img').click()
        mse+=Lingqu(web,i)
    else:
        print('任务暂未刷新')

    web.quit()
print(f"mse:{mse}")
import time
from datetime import datetime
title=datetime.fromtimestamp(int(time.time()))
print(f"title:{title}")
async def sendMessage():
    bot = Bot(token=botToken)
    await bot.send_message(chat_id=chatId,text=title+"\n"+mes)
if botToken and chatId:
    asyncio.run(sendMessage())



    
