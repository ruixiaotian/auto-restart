#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2023/3/21 19:44
# @Author  : 桥话语权
# @File    : __init__.py.py
# @Software: PyCharm
"""
程序的UI设计均在此处
"""
import winreg
import sys
from pathlib import Path
from PyQt5.QtWidgets import QApplication, QWidget, QPushButton, QGridLayout, QCheckBox, QSpacerItem, QSizePolicy, \
    QTableWidget, QAbstractItemView, QTableWidgetItem, QFileDialog, QInputDialog
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QIcon, QFont
from core.file_operate import FileOperate
from core.thread import StartThread


class MainWindow(QWidget):
    __file_operate = FileOperate()

    def __init__(self):
        super().__init__()
        self.setup_window()
        self.setup_layout()

    def setup_window(self):
        """
        设置窗体属性
        :return:
        """
        self.setWindowTitle("自动重启")
        self.setWindowIcon(QIcon("./img/icon/icon.png"))
        self.setFixedSize(600, 300)

    def setup_layout(self):
        """程序布局设置"""
        layout = QGridLayout()
        layout.addLayout(self.setup_top(), 0, 0, 1, 1, Qt.AlignmentFlag.AlignTop)
        layout.addLayout(self.setup_bottom(), 1, 0, 1, 1, Qt.AlignmentFlag.AlignTop)
        self.setLayout(layout)

    def setup_top(self):
        """顶部设置"""
        # 创建载体
        layout = QGridLayout()

        # 创建载体子控件
        self.run_and_stop_btn = QPushButton("启动", self)
        add_button = QPushButton("添加", self)
        rm_button = QPushButton("移除", self)
        self.boot_auto_start_button = QCheckBox("开机自启动", self)
        self.save_config_button = QCheckBox("保存配置", self)

        # 设置按钮属性
        # 设置大小
        self.run_and_stop_btn.setFixedSize(250, 60)
        add_button.setFixedSize(60, 60)
        rm_button.setFixedSize(60, 60)
        self.boot_auto_start_button.setFixedSize(150, 25)
        self.save_config_button.setFixedSize(150, 25)

        if self.__file_operate.read_config()['boot_auto_start_button']:
            self.boot_auto_start_button.setChecked(True)
        if self.__file_operate.read_config()['save_config_button']:
            self.save_config_button.setChecked(True)

        # 绑定信号
        self.run_and_stop_btn.clicked.connect(self.__run_and_stop_signal)
        add_button.clicked.connect(self.__add_signal)
        rm_button.clicked.connect(self.__rm_signal)
        self.boot_auto_start_button.stateChanged.connect(self.__boot_auto_start_signal)
        self.save_config_button.stateChanged.connect(self.__save_config_signal)

        # 添加到控件
        layout.addWidget(self.run_and_stop_btn, 0, 0, 2, 1)
        layout.addWidget(add_button, 0, 1, 2, 1)
        layout.addWidget(rm_button, 0, 2, 2, 1)
        layout.addWidget(self.boot_auto_start_button, 0, 3, 1, 1)
        layout.addWidget(self.save_config_button, 1, 3, 1, 1)

        return layout

    def setup_bottom(self):
        """设置底部"""
        layout = QGridLayout()

        self.table_widget = QTableWidget()

        # 设置列数和列宽
        self.table_widget.setColumnCount(3)
        self.table_widget.setColumnWidth(0, 100)
        self.table_widget.setColumnWidth(1, 359)
        self.table_widget.setColumnWidth(2, 100)

        # 　设置表头标签
        self.table_widget.setHorizontalHeaderLabels(["名称", "路径", "启动参数"])

        # 禁止修改和选中整行以及隐藏行号,隐藏虚线框
        self.table_widget.setEditTriggers(QAbstractItemView.NoEditTriggers)
        self.table_widget.setSelectionBehavior(QAbstractItemView.SelectRows)
        self.table_widget.setSelectionMode(QAbstractItemView.SingleSelection)
        self.table_widget.verticalHeader().setVisible(False)

        # 创建项
        config = self.__file_operate.read_config()["config_list"]
        len_config = len(config)
        for i, num in zip(config, range(len_config)):
            self.table_widget.setRowCount(len_config)
            self.table_widget.setItem(num, 0, QTableWidgetItem(i["name"]))
            self.table_widget.setItem(num, 1, QTableWidgetItem(i["path"]))
            self.table_widget.setItem(num, 2, QTableWidgetItem(i["parameter"]))

        # 添加到控件
        layout.addWidget(self.table_widget, 0, 0, 1, 1)

        return layout

    def __run_and_stop_signal(self):
        """启动和停止按钮槽函数"""
        file_path = self.__file_operate.read_config()["config_list"]
        file_parameter = self.__file_operate.read_config()["config_list"]
        self.start_thread_list = []
        if self.run_and_stop_btn.text() == "启动":
            self.run_and_stop_btn.setText("停止")
            for path, parameter in zip(file_path, file_parameter):
                # 循环创建子进程
                self.start_thread = StartThread(path['path'], parameter['parameter'])
                self.start_thread_list.append(self.start_thread)
                self.start_thread.start()
        else:
            self.run_and_stop_btn.setText("正在停止")
            for i in self.start_thread_list:
                i.signal = False
            self.run_and_stop_btn.setText("启动")

    def __add_signal(self):
        """添加按钮的槽函数"""
        # 文件路径
        file_path = QFileDialog().getOpenFileName(self, "选择文件", "", "Executable Files (*.exe)")
        # 启动参数
        parameter, ok = QInputDialog.getText(self, "输入启动参数", "请输入启动参数(没有请留空)")
        if not file_path[0]:
            # 如果没有选择文件，则退出
            return

        # 添加到列表
        self.table_widget.insertRow(self.table_widget.rowCount())  # 添加行
        self.table_widget.setItem(self.table_widget.rowCount() - 1, 0, QTableWidgetItem(Path(file_path[0]).name))
        self.table_widget.setItem(self.table_widget.rowCount() - 1, 1, QTableWidgetItem(file_path[0]))
        self.table_widget.setItem(self.table_widget.rowCount() - 1, 2, QTableWidgetItem(parameter))

        # 禁止修改
        self.table_widget.setEditTriggers(QAbstractItemView.NoEditTriggers)

        # 保存到文件
        if not self.__file_operate.read_config()['save_config_button']:
            # 如果没有保存配置，则退出
            pass
        else:
            self.__file_operate.append_config(
                {
                    "name": Path(file_path[0]).name,
                    "path": file_path[0],
                    "parameter": parameter
                }
            )

    def __rm_signal(self):
        """移除按钮的槽函数"""
        # 获取选中的行
        row = self.table_widget.currentRow()
        if row == -1:
            # 如果没有选中行，则退出
            return
        # 删除选中行
        selected_rows = self.table_widget.selectionModel().selectedRows()
        for row in selected_rows:
            self.table_widget.removeRow(row.row())
            self.__file_operate.remove_config(row.row())

    def __boot_auto_start_signal(self):
        """开机自启动按钮槽函数"""
        path = r"Software\Microsoft\Windows\CurrentVersion\Run"
        if self.boot_auto_start_button.isChecked():
            # 修改配置文件
            item = self.__file_operate.read_config()
            item["boot_auto_start_button"] = True
            self.__file_operate.write_config(item)
            # 设置开机自启动
            key = winreg.OpenKey(winreg.HKEY_CURRENT_USER, path, 0, winreg.KEY_WRITE)
            winreg.SetValueEx(key, "Auto Restart", 0, winreg.REG_SZ, str(Path(__file__).resolve().parent))
            winreg.CloseKey(key)
        else:
            # 修改配置文件
            item = self.__file_operate.read_config()
            item["boot_auto_start_button"] = False
            self.__file_operate.write_config(item)
            try:
                # 取消设置开机自启动
                key = winreg.OpenKey(winreg.HKEY_CURRENT_USER, path, 0, winreg.KEY_WRITE)
                winreg.DeleteValue(key, "Auto Restart")
                winreg.CloseKey(key)
            except WindowsError:
                pass

    def __save_config_signal(self):
        """保存配置按钮槽函数"""
        item = self.__file_operate.read_config()
        if self.save_config_button.isChecked():
            # 修改配置文件
            item["save_config_button"] = True
            self.__file_operate.write_config(item)
        else:
            # 修改配置文件
            item["save_config_button"] = False
            self.__file_operate.write_config(item)
