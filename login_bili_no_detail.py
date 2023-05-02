import os
from datetime import datetime
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import StaleElementReferenceException, TimeoutException
from bs4 import BeautifulSoup
import csv
import time

def login_bili(search_keyword):
    chrome_options = Options()
    chrome_options.add_argument("--incognito")
    driver = webdriver.Chrome(options=chrome_options)
    driver.get("https://www.bilibili.com")

    input("请在浏览器中登录B站账号，登录完成后按下回车键以继续...")
    
    search_box = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.XPATH, '//input[@class="nav-search-input"]'))
    )
    search_box.send_keys(search_keyword)

    suggestions = WebDriverWait(driver, 10).until(
        EC.presence_of_all_elements_located((By.XPATH, '//div[@class="suggest-item"]'))
    )

    suggestions_text = []
    for suggestion in suggestions:
        while True:
            try:
                suggestions_text.append(suggestion.text)
                break
            except StaleElementReferenceException:
                continue

    output_dir = 'output/search_suggestions'
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

    filename = f'suggestion_{datetime.now().strftime("%Y%m%d_%H%M%S")}.csv'
    file_path = os.path.join(output_dir, filename)

    with open(file_path, 'w', newline='', encoding='utf-8') as csvfile:
        writer = csv.writer(csvfile)
        for suggestion in suggestions_text:
            writer.writerow([suggestion])

    click_search = WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable((By.XPATH, '//div[@class="nav-search-btn"]'))
    )
    click_search.click()

    # 循环以历遍所有页面
    page_number =1 
    while True:
        time.sleep(5) # 等待页面加载完成, 可根据实际情况调整等待时间或者优化为 WebDriverWait(driver, 30).until(形式
        # 获取所有窗口的句柄
        window_handles = driver.window_handles

        # 切换到新打开的标签页
        driver.switch_to.window(window_handles[-1])

        # 获取页面的HTML内容
        html_content = driver.page_source

        # 使用BeautifulSoup解析HTML
        soup = BeautifulSoup(html_content, "html.parser")

        # 提取所有img标签
        img_tags = soup.find_all("img")[4:]

        # 创建 output/title 目录
        output_dir = 'output/title'
        if not os.path.exists(output_dir):
            os.makedirs(output_dir)

        # 在 output/title 目录下创建 page00n.csv 的文件 n 为页码
        file_path = os.path.join(output_dir, f'page{page_number:03d}.csv')

        # 将 alt 属性值写入 CSV 文件
        with open(file_path, 'w', newline='', encoding='utf-8') as csvfile:
            writer = csv.writer(csvfile)
            for img in img_tags:
                alt_value = img.get("alt", "")
                writer.writerow([alt_value])

        # 点击下一页
        try:
            next_page = WebDriverWait(driver, 20).until(
                EC.element_to_be_clickable((By.XPATH, '//button[contains(text(), "下一页")]'))
            )
            next_page.click()
            print(f"已读取完第 {page_number} 页")

            # 等待页面加载完成
            WebDriverWait(driver, 20).until(
                EC.presence_of_all_elements_located((By.TAG_NAME, 'img'))
            )
        except TimeoutException:
            print("已经到达最后一页")
            break

        
        page_number += 1

    input("按下回车键以退出...")
    driver.quit()