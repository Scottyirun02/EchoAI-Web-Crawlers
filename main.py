# This is a sample Python script.
import time
# Press Shift+F10 to execute it or replace it with your code.
# Press Double Shift to search everywhere for classes, files, tool windows, actions, and settings.

# -*- coding: utf-8 -*-
# @Author : CLD
# @File : download_pic.py

import urllib.request


import urllib


import bs4
import re
import os
import csv


# 由链接获取该网页的详细信息
def get_html(url):
    content = urllib.request.urlopen(url).read()
    soup = bs4.BeautifulSoup(content, "html.parser")
    return soup


# 获取目录页中每个图片的链接
def get_link(soup):
    memory = ""

    links = soup.findAll("a")
    for link in links:
        href = link.get('href')
        if href is None:
            continue
        elif href[:26] == ("photogallery.php?album=" + str(html_num)) and str(href) != memory:
            memory = str(href)
            pic_link = "https://marinespecies.org/{}".format(str(href))
            pic_html = get_html(pic_link)
            get_picture(pic_html)


# 获取图片
def get_picture(soup):
    global num
    title = "Error"
    label_link = ""
    # 获取分类信息所在网页的链接
    for link in soup.select("span.photogallery_caption.photogallery_aphia_row"):
        title = link.get_text()
        title = title.replace(u'\xa0', '')
        for a in link.select('a'):
            path = a.get('href')
            label_link = "https:" + path

    pics = soup.findAll("img")
    pic = pics[7]
    src = pic['src']

    if src[:14] == 'https://images' and src[-3:] != 'png' and label_link != "":
        pic_path = folder_path + str(num) + '.jpg'
        # 下载图片
        urllib.request.urlretrieve(src, pic_path)
        # 存储label
        get_label(label_link, src, title)
        print("第%s张图片下载完毕" % num)
        num += 1


# 获取每张图片的label，存储在csv文件中
def get_label(path, path_pic, title):
    pic_html = get_html(path)
    class_dic = {}
    dic = {"pic_name": str(num) + ".jpg", "html": path, "html_pic": path_pic, "WoRMS taxa": title}
    for link in pic_html.select("#Classification"):
        labels = str(link.get_text())
        labels = labels.replace(u'\xa0', '').strip('\n')
        label_lists = labels.split('\n')
        label_lists.remove("Biota")
        print(label_lists)
        for lab in label_lists:
            key = re.findall(r'[(](.*?)[)]', lab)
            val = lab.replace('(' + key[-1] + ')', '')
            class_dic[key[-1]] = val
        dic["classification"] = class_dic

    with open(csv_path, 'a', newline='', encoding='utf-8') as file:
        dic_w = csv.DictWriter(file, row_names)
        dic_w.writerow(dic)
    # print(dic)


if __name__ == "__main__":
    # num变量是爬取图片的命名，如果爬取中断需重新爬取要对应修改
    num = 0
    # 该数字是指网页中唯一要修改的数字，观察可得每一大类的目录页不同之处就是这个数字
    html_num = 763
    ## 694 第3675张图片下载完毕

    # 图片将会保存在此处的文件夹，注意使用绝对路径
    folder_path = 'C:/Users/Lenovo/PycharmProjects/pythonProject2/'
    assert os.path.exists(folder_path), "dataset root: {} does not exist.".format(folder_path)

    row_names = ['pic_name', 'html', "html_pic", 'WoRMS taxa', 'classification']
    csv_path = folder_path + 'label763.csv'
    # 判断是否存在label.csv文件(无需自己创建)
    # 不存在的话生成一个带列名的空白文件
    if os.path.exists(csv_path) is False:
        with open(csv_path, 'w', newline='') as f:
            writer = csv.DictWriter(f, row_names)
            writer.writeheader()

    # 每次爬取注意总共多少页，在这里修改就好啦
    for i in range(1, 6):
        page_path = "https://marinespecies.org/photogallery.php?p=show&album={}&pg={}".format(html_num, i)
        page_html = get_html(page_path)
        get_link(page_html)  # 从网页源代码中分析下载保存图片
        print("第%s页图片下载完成" % i)
        print('***' * 10)


    print('一共下载图片：' + str(num) + '张')
    print('done')

