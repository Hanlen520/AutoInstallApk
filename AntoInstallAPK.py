#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Author : Benjamin
# @Time   : 2018/8/9 11:17

import os
import re
import subprocess
import json

packages = "adb shell pm list packages"
filepath = "D:\\AgeingSpecialTest\\old\\res\\apk_aging_install_test_directory_1"

def File_Name(file_dir):
    RootFiles = []
    for root, dirs, files in os.walk(file_dir):
        # 当前路径下所有非目录子文件
        for file in files:
            if os.path.splitext(file)[1] == '.apk':
                RootFiles.append(str(file_dir)+"\\"+str(file))
    return RootFiles

def GetPackageName():
    testlist = []
    testdict = {}
    for i in File_Name(filepath):
        adbmessage = subprocess.Popen("aapt dump badging " + '"' + i + '"', stdout=subprocess.PIPE)
        adbmessage = str(adbmessage.communicate())

        packagename = re.compile(r"package: name='(.*?)'")
        packagename = re.findall(packagename, adbmessage)
        testlist.append(packagename[0])

        testdict["%s"%packagename[0]] = "%s"%i

        print(packagename)
    print(len(testlist))


    filepackages = open("filepackages", "w+")
    filepackages.write(str(testlist))
    filepackages.close()


    filepackagesdict = open("filepackagesdict", "w+")
    filepackagesdict.write(str(testdict))
    filepackagesdict.close()

def GetDevicesPackgName():
    adbmessage = subprocess.Popen(packages, stdout=subprocess.PIPE)
    adbmessage = str(adbmessage.communicate())

    compackagename = re.compile(r"package:(com.*?)\\r\\npackage:")
    compackagename = re.findall(compackagename, adbmessage)

    cnpackagename = re.compile(r"package:(cn.*?)\\r\\npackage:")
    cnpackagename = re.findall(cnpackagename, adbmessage)

    airpackagename = re.compile(r"package:(air.*?)\\r\\npackage:")
    airpackagename = re.findall(airpackagename, adbmessage)

    packagename = compackagename + cnpackagename + airpackagename

    Dpackagename = open("devices","w+")
    Dpackagename.write(str(packagename))
    Dpackagename.close()


filepackagesdict = json.loads(open("filepackagesdict","r+").readline().replace("'",'"'))

a = 1
for i in filepackagesdict:
    packagename = i
    checkpackage = "adb shell pm list packages | grep %s"%packagename
    message = str(subprocess.Popen(checkpackage, stdout=subprocess.PIPE).communicate())
    print(checkpackage)
    if len(message) <= 15:
        strs = "adb install " + '"%s"' % filepackagesdict.get(i)
        installmessage = os.popen(strs).readlines()
        print(strs)
        print(installmessage)
    else:
        print(a)
        print("Already installed")
        a += 1