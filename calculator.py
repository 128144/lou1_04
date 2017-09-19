#!/usr/bin/env python3

import sys
import os
import configparser
import argparse
from multiprocessing import Process, Queue

queue = Queue()

args_obj = argparse.ArgumentParser()
args_obj.add_argument('-c')
args_obj.add_argument('-d')
args_obj.add_argument('-o')

args = args_obj.parse_args()
yuangong_filename = args.d
peizhi_filename = args.c
shuchu_filename = args.o
    
if os.path.isfile(yuangong_filename) == False:
    print("yuangong_filename bucunzai.")
    exit()
     
if os.path.isfile(peizhi_filename) == False:
    print("peizhi_filename bucunzai.")
    exit()

class Config:
    def __init__(self, name):
        self._name = name
    
    def get_info(self,filename,chengshi = 'default'):
        pass

    filename = peizhi_filename
    #cf = configparser.ConfigParser()
    #cf.read(filename)
    #JiShuL = float(cf.get("default","JiShuL"))
    #JiShuH = float(cf.get("default","JiShuH"))
    #YangLao = float(cf.get("default","YangLao"))
    #YiLiao = float(cf.get("default","YiLiao"))
    #ShiYe = float(cf.get("default","ShiYe"))
    #GongShang = float(cf.get("default","GongShang"))
    #ShengYu = float(cf.get("default","ShengYu"))
    #GongJiJin = float(cf.get("default","GongJiJin"))
    #SheBaoJiShu = YangLao + YiLiao + ShiYe + GongShang + ShengYu + GongJiJin
    with open(filename,'r') as f:
        a = f.readlines()
        for i in range(0,len(a)):
            if 'JiShuL' in a[i]:
                JiShuL = float(a[i].split('=')[1])
            if 'JiShuH' in a[i]:
                JiShuH = float(a[i].split('=')[1])
            if 'YangLao' in a[i]:
                YangLao = float(a[i].split('=')[1])
            if 'YiLiao' in a[i]:
                YiLiao = float(a[i].split('=')[1])
            if 'ShiYe' in a[i]:
                ShiYe = float(a[i].split('=')[1])
            if 'GongShang' in a[i]:
                GongShang = float(a[i].split('=')[1])
            if 'ShengYu' in a[i]:
                ShengYu = float(a[i].split('=')[1])
            if 'GongJiJin' in a[i]:
                GongJiJin = float(a[i].split('=')[1])
    SheBaoJiShu = YangLao + YiLiao + ShiYe + GongShang + ShengYu + GongJiJin
   
        



def shebao(gongzi):
    a = Config('xx')
    if gongzi > a.JiShuH:
        shebao = a.JiShuH * a.SheBaoJiShu
    elif gongzi > a.JiShuL:
        shebao = gongzi * a.SheBaoJiShu
    elif gongzi > 0:
        shebao = a.JiShuL * a.SheBaoJiShu
    else:
        shebao = 0
    return shebao

def jisuan_ynse(ynssdr):
    if ynssdr > 80000:
        ynse = ynssdr * 0.45 -13505
    elif ynssdr > 55000:
        ynse = ynssdr * 0.35 - 5505
    elif ynssdr > 35000:
        ynse = ynssdr * 0.30 -2755
    elif ynssdr > 9000:
        ynse = ynssdr * 0.25 -1005
    elif ynssdr > 4500:
        ynse = ynssdr * 0.20 -555
    elif ynssdr > 1500:
        ynse = ynssdr * 0.10 -105
    elif ynssdr > 0:
        ynse = ynssdr * 0.03
    else:
        ynse = 0
    return ynse
    

def user_info():
    try:

        # yuangong_filename = '/home/shiyanlou/user.csv'
        with open(yuangong_filename, 'r') as f:
            alist = f.readlines()

        blist = []
        clist = []
        for i in alist:
            gonghao = i.split(",")[0]
            # print(gonghao)
            gzje = int(float(i.split(",")[1]))
            # print(gzje)
            SheBao = shebao(gzje)
            # print(SheBao)
            # gzje = gzje * (1 - wuxianyijin)
            ynssdr = gzje - 3500 - SheBao

            ynse = jisuan_ynse(ynssdr)
            shgz = gzje - ynse - SheBao
            blist.append('{},{},{:.2f},{:.2f},{:.2f}'.format(gonghao, gzje, SheBao, ynse, shgz)) 
        clist.append(blist)
        #print(clist[0][0])
        queue.put(clist)
        #print(len(clist[0]))
            # print(ynse)
            # print(shgz)
            # print('{} : {:.2f}'.format(gonghao,(gzje - ynse )))
            # print('{},{},{:.2f},{:.2f},{:.2f}'.format(gonghao,gzje,SheBao,ynse,shgz))
            #with open(shuchu_filename, 'a') as f:
                #f.write(('{},{},{:.2f},{:.2f},{:.2f}'.format(gonghao, gzje, SheBao, ynse, shgz)) + '\n')
    except:
        print("Parameter Error")


def write_info():
    alist = queue.get()
    with open(shuchu_filename, 'a') as f:
       # writer= csv.writer(f)
        for i in range(len(alist[0])):
            f.write(alist[0][i] + '\n')

def main():
   
    Process(target=user_info).start()
    Process(target=write_info).start()
    


if __name__=='__main__':
    main()

