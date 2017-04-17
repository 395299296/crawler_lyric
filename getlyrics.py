import os
import io
import sys
import re
import time
import requests
from lxml import etree

inputDir = 'music/'
outputDir = 'lyrics/'
parser = 'html5lib'

def getSinger(file):
    singer = os.path.splitext(file)[0]
    print(singer, "================================")
    if not os.path.exists(outputDir + singer):
        os.makedirs(outputDir + singer)
    with open(inputDir + file, encoding='utf-8') as f:
        data = f.readlines()
        for x in data:
            music = x.split('\t')
            r = re.compile(r'[^\u4e00-\u9fa5]')
            if r.search(music[0]): continue #过滤非中文名歌曲
            out_file = '%s/%s/%s.txt' % (outputDir, singer, music[0])
            if os.path.exists(out_file): continue
            lyrics = parseLyrics(music[1])
            writeLyrics(out_file, lyrics)

def parseLyrics(url):
    print("[*]Start get page", url)
    time.sleep(0.05)
    try:
        r = requests.get(url)
        r.encoding = 'utf-8'
        text = r.text.replace('<br>', '')
        tree = etree.HTML(text)
        content = tree.xpath("//div[@id='lrc_yes']")        
    except Exception as e:
        print(str(e))
        return ''
    
    if not content:
        return ''

    print("[*]End get page", url)
    return content[0].text

def writeLyrics(out_file, lyrics):
    with open(out_file, 'w', encoding='utf-8') as file:
        file.write(lyrics)

if __name__ == '__main__':
    if not os.path.exists(outputDir):
        os.makedirs(outputDir)
    for parent,dirnames,filenames in os.walk(inputDir):
        for x in filenames:
            getSinger(x)
    