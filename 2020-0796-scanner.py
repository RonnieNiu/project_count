#!/usr/bin/env python3
# -*- coding: utf-8 -*-

#使用三方库协程多并发执行
# import gevent
# from gevent import monkey
# monkey.patch_all()

import asyncio

import subprocess
import threading
import time
import sys
import datetime
import os
import functools
from multiprocessing import Process, Pool, cpu_count


def _run_time(func):
    @functools.wraps(func)
    def wrapper(*args,**kwargs):
        starttime = datetime.datetime.now()
        func(*args,**kwargs)
        endtime = datetime.datetime.now()
        print("共耗时:%d分%d秒!" % ((endtime - starttime).seconds // 60, (endtime - starttime).seconds % 60))
        return None
    return wrapper

def _get_ip(ip_file):
    ip_list = []
    with open (ip_file,"r") as f:
        for each in f.readlines():
            ip = each.strip("\n").strip(" ").split(" ")[-1]
            if len(ip):
                ip_list.append(ip)
    # print len(ip_list)
    return ip_list

def _run(ip):
    try:
        print(ip)
        res = subprocess.check_output("CVE-2020-0796-Scanner.exe %s"%ip,shell=True)
        print(res.decode('utf-8'))

        if "仍存在漏洞风险" in res.decode('utf-8'):
            with open(sys.argv[1].split("_")[0] + "_vulnerable.txt", "a") as f2:
                f2.write("%s is: WARNING: SERVER IS VULNERABLE !!!\n"%(ip))
        time.sleep(5)
    except subprocess.CalledProcessError as e:
        print(e)
        pass


#(((######################################################################################################
#多线程实现(
#用semaphore 控制线程数量
sem = threading.Semaphore(50)

def run_threats(ip):
    _run(ip)
    sem.release()

@_run_time
def start_threads(ip_list):
    thread_list = [threading.Thread(target=run_threats, args=(ip,)) for ip in ip_list]
    for t in thread_list:
        sem.acquire()
        t.setDaemon(True)
        t.start()

    for t in thread_list:
        t.join()
    print("----------main thread---- {0}: ，属于进程 ；l{1}".format(threading.current_thread().name, os.getpid()))
######################################################################################################)))

"""
#(((############################################################################################
#多进程+多线程实现
@_run_time
def start_process(ip_lists):
    # 方法一: 使用Pool进程池方式创建子进程，这是多进程+多线程实现
    pool = Pool(cpu_count())
    for ip_list in ip_lists:
        pool.apply_async(start_threads,args=(ip_list,))

    pool.close()
    pool.join() #使用Pool方法创建时，记得一定调用join()使主进程等待子进程结束后在结束，否则子进程不会执行
###############################################################################################)))
""""

"""
#多进程实现
#(((#############################################################################################
@_run_time
def start_process(ip_lists):
    # 方法一: 使用Pool进程池方式创建子进程
    pool = Pool(cpu_count())
    for ip in ip_list:
        pool.apply_async(_run,args=(ip,))

    pool.close()
    pool.join() #使用Pool方法创建时，记得一定调用join()使主进程等待子进程结束后在结束，否则子进程不会执行

    ##方法二: 使用Process创建子进程
    # process_list = [Process(target=_run,args=(ip,)) for ip in ip_list]
    # for each_p in process_list:
    #     each_p.start()
    #
    # for each_p in process_list:
    #     each_p.join()

###############################################################################################)))
"""

"""
#(((#####################################################################################################
#三方库gevent 实现协程
@_run_time
def start_gevent(ip_list):
    greenlets = [gevent.spawn(_run, ip) for ip in ip_list]
    gevent.joinall(greenlets=greenlets)
######################################################################################################)))
"""

"""
#(((########################################################################################################
@asyncio.coroutine
def _run_coroutine(ip):
    try:
        # print(ip)
        # res = subprocess.check_output("CVE-2020-0796-Scanner.exe %s"%ip,shell=True)
        # print(res.decode('utf-8'))
        yield from asyncio.sleep(1)

        # if "仍存在漏洞风险" in res.decode('utf-8'):
        #     with open(sys.argv[1].split("_")[0] + "_vulnerable.txt", "a") as f2:
        #         f2.write("%s is: WARNING: SERVER IS VULNERABLE !!!\n"%(ip))

    except subprocess.CalledProcessError as e:
        print(e)
        pass

@asyncio.coroutine
def _start_coroutine(ip_list):
    tasks = [_run_coroutine(ip) for ip in ip_list]
    done,pending = yield from asyncio.wait(tasks)
    print(done)

@_run_time
def main_coroutine(ip_list):
    loop = asyncio.get_event_loop()
    loop.run_until_complete(_start_coroutine(ip_list))
    loop.close()
#########################################################################################################)))
"""

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage:python %s ip_445.txt"%sys.argv[0])
        # main_coroutine(_get_ip("10.99.0.0_445.txt".split("_")[0] + "_445.txt"))
        start_process([_get_ip("10.99.0.0_445.txt".split("_")[0] + "_445.txt"),_get_ip("10.101.0.0_445.txt".split("_")[0] + "_445.txt"),_get_ip("10.130.0.0_445.txt".split("_")[0] + "_445.txt")])
        # sys.exit()

    # start_threads(_get_ip(sys.argv[1].split("_")[0] + "_445.txt"))

    #start_gevent(_get_ip(sys.argv[1].split("_")[0] + "_445.txt"))





