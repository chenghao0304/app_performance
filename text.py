# self.app = 'com.gwm.thailand'
# self.activity = 'com.beans.gwm.ui.MainActivity'
# /usr/bin/python
# encoding:utf-8
import csv
import os
import time


class App(object):
    def __init__(self):
        self.content = ""
        self.startTime = 0

    # 启动App
    def LaunchApp(self):
        cmd = 'adb shell am start -W -n com.gwm.thailand/com.beans.gwm.ui.MainActivity'
        cmd = 'adb shell am start -W com.gwm.thailand/com.beans.gwm.ui.MainActivity'
        self.content = os.popen(cmd)
        # ThisTime: 最后一个启动的Activity的启动耗时；
        # TotalTime: 自己的所有Activity的启动耗时；
        # WaitTime: ActivityManagerService启动App的Activity时的总时间（包括当前Activity的onPause()
        # 和自己Activity的启动）

        print("LaunchApp self.content", self.content)
        for line in self.content.readlines():
            print("GetLaunchedTime line:", line)

    # 停止App
    def StopApp(self):
        # 冷启动停止
        cmd = 'adb shell am force-stop com.gwm.thailand'
        # 热启动停止
        # cmd = 'adb shell input keyevent 3'
        os.popen(cmd)

    # 获取启动时间
    def GetLaunchedTime(self):
        for line in self.content.readlines():
            # print("GetLaunchedTime line",line)
            if "ThisTime" in line:
                self.startTime = line.split(":")[1]
                break
        return self.startTime


# 控制类
class Controller(object):
    def __init__(self, count):
        self.app = App()
        self.counter = count
        self.alldata = [("timestamp", "elapsedtime")]

    # 单次测试过程
    def testprocess(self):
        self.app.LaunchApp()
        time.sleep(5)
        elpasedtime = self.app.GetLaunchedTime()
        print("elpasedtime", elpasedtime)
        self.app.StopApp()
        time.sleep(3)
        currenttime = self.getCurrentTime()
        print("currenttime", currenttime)
        self.alldata.append((currenttime, elpasedtime))

    # 多次执行测试过程
    def run(self):
        while self.counter > 0:
            self.testprocess()
            self.counter = self.counter - 1

    # 获取当前的时间戳
    def getCurrentTime(self):
        currentTime = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
        return currentTime

    # 数据的存储
    def SaveDataToCSV(self):
        # csvfile = open('startTime2.csv', 'wb')
        # writer = csv.writer(csvfile)
        # # writer.writerows(self.alldata)
        # bs = bytes(str(self.alldata), encoding='utf-8')
        # writer.writerows(bs)
        # csvfile.close()
        with open('startTime2.csv', 'w', newline='') as f:
            mywrite = csv.writer(f)
            mywrite.writerow(self.alldata)


if __name__ == "__main__":
    controller = Controller(1)
    controller.run()
    controller.SaveDataToCSV()
