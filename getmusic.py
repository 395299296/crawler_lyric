import os
import re
import time
from bs4 import BeautifulSoup
from selenium import webdriver

browserPath = 'D:/soft/phantomjs-2.1.1-windows/bin/phantomjs.exe'
outputDir = 'music/'
parser = 'html5lib'

driver = webdriver.PhantomJS(executable_path=browserPath)  #浏览器的地址
driver.set_page_load_timeout(10)  
driver.set_script_timeout(10)

def getPage(page):
    try:
        print("[*]Start get page", page)
        driver.get(page)
        print("[*]End get page", page)
        return True
    except Exception as e:
        print("[*]Error get page", page)
        return False

def parseMusic(singer, musics, index):
    print(singer, "================================", index)
    time.sleep(2)
    songList = driver.find_elements_by_class_name('song')
    result = []
    for x in songList:
        #print(x.text.replace(u'\xa0', u' '))
        try:
            a = x.find_elements_by_tag_name('a')
            if not a: continue
            r = re.compile(r'[\{|\(|（|\-|\[|【|:](.*)' ) #提取歌名
            song = r.sub('',x.text).strip()
            url = a[0].get_attribute("href")
            item = {'name':song, 'url':url}
            if item in musics: continue
            result.append(item)
            #print(song, url)
        except Exception as e:
            print(str(e))
            continue
    if len(result) == 0: return

    musics.extend(result)
    try:
        pageDiv = driver.find_element_by_id('pageDiv')
        pageList = pageDiv.find_elements_by_tag_name('a')
        for x in pageList:
            if x.text == '下一页':
                x.click()
                parseMusic(singer, musics, index + 1)
                break
    except Exception as e:
        pass

def writeMusic(singer, musics):
    text = ''
    if not musics:
        print("Error, no musics", singer)
        return
    for x in musics:
        text += '{}\t{}\n'.format(x['name'], x['url'])
    with open(singer, 'w', encoding='utf-8') as file:
        file.write(text)

if __name__ == '__main__':
    if not os.path.exists(outputDir):
        os.makedirs(outputDir)
    with open('singer.txt', encoding='utf-8') as f:
        data = f.readlines()
        for x in data:
            singer = x.split('\t')
            r = re.compile(r'[^\u4e00-\u9fa5]')
            if r.search(singer[0]): continue #过滤非中文名歌手
            out_file = '%s/%s.txt' % (outputDir, singer[0])
            if os.path.exists(out_file): continue
            if not getPage(singer[1]): continue
            musics = []
            index = 1
            parseMusic(singer[0], musics, index)
            writeMusic(out_file, musics)
    