import requests
from bs4 import BeautifulSoup
from selenium import webdriver
from urllib.parse import urljoin
from flask import Flask, render_template_string, request
from selenium.webdriver.chrome.options import Options
import os

app = Flask(__name__)

# 首頁：輸入 num
@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        num = request.form.get("num")
        return show_page(num)
    
    # 顯示輸入表單
    return render_template_string("""
    <!DOCTYPE html>
    <html lang="zh-Hant">
    <head>
        <meta charset="UTF-8">
        <title>輸入神奇數字</title>
    </head>
    <body>
        <h1>請輸入神奇數字</h1>
        <form method="POST">
            <input type="text" name="num" required>
            <button type="submit">送出</button>
        </form>
    </body>
    </html>
    """)


def show_page(num):
    # 1. 抓取圖片
    UA = ("Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 "
      "(KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36")
    opts = Options()
    opts.add_argument(f"--user-agent={UA}")
    opts.add_argument("--headless=new")

    driver = webdriver.Chrome(options=opts)
    page_url = f"https://nhentai.net/g/{num}/1/"
    driver.get(page_url)
    html = driver.page_source
    soup = BeautifulSoup(html, 'html.parser')

    # 找頁數
    pagenum = soup.find("span", {"class": "num-pages"}).text.strip()

    # 找圖片
    img = soup.find_all("img")
    img_url = img[1].get("data-src") or img[1].get("src")
    img_url = urljoin(page_url, img_url)

    img_pages_url = []
    base = img_url.rsplit("/", 1)[0]
    ext  = os.path.splitext(img_url)[1]
    img_pages_url = [f"{base}/{i}{ext}" for i in range(1, int(pagenum) + 1)]

    driver.close()

    # 回傳結果頁面
    return render_template_string(f"""
    <!DOCTYPE html>
    <html lang="zh-Hant">
    <head>
        <meta name="viewport" content="width=device-width, initial-scale=1.0" />
        <meta charset="UTF-8">
        <title>封面即時顯示</title>
    </head>
    <style>
        @media screen and (max-width: 600px) {{
            img {{ width: 100%; height: auto; }}
        }}
    </style>
    <body>
        <h1>{num}</h1>
        <img src="{img_url}" alt="Cover" width="350">
        <h2>總共有 {pagenum} 頁</h2>
        {"".join(f'<div><img src="{url}" alt="Page {i+1}" width="350"></div>' for i, url in enumerate(img_pages_url))}
    </body>
    </html>
    """)


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8888, debug=False)
