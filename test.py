import re

c = '守候在凌晨2:00 的伤心 - Show Bar\n2002年的第一场雪'
print(c)
reg = re.compile(r"[\s+]")
c = reg.sub(' ',c)
c = c.strip()
print(c)
reg = re.compile(r"[^\u4e00-\u9fa5\s]")
c = reg.sub('',c)
print(c)
w = list(set(c))
print(w)
w.sort()
print(w)
char2id_dict = {w: i for i, w in enumerate(w)}
id2char_dict = {i: w for i, w in enumerate(w)}
print(char2id_dict)
print(id2char_dict)