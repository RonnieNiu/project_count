# -*- coding: utf-8 -*-

import os
import sys
#from functools import reduce

temp_result = []
count = 0

if os.name == "nt":
    cad = 'type %s  | find /v"" /c'
else:
    cad = 'cat %s | wc -l'

# The method is implemented recursively, but it is very slow
'''
def each_dir(path,lang):
    return list(map(lambda each:os.path.join(path,each),\
                    [each for each in os.listdir(path) if os.path.isfile(os.path.join(path,each)) and\
      os.path.splitext(each)[1] == lang]))

def total(path,lang):
    global result
    try:
        for each in os.listdir(path):
            if os.path.isdir(os.path.join(path,each)):
                #result += each_dir(os.path.join(path,each),lang)
                total(os.path.join(path,each),lang)
            elif os.path.splitext(each)[1] == lang:
                temp_result.append(os.path.join(path,each))
    except Exception:
        pass
    return temp_result
'''
#use os.walk()
def total(path,lang):
    for root,dirs,files in os.walk(path):
        for each in files:
            if os.path.splitext(each)[1] == lang:
                temp_result.append(os.path.join(root,each))
    return temp_result

if  __name__ == "__main__":
    if len(sys.argv) != 3:
        print("Usage:python project_count.py /path/project .py/.c/.java/...etc")
        sys.exit()
    base_path = sys.argv[1]
    lang = sys.argv[2]

    try:
        result = list(map(lambda x:(x,int(os.popen(cad % x).read().strip("\n"))), total(base_path,lang)))
        print("\nThe %s project have %s file as follows:\n"%(base_path,lang))
        for index in range(len(result)):
            print("%d:%s, row_nums:%d"%(index+1,result[index][0],result[index][1]))
            count +=result[index][1]
        print("\nThe total code numbers is %d\nThe total file numbers is:%d"%(count,len(result)))
    except Exception:
        pass
    except BaseException:
        pass

