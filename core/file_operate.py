#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2023/3/25 10:23
# @Author  : 桥话语权
# @File    : file_operate.py
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
import json
from pathlib import Path


class FileOperate:
    """文件操作"""
    __template = {
        "boot_auto_start_button": False,
        "save_config_button": True,
        "config_list": [

        ]
    }

    def __init__(self):
        self.exe_cfg_path = Path.home() / "Documents/Bridge Club/auto_restart/config.json"
        if not self.exe_cfg_path.exists():
            Path.mkdir(self.exe_cfg_path.parent, exist_ok=True, parents=True)
            with open(self.exe_cfg_path, "w") as f:
                json.dump(self.__template, f, ensure_ascii=False, indent=4)

    def append_config(self, config):
        with open(self.exe_cfg_path, "r") as f:
            config_list: dict = json.load(f)
        config_list['config_list'].append(config)
        with open(self.exe_cfg_path, "w") as f:
            json.dump(config_list, f, ensure_ascii=False, indent=4)

    def read_config(self):
        with open(self.exe_cfg_path, "r") as f:
            config_list: dict = json.load(f)
        return config_list

    def remove_config(self, row):
        with open(self.exe_cfg_path, "r") as f:
            config_list: dict = json.load(f)
        del config_list['config_list'][row]
        with open(self.exe_cfg_path, "w") as f:
            json.dump(config_list, f, ensure_ascii=False, indent=4)

    def write_config(self, config):
        with open(self.exe_cfg_path, "w") as f:
            json.dump(config, f, ensure_ascii=False, indent=4)

