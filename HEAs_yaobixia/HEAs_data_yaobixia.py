#!/usr/bin/env python
# coding: utf-8
#W13361353383@126.com
#thsu@gmail.com

import os
import fnmatch
import xlrd
import re 
import csv

"""
处理高熵合金数据，读取infile类型文件，获取化学式，能量，X，晶格并写入outfile文件中
容忍掺杂、能量和X数据缺失，但不容忍化学式通式缺失
处理9列*3行共27组数据，每组数据X*1行，掺杂和能量*9行*1列，数据数量不同修改29-30行和61行即可
format  yaobixia.xls
"""

infile = '*.xls'
outfile = 'data.csv'

#写入表头
header = [ '化学式','能量',"X",'晶格'] #数据列名
with open(outfile, 'w', newline='',encoding='utf-8') as fp: 
    writer = csv.DictWriter(fp,header)
    writer.writeheader()  # 写入列名
fp.close()

#获取目录下所有文件
files = fnmatch.filter(os.listdir(), infile)
for file in files:   
    #打开文件，获取excel文件的workbook（工作簿）对象
    excel = xlrd.open_workbook(file,encoding_override="utf-8")
    #获取sheet对象
    all_sheet = excel.sheets()
    
    for sheet in all_sheet:
        for col in range(1,19,2):
            for row in range(0,32,11):
                dic = {}
                #获取sheet名称
                dic["晶格"] = sheet.name

                def get_X():#获取特征X
                    a = sheet.col_values(col)[row].split("=")
                    X = int(a[1])
                    dic["X"] = X

                #获取结构通式
                preconfig = sheet.col_values(0)[row]
                pattern = re.compile(r'\d\d-*x|\d\d|[A-Z][a-z]|[a-z]')
                configlist = pattern.findall(preconfig)
                
                def get_config():#获取化学式，预防空数据
                    x = sheet.col_values(col)[row+num]
                    a = configlist[:]
                    for i in (1, 3, 5):
                        if configlist[i].isdigit()==False:
                            c = a[i].split("-")
                            if c[0].isdigit() == True:
                                a[i] = str(float(c[0])-x)
                            else:
                                a[i] = str(x)                                
                    dic['化学式'] = ""
                    for i in range(len(configlist)):
                        dic['化学式'] += a[i]
                    return dic
                
                data = []
                for num in range(1,10):                 
                    #获取energy
                    dic["能量"] = sheet.col_values(col+1)[row+num]
                    
                    #获取结构式
                    try:
                        get_X()
                        get_config()
                        data.append(dic.copy())
                    except:
                        pass
                
                
                #写入文件
                with open(outfile, 'a', newline='',encoding='utf-8') as fp:
                    writer = csv.DictWriter(fp,header)                  
                    writer.writerows(data) # 写入数据
                    fp.close()




