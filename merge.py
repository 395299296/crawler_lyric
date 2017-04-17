import os
import re

rootdir = 'lyrics/'
singerNum = 0
musicNum = 0
lineNum = 0
lyricsDict = {}
charDict = {}

def checkChinese(text):
    reg = re.compile(r"[\s+]")
    c = reg.sub('',text)
    reg = re.compile(r'[^\u4e00-\u9fa5]')
    if reg.search(c):
        return ''
    return c

def mergeLyrics(dirname):
    global musicNum
    global lineNum
    lyrics = []
    for parent,dirnames,filenames in os.walk(rootdir + dirname):
        for x in filenames:
            musicNum += 1
            try:
                filename = rootdir + dirname + '/' + x
                with open(filename, 'r', encoding='utf-8') as f:
                    text = f.readlines()
                    for y in text:
                        #过滤非中文名歌手
                        ch = checkChinese(y)
                        if not ch: continue
                        if ch in lyricsDict: continue
                        lyricsDict[ch] = True
                        lyrics.append(ch)
                        for c in ch:
                            charDict[c] = True
                        lineNum += 1
            except Exception as e:
                print(filename, str(e))

    return '\n'.join(lyrics)


if __name__ == '__main__':

    lyrics = []
    for parent,dirnames,filenames in os.walk(rootdir):
        singerNum += len(dirnames)
        for x in dirnames:
            text = mergeLyrics(x)
            if not text: continue
            lyrics.append(text)

    print('singer', singerNum)
    print('music', musicNum)
    print('line', lineNum)
    print('word', len(charDict))
    with open('lyrics.txt', 'w', encoding='utf-8') as f:
        f.write('\n'.join(lyrics))
