# -*- coding: utf-8 -*-

import os
import re
import time
import pexpect, sys


class Android_app_test(object):

    def __init__(self, num):
        self.data = []
        self.num = num
        # self.app = 'com.tencent.mobileqq'
        # self.activity = 'com.tencent.mobileqq.activity.SplashActivity'
        self.local_app = 'GWM_2021_07_08.apk'
        self.device = 'RKW8XSGQAUCIAUTS'
        self.app = 'com.gwm.thailand'
        self.activity = 'com.beans.gwm.ui.MainActivity'
        self.path_to_apk = '/data/local/tmp'

    def check_devices(self):
        '''检查设备是否连接成功，如果成功返回True，否则返回False'''
        try:
            deviceInfo = os.popen('adb devices').read()
            print('deviceInfo:', deviceInfo, deviceInfo.split('\n')[1])
            if 'device' in deviceInfo.split('\n')[1]:
                os.popen('adb -s %s shell' % self.device)
                print('=' * 21, '已连接设备,开始测试', '=' * 21)
                print(self.deviceInfo())
                return True
            else:
                return False
        except Exception as e:
            print(e)

    def check_install(self):
        try:
            applist = os.popen('adb -s %s shell pm list packages' % self.device).read()
            # print('applist:\n', applist)
            for string_line in applist.split('\n'):
                for string_str in string_line.split(':'):
                    # print('*' * 10, string_str, '*' * 10)
                    if 'com.gwm.thailand' == string_str:
                        print('=' * 21, 'apk is installed before', '=' * 21)
                        return True
            return False
        except Exception as e:
            print(e)

    def deviceInfo(self):
        '''获取设备基础信息(如：厂商、型号、系统版本)'''
        deviceName = os.popen('adb -s %s shell getprop ro.product.model' % self.device).read()
        platformVersion = os.popen('adb -s %s shell getprop ro.build.version.release' % self.device).read()
        producer = os.popen('adb -s %s shell getprop ro.product.brand' % self.device).read()
        return "手机型号：%s %s，系统版本：Android %s" % (
            producer.replace('\n', ''), deviceName.replace('\n', ''), platformVersion.replace('\n', ''))

    def start_adb(self):
        '''运行adb命令，并记录启动耗时'''
        print('adb -s %s shell am start -W %s/%s' % (self.device, self.app, self.activity))
        start = 'adb -s %s shell am start -W %s/%s' % (self.device, self.app, self.activity)
        # data = re.findall(r'.*ThisTime: (.*?)TotalTime:(.*?)WaitTime: (.*?)Complete',
        #                   os.popen(start).read().replace('\n', ''))
        data = re.findall(r'.*TotalTime:(.*?)WaitTime: (.*?)Complete',
                          os.popen(start).read().replace('\n', ''))
        if len(data) == 0:
            print("adb命令执行出错，数据为空")
        else:
            self.data.append(int(data[0][0]))
            # print(type(data),data)
            return data

    def stop_adb(self):
        '''结束程序运行'''
        stop = 'adb -s %s shell am force-stop %s' % (self.device, self.app)
        os.popen(stop)

    def app_install(self):
        try:
            # install = 'adb -s %s  install -g -r %s' % (self.device, self.local_app)
            # print('install:', install)
            # os.popen(install)
            adb_push = 'adb -s {0} push {1} {2}/{3}'.format(self.device, self.local_app, self.path_to_apk,
                                                            self.local_app)
            print('adb_push:',adb_push)
            push_response = os.popen(adb_push)
            # print('push_response:', push_response.read())

            pm_install = 'adb -s {0} shell pm install -r {1}/{2}'.format(self.device, self.path_to_apk, self.local_app)
            print('pm_install:', pm_install)
            install_response = os.popen(pm_install)
            time.sleep(3)
            # print('pm_install:', install_response.read())

        except Exception as e:
            print('-' * 10, e, '-' * 10)

        # pexpect.run\pexpect.spawn only for linux
        # print('Installing apk: {0} for device: {1}'.format(self.path_to_apk, self.device))
        # file_name = os.path.basename(self.path_to_apk)
        # print('adb -s {0} push {1} {2}/{3}'.format(self.device, self.local_app, self.path_to_apk, self.local_app))
        # pexpect.run('adb -s {0} push {1} {2}/{3}'.format(self.device, self.local_app,self.path_to_apk, self.local_app))
        # p = pexpect.spawn('adb -s {0} shell'.format(self.device))
        # p.logfile = sys.stdout
        # p.expect('.*shell@.*', 20)
        # p.sendline('pm install {0}/{1}'.format(self.path_to_apk,self.local_app))
        # index = p.expect(['Success', '.*shell@.*'], 120)
        # p.sendline('rm {0}/{1}'.format(self.path_to_apk,self.local_app))

    def app_uninstall(self):
        uninstall = 'adb -s %s  uninstall %s' % (self.device, self.app)
        time.sleep(10)
        print('uninstall:', uninstall)
        os.popen(uninstall)

    def run_test_first(self):
        '''app 安装后首次启动耗时测试'''
        self.data.clear()
        if self.check_install() == True:
            self.app_uninstall()
        if self.check_devices() == True:
            self.stop_adb()
            for i in range(self.num):
                print('=' * 20, '安装后首次动测试：第%d次运行' % (i + 1), '=' * 20)
                self.stop_adb()
                self.app_install()
                time.sleep(3)
                test = self.start_adb()
                print("run_test_cold:", type(test), test)
                # print("ThisTime:%s,TotalTime:%s,WaitTime:%s" % (test[0][0], test[0][1], test[0][2]))
                print("TotalTime:%s,WaitTime:%s" % (test[0][0], test[0][1]))
                time.sleep(3)
                if i < self.num - 1:
                    self.app_uninstall()
            self.stop_adb()
            print('\n冷启动%s次平均耗时为：%s' % (len(self.data), sum(self.data) / len(self.data)))

        else:
            print("未连接安卓设备,请连接设备（3秒后重试）")
            while True:
                time.sleep(3)
                self.run_test_cold()

    def run_test_cold(self):
        '''app 冷启动耗时测试'''
        self.data.clear()
        if self.check_devices() == True:
            self.stop_adb()
            for i in range(self.num):
                print('=' * 20, '冷启动测试：第%d次运行' % (i + 1), '=' * 20)
                self.stop_adb()
                self.app_install()
                time.sleep(3)
                test = self.start_adb()
                print("run_test_cold:", type(test), test)
                # print("ThisTime:%s,TotalTime:%s,WaitTime:%s" % (test[0][0], test[0][1], test[0][2]))
                print("TotalTime:%s,WaitTime:%s" % (test[0][0], test[0][1]))
                time.sleep(3)
            self.stop_adb()
            print('\n冷启动%s次平均耗时为：%s' % (len(self.data), sum(self.data) / len(self.data)))

        else:
            print("未连接安卓设备,请连接设备（3秒后重试）")
            while True:
                time.sleep(3)
                self.run_test_cold()

    def run_test_hot(self):
        '''app 热启动耗时测试'''
        self.data.clear()
        if self.check_devices() == True:
            os.popen('adb -s %s shell am start -W %s/%s' % (self.device, self.app, self.activity))
            time.sleep(3)
            for i in range(self.num):
                print('=' * 20, '热启动测试：第%d次运行' % (i + 1), '=' * 20)
                os.popen('adb -s %s shell input keyevent 3' % self.device)
                time.sleep(3)
                test = self.start_adb()
                time.sleep(3)
                # print("ThisTime:%s,TotalTime:%s,WaitTime:%s" % (test[0][0], test[0][1], test[0][2]))
                print("TotalTime:%s,WaitTime:%s" % (test[0][0], test[0][1]))

            self.stop_adb()
            print('\n热启动%s次平均耗时为：%s' % (len(self.data), sum(self.data) / len(self.data)))

        else:
            print("未连接安卓设备,请连接设备（3秒后重试）")
            while True:
                time.sleep(3)
                self.run_test_hot()


if __name__ == '__main__':
    apptest = Android_app_test(1)
    apptest.check_devices()
    print("---check_devices done---")
    if apptest.check_install() == True:
        apptest.app_uninstall()
        print("---app_uninstall done---")
    apptest.app_install()
    print("---app_install done---")

    # apptest.run_test_first()
    # apptest.run_test_cold()
    # apptest.run_test_hot()
