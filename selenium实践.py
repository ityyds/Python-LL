
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
#无头浏览器
from selenium.webdriver.chrome.options import Options
opt = Options()
opt.add_argument("--headless")
opt.add_argument("--disable-gpu")


web = webdriver.Chrome(options=opt)
web.get("https://ys.endata.cn/Schedule/Movie")

# web.find_element(By.XPATH, '//*[@id="app"]/div/div[2]/div/ul/div[1]/div[2]/p').click()
# #将selenium定义到最后一个窗口
# web.switch_to.window(web.window_handles[-1])
# print(web.find_element(By.XPATH, '//*[@id="v_upinfo"]/div[2]/div[1]/a[1]').text)
# web.close()
# web.switch_to.window(web.window_handles[0])
# print(web.find_element(By.XPATH, '//*[@id="app"]/div/div[2]/div/ul/div[1]/div[2]/p').text)

b = web.find_element(By.XPATH, '//*[@id="app"]/section/main/div/div[1]/div/section/section[2]/div[2]/section[2]/div[1]/div[4]/div[2]/table/tbody/tr[1]/td[2]')

print(b)










