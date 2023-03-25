# Auto Restart 
[![](https://img.shields.io/badge/Python-3.10-blue) ](https://www.python.org/)
[![](https://img.shields.io/badge/PyQt-5.15-green) ](https://doc.qt.io/qt.html#qtforpython)
[![](https://img.shields.io/badge/license-GPL3.0-orange)](https://github.com/ruixiaotian/auto-restart/blob/main/LICENSE)


Auto Restart 是一种具有自动重启功能的监控程序，它可以监控指定的程序，如果该程序意外退出或崩溃，Auto Restart会自动重新启动该程序，以确保程序可以持续运行。以下是一些它的特点：

+ 自动重启功能：Auto Restart 可以在程序意外退出或崩溃时自动重新启动该程序，以确保程序可以持续运行。

+ 监控指定程序：用户可以指定要监控的程序及其启动参数，以确保程序的正确运行。

+ 界面友好：Auto Restart 提供图形化界面，操作简单方便，可以轻松完成程序的监控和管理。


### 如何打包?
最方便快捷的就是pyinstaller方法了(发行版使用的是nuitka打包)

```
# pyinstaller方法
pip install -r requirement.txt
pip install -r pyinstaller
pyinstaller -F -w -i ./img/icon/icon.ico main.py
```
```
# nuitka方法
pip install -r requirement.txt
pip install -r nuitka

# 带控制台
nuitka --mingw64 --standalone --show-progress --show-memory --enable-plugin=pyqt5 --nofollow-import-to=http,email,urllib,click --windows-icon-from-ico=./img/icon/icon.ico --windows-company-name=name --windows-product-name=AutoRestart --windows-file-version=1.0.0 --output-dir=out .\main.py

# 不带控制台
nuitka --mingw64 --windows-disable-console --standalone --show-progress --show-memory --enable-plugin=pyqt5 --nofollow-import-to=http,email,urllib,click --windows-icon-from-ico=./img/icon/icon.ico --windows-company-name=name --windows-product-name=AutoRestart --windows-file-version=1.0.0 --output-dir=out .\main.py
```

### 使用方法
1. 点击添加
2. 选择一个运行程序(不建议使用快捷方式)
3. 在对话框输入运行参数(没有则留空)
4. 点击运行,程序自动隐藏到托盘图标

### License
该程序遵循GPT3.0开源协议
