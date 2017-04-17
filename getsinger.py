import os
import time
import string
from selenium import webdriver

browserPath = 'D:/soft/phantomjs-2.1.1-windows/bin/phantomjs.exe'
homePage = 'http://www.kuwo.cn/geci/artist_{letter}.htm'
parser = 'html5lib'

singerList = []
driver = webdriver.PhantomJS(executable_path=browserPath)  #浏览器的地址

def getPage(page):
    print("[*]Start get page", page)
    driver.get(page)
    print("[*]End get page", page)
    time.sleep(3)

def parseSinger():
    singerEle = driver.find_element_by_class_name('songer_list')
    singerEle = singerEle.find_elements_by_tag_name('a')
    for x in singerEle:
        singer = x.text
        url = x.get_attribute("href")
        print(singer, url)
        singerList.append({'name':singer, 'url':url})

    #检查下一页
    pageEle = driver.find_element_by_id('pageDiv')
    pageEle = pageEle.find_elements_by_tag_name('a')
    for x in pageEle:
        if x.text == '下一页':
            x.click()
            time.sleep(3)
            parseSinger()
            break

if __name__ == '__main__':
    letter = string.ascii_lowercase
    for a in letter:
        #访问目标网页地址
        getPage(homePage.format(letter=a))
        print("[*]OK GET Page", a)
        parseSinger()

    text = ''
    for x in singerList:
        text += '{}\t{}\n'.format(x['name'], x['url'])

    with open('singer.txt', 'w', encoding='utf-8') as f:
        f.write(text)

    driver.close()
