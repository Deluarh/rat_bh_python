# -*- coding: utf-8 -*-
import os
def run(**args):
    #print("[*] In dirlister module.")
    files = os.listdir(".") #возвращает список файлов в папке
    return str(files)
