from os.path import split
from time import sleep

from bs4 import BeautifulSoup
import requests
from lxml.html.diff import html_escape
from Config import config


def gettext(Link):
    resp = requests.get(Link, headers=config.headers, cookies=config.cookie, proxies=config.proxy)
    return resp.text

def getcontent(Link):
    resp = requests.get(Link, headers=config.headers, cookies=config.cookie, proxies=config.proxy)
    return resp.content

def no_cost(RespFlie="resp.txt"):
    f = open(RespFlie, "r", encoding="utf-8")
    html_content = f.read()
    pre = BeautifulSoup(html_content, 'lxml')
    
    # 获取所有分页链接
    page_links = []
    page_nav = pre.find('table', class_='ptt')
    if page_nav:
        for link in page_nav.find_all('a'):
            href = link.get('href')
            if href and "?p=" in href:  # 分页链接特征
                page_links.append(href)
    
    # 处理当前页和所有分页
    all_linklist = []
    processed_pages = set()  # 避免重复处理
    
    def process_page(url):
        if url in processed_pages:
            return
        processed_pages.add(url)
        
        # 获取分页内容
        resp_text = gettext(url)
        page_soup = BeautifulSoup(resp_text, 'lxml')
        div = page_soup.find('div', id="gdt")
        if not div:
            return
        
        # 提取图片链接（原有逻辑）
        step1 = BeautifulSoup(str(div), "lxml")
        step1text = step1.find_all("a")
        linklist = [text.get('href') for text in step1text]
        all_linklist.extend(linklist)
        
    # 处理第一页（原始URL）
    original_url = pre.find('link', rel='canonical').get('href')
    process_page(original_url)
    
    # 处理其他分页
    for link in page_links:
        process_page(link)
    
    # 后续下载逻辑（原有代码，略作调整）
    imglinklist = []
    namelist = []
    for link in all_linklist:
        resp = gettext(link)
        step2 = BeautifulSoup(str(resp), "lxml")
        step2text = step2.find_all("div", id="i3")
        for imghtml in step2text:
            step3 = BeautifulSoup(str(imghtml), "lxml")
            step3text = step3.find_all("img")
            for imglink in step3text:
                img = imglink.get("src") or imglink.get("data-src")  # 兼容性处理
                if img:
                    imglinklist.append(img)
    
    # 下载图片（原有逻辑）
    for img in imglinklist:
        imgsplited = img.split('/')
        filename = imgsplited[-1].split('?')[0]  # 更安全的文件名提取
        namelist.append(filename)
        f = open(filename, "wb")
        f.write(getcontent(img))
        f.close()
        print("file:%s OK!" % filename)
        sleep(3)
    
    f.close()
    return namelist
