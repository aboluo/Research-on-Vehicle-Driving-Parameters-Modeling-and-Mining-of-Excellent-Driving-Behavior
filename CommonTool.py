# _*_ coding: UTF-8 _*_
__author__ = 'aboluo'
from math import *

import numpy as np
import pandas as pd
import os
import csv
import time

commonAllFileList = []
#获取指定目录下所有的CSV文件,记得结合全局变量fileList这个全局变量一块使用
def getAllCsvFile(inputDir):
    #2016-21-25,Added by lzm，置空，防止函数多重调用
    # fileList = []
    Flag = False
    dirList = []
    if(False == os.path.exists(inputDir)):
        return Flag
    files = os.listdir(inputDir)
    for f in files:
        tempF = inputDir + '/' + f
        #是目录
        if(os.path.isdir(tempF)):
            #排除.打头目录
            if(f[0] == '.'):
                pass
            else:
                dirList.append(tempF)
        #是文件
        if(os.path.isfile(tempF)):
            #且是CSV文件
            if(tempF.find('.csv') == (len(tempF) - 4 )):
                commonAllFileList.append(tempF)
    #递归查询
    for dirF in dirList:
        print "子目录:[%s]" % (dirF)
        getAllCsvFile(dirF)

    #查询完毕，返回
    print "获取目录:[%s]" % (inputDir) + "下所有的CSV文件完毕!,文件个数为:%d" % (len(commonAllFileList))
    return commonAllFileList

fileWithoutDirList = []
#2016-11-24,Added by lzm,获取指定目录下所有的CSV文件,记得结合全局列表变量fileWithoutDirList这个全局变量一块使用
def getAllCsvFileWithoutDirList(inputDir):
    fileWithoutDirList = []
    Flag = False
    dirList = []
    if(False == os.path.exists(inputDir)):
        return Flag
    files = os.listdir(inputDir)
    for f in files:
        tempF = inputDir + '/' + f
        #是目录
        if(os.path.isdir(tempF)):
            #排除.打头目录
            if(f[0] == '.'):
                pass
            else:
                dirList.append(tempF)
        #是文件
        if(os.path.isfile(tempF)):
            #且是CSV文件
            if(tempF.find('.csv') == (len(tempF) - 4 )):
                fileWithoutDirList.append(f)
    #递归查询
    for dirF in dirList:
        print "子目录:[%s]" % (dirF)
        getAllCsvFile(dirF)

    #查询完毕，返回
    print "获取目录:[%s]" % (inputDir) + "下所有的CSV文件完毕!,文件个数为:%d" % (len(commonAllFileList))
    return fileWithoutDirList

#2016-12-11，Added by lzm，网上版本，获取所有文件
def getListFiles(path):
    ret = []
    for root, dirs, files in os.walk(path):
        for filespath in files:
            ret.append(os.path.join(root,filespath))
    print "获取目录:[%s]" % (path) + "下所有的文件完毕!,文件个数为:%d" % (len(ret))
    return ret

# #2016-12-11，Added by lzm，网上版本，获取所有文件
# def getListFiles(inputDir):
#     #2016-21-25,Added by lzm，置空，防止函数多重调用
#     # fileList = []
#     Flag = False
#     dirList = []
#     if(False == os.path.exists(inputDir)):
#         return Flag
#     files = os.listdir(inputDir)
#     for f in files:
#         tempF = inputDir + '/' + f
#         #是目录
#         if(os.path.isdir(tempF)):
#             #排除.打头目录
#             if(f[0] == '.'):
#                 pass
#             else:
#                 dirList.append(tempF)
#         #是文件
#         if(os.path.isfile(tempF)):
#             #且是CSV文件
#             if(tempF.find('.csv') == (len(tempF) - 4 )):
#                 commonAllFileList.append(tempF)
#     #递归查询
#     for dirF in dirList:
#         print "子目录:[%s]" % (dirF)
#         getAllCsvFile(dirF)
#
#     #查询完毕，返回
#     print "获取目录:[%s]" % (inputDir) + "下所有的CSV文件完毕!,文件个数为:%d" % (len(commonAllFileList))
#     return commonAllFileList

#关键区域的元组数据，存放到一个元组里
keyAreaArr = ("106.459565-29.570232",
			"106.45878-29.566944",
			"106.458336-29.565036",
			"106.453246-29.561949",
			"106.451102-29.563839",
			"106.443377-29.566707",
			"106.44178-29.571123",
			"106.442399-29.574738",
			"106.442667-29.579099",
			"106.442389-29.582976",
			"106.440573-29.589554",
			"106.435848-29.591864",
			"106.435883-29.59526",
			"106.435584-29.599946",
			"106.436263-29.60203",
			"106.438809-29.604325",
			"106.442713-29.605981",
			"106.445181-29.606481",
			"106.445964-29.610932",
			"106.447658-29.613047",
			"106.451095-29.613801");

#设置相关变量
#地球平均半径
avgEarthRadius = 6378137;
#E
E = 2.7182818284590452354;
#PI
PI = 3.14159265358979323846;
#地球赤道周长,单位(m)
equaCircum = 40076000;
#地球上每一个纬度的距离,单位(m)--地球周长除以360度
distancePerDegreeInLa = 40076000/360;

# input Lat_A 纬度A
# input Lng_A 经度A
# input Lat_B 纬度B
# input Lng_B 经度B
# output distance 距离(km)
#根据两地的经纬度计算两地的距离，参考 http://www.tuicool.com/articles/ayi2IzA
def countDistanceInlongLa(Lat_A, Lng_A, Lat_B, Lng_B):
    ra = 6378.140  # 赤道半径 (km)
    rb = 6356.755  # 极半径 (km)
    flatten = (ra - rb) / ra  # 地球扁率
    rad_lat_A = radians(Lat_A)
    rad_lng_A = radians(Lng_A)
    rad_lat_B = radians(Lat_B)
    rad_lng_B = radians(Lng_B)
    pA = atan(rb / ra * tan(rad_lat_A))
    pB = atan(rb / ra * tan(rad_lat_B))
    xx = acos(sin(pA) * sin(pB) + cos(pA) * cos(pB) * cos(rad_lng_A - rad_lng_B))
    c1 = (sin(xx) - xx) * (sin(pA) + sin(pB)) ** 2 / cos(xx / 2) ** 2
    c2 = (sin(xx) + xx) * (sin(pA) - sin(pB)) ** 2 / sin(xx / 2) ** 2
    dr = flatten / 8 * (c1 - c2)
    distance = ra * (xx + dr)
    return distance

#计算两地的距离，输出应该是km吧??? ，参考自 http://blog.csdn.net/vernice/article/details/46581361
def haversine(lon1, lat1, lon2, lat2): # 经度1，纬度1，经度2，纬度2 （十进制度数）
    """
    Calculate the great circle distance between two points
    on the earth (specified in decimal degrees)
    """
    # 将十进制度数转化为弧度
    # 将十进制度数转化为弧度
    lon1, lat1, lon2, lat2 = map(radians, [lon1, lat1, lon2, lat2])

    # haversine公式
    dlon = lon2 - lon1
    dlat = lat2 - lat1
    a = sin(dlat/2)**2 + cos(lat1) * cos(lat2) * sin(dlon/2)**2
    c = 2 * asin(sqrt(a))
    r = 6371 # 地球平均半径，单位为公里
    return c * r * 1000

#判断是否在关键区域里，Lat:纬度， 经度:Lng,返回关键区域的编号,-1表示不在关键区域，关键区域标号1-21，从1开始
def isInKeyArea(Lat, Lng):
    keyAreaNo = -1
    #误差距离设置为100m
    errorGap = 100
    #引入全局变量
    global keyAreaArr
    i = 1
    for keyAreaStr in keyAreaArr:
        singleKeyAreaArr = keyAreaStr.split('-')
        #获取经纬度
        keyAreaLng = singleKeyAreaArr[0]
        keyAreaLat = singleKeyAreaArr[1]
        print "keyAreaLng:%s, keyAreaLat:%s, i:%d" % (keyAreaLng, keyAreaLat,i)
        #计算是否跟关键区域距离在误差范围内
        distanceInM = 1000 * countDistanceInlongLa(float(keyAreaLat), float(keyAreaLng), Lat, Lng)
        print "distanceInM:%f" % (distanceInM)
        if (distanceInM) < errorGap:
            #如果在关键区域里，直接终止
            keyAreaNo = i
            break
        i = i + 1
    #
    return keyAreaNo

# Lat_A=29.570232
# Lng_A=106.459565
# Lat_B=29.572961
# Lng_B=106.470169
# distance=countDistanceInlongLa(Lat_A,Lng_A,Lat_B,Lng_B)
# print('Distance={0:10.3f} km'.format(distance))
#
# #test
# #重大 1
# print isInKeyArea(29.572961, 106.470169)
# #陈家湾 4
# print isInKeyArea(29.565035, 106.464157)
