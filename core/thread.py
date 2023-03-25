#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2023/3/25 11:29
# @Author  : 桥话语权
# @File    : thread.py
# @Software: PyCharm
"""
 *            佛曰:
 *                   写字楼里写字间，写字间里程序员；
 *                   程序人员写程序，又拿程序换酒钱。
 *                   酒醒只在网上坐，酒醉还来网下眠；
 *                   酒醉酒醒日复日，网上网下年复年。
 *                   但愿老死电脑间，不愿鞠躬老板前；
 *                   奔驰宝马贵者趣，公交自行程序员。
 *                   别人笑我忒疯癫，我笑自己命太贱；
 *                   不见满街漂亮妹，哪个归得程序员？
"""
import subprocess
from PyQt5.QtCore import QThread, pyqtSignal


class StartThread(QThread):
    """启动线程"""
    def __init__(self, path, parameter):
        super().__init__()
        self.path = path
        self.parameter = parameter
        self.signal = True

    def run(self):
        # 启动外部程序
        proc = subprocess.Popen([f"{self.path} {self.parameter}"])
        while self.signal:
            # 监控程序是否退出
            if proc.poll() is None:
                self.sleep(1)
                continue
            else:
                # 重新启动程序
                proc = subprocess.Popen({f"{self.path} {self.parameter}"})
