import pandas as pd
from selenium import webdriver
from selenium.webdriver.common.by import By
import time
from bs4 import BeautifulSoup

# 初始化Selenium的Edge WebDriver
drive = webdriver.Edge()
# 打开瓜子二手车网站首页
url = 'https://www.guazi.com/buy'
drive.get(url)

# 点击选择城市
citys = drive.find_element(By.CLASS_NAME, 'header-city')
citys.click()
# 选择城市为第广州
city = drive.find_element(By.XPATH, '//div[@class="city-hot"]/a[2]')
city.click()

# 选择二手车品牌,根据自己需求选择
carname = drive.find_element(By.XPATH, '//div[@class="tags"]/span[2]')
carname.click()

# 等待页面加载（这里等待3秒，可以根据网速进行调整）
time.sleep(3)
# 定义拿来确定字典的字符
font = drive.find_element(By.XPATH, '//span[@class="gzfont"]').text[0]
font = str(ord(font))
# 定义三个字典
font_dict1 = {
    '57808': '4',
    '58149': '7',
    '58397': '9',
    '58670': '1',
    '58928': '8',
    '59246': '2',
    '59537': '3',
    '59854': '0',
    '60146': '5',
    '60492': '6',
}
font_dict2 = {
    '57808': '6',
    '58149': '9',
    '58397': '1',
    '58670': '2',
    '58928': '3',
    '59246': '5',
    '59537': '8',
    '59854': '0',
    '60146': '7',
    '60492': '4',
}
font_dict3 = {
    '57808': '8',
    '58149': '2',
    '58397': '3',
    '58670': '4',
    '58928': '5',
    '59246': '7',
    '59537': '1',
    '59854': '0',
    '60146': '9',
    '60492': '6',
}
f = '3'  # 字典选择的条件

# 根据选择的条件确定要使用的字典
if font_dict1[font] == f:
    font_dict = font_dict1
elif font_dict2[font] == f:
    font_dict = font_dict2
elif font_dict3[font] == f:
    font_dict = font_dict3

# 创建一个空的DataFrame来存储爬取的数据
data = pd.DataFrame(columns=['车辆型号', '公里数', '车龄（年）', '价格（万元）'])

# 循环爬取多页数据
for i in range(70):
    # 获取当前页面的HTML源代码
    html = drive.page_source
    soup = BeautifulSoup(html, 'html.parser')

    # 使用BeautifulSoup解析页面并提取数据
    divlist = soup.select('div[class="car-card content-item"]')
    for div in divlist:
        car = div.find('h5').text.strip()
        year = div.find('div', class_='card-tags').text.strip().split('年')[0]
        mileage = div.find('span', class_='gzfont').text.strip()

        # 解码公里数中的乱码字符，替换为实际数字
        for char, replacement in font_dict.items():
            mileage = mileage.replace(chr(int(char)), replacement)

        price = div.find('p', class_='price-now').find('span', class_='gzfont').text.strip()

        # 解码价格中的乱码字符，替换为实际数字
        for char, replacement in font_dict.items():
            price = price.replace(chr(int(char)), replacement)

        # 将提取的数据转换为DataFrame对象并连接到data
        row_data = pd.DataFrame(
            [{'车辆型号': car, '公里数': mileage, '车龄（年）': year, '价格（万元）': price}])
        data = pd.concat([data, row_data], ignore_index=True)

    # 点击下一页按钮
    ne = drive.find_element(By.XPATH, '//button[@class="btn-next"]')
    ne.click()
    # 等待2秒，防止程序执行过快
    time.sleep(2)

# 将爬取的数据保存到CSV文件中
data.to_csv('瓜子二手车广州数据.csv', index=False)

# 关闭WebDriver
drive.close()
