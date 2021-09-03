# -*- coding: utf-8 -*-
# @Time    : 2021/6/24 21:12
# @Author  : HUII
# @FileName: rc4.py
# @Software: PyCharm
def rc4(data, key):
    x = 0
    box = list(range(256))
    for i in range(256):
        x = (x + box[i] + ord(key[i % len(key)])) % 256
        box[i], box[x] = box[x], box[i]
    x = 0
    y = 0
    out = []
    for char in data:
        x = (x + 1) % 256
        y = (y + box[x]) % 256
        box[x], box[y] = box[y], box[x]
        out.append(chr(ord(char) ^ box[(box[x] + box[y]) % 256]))

    return ''.join(out)

if __name__ == '__main__':
    print(rc4('2019217872', '2019217872'))