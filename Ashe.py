# !/usr/bin/env python
# -*- coding:utf-8 -*-
__author__ = 'bit4'
__github__ = 'https://github.com/bit4woo'

import os.path
from lib.xmlparser import *
from WVS.WVS10 import *
import shutil


def interactive():
    #t = tabCompleter()
    print "\n\nWelcome to interactive mode!\n\n"

    task_home_dir = os.path.join(os.path.dirname(__file__), "task")
    while True:
        tasks = os.listdir(task_home_dir)
        for task in tasks:
            if os.path.isfile(task):
                tasks.remove(task)
        print "{0} tasks existed:".format(len(tasks))
        for item in tasks:
            print item

        task_name = raw_input("\n\n*.Input a existed task name to operate it or Input a new task name to create.\n*.Input x to exit Ashe.\n==>")
        if task_name == 'x':
            break
        elif task_name == "":
            continue
        else:
            task_dir = os.path.join(task_home_dir,task_name)

            if os.path.isdir(task_dir):
                choice = raw_input("the task already exist, operate this task? (Y/n)")
                if choice.lower() not in ["y","yes",""]:
                    continue
            else:
                os.mkdir(task_dir)
                print "task {0} created, chose what to do:".format(task_name)

            urls_file = os.path.join(task_dir, "urls.txt")
            urls_scanned_file = os.path.join(task_dir, "urls_scanned.txt")
            while True:
                index = '''
                [Current Task: {0}]
                1. Delete this task
                2. Input the xml file and parse to urls
                3. Add urls to scan
                4. Query high vuln from wvs
                5. back
                ==>
                '''.format(task_name)
                choice = raw_input(index)

                if choice == "1":
                    delete = raw_input("Are you sure to DELETE this task?(y/N)")
                    if delete.lower() in ["y","yes"]:
                        shutil.rmtree(task_dir)
                        break
                    else:
                        continue
                elif choice == "2":
                    xmlfile = raw_input("parse xml, please input the xml file:==>")
                    if os.path.isfile(xmlfile):
                        xml_file = os.path.join(task_dir, xmlfile)
                        shutil.copy(xmlfile,xml_file)
                        url_list = GetHttp(xmlfile)
                        fp = open(urls_file, "w")
                        fp.writelines("\n".join(url_list))
                        fp.close()
                    continue
                elif choice == "3":
                    if os.path.isfile(urls_file):
                        fp = open(urls_file,"r")
                        urls = fp.readlines()
                        fp.close()
                        number_added = AddToWVS(urls)
                        print "{0} urls added".format(number_added)
                        if number_added >= 0:
                            urls_left = urls[number_added+1:-1]
                            urls_scanned = urls[0:number_added]
                        fp = open(urls_file,"w")
                        fp.writelines(urls_left)
                        fp.close()

                        fp = open(urls_scanned_file,"a")
                        fp.writelines(urls_scanned)
                        fp.write("\n___________{0}_________\n".format(datetime.datetime.now().strftime("%m/%d/%Y %H%M")))
                        fp.close()
                elif choice == "4":
                    QueryFromWVS()
                elif choice == "5":
                    break
                else:
                    continue


if __name__ == "__main__":
    interactive()