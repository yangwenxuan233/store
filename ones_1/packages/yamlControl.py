#!/usr/bin/env python
# -*- coding: utf-8 -*-




import yaml.scanner

# TODO:需要根据项目位置修改该参数
fileDir = '/home/weisen/ONES_AutoTest/config.yaml'

def getYamlData() -> dict:
    """
    获取 yaml 中的数据
    :param: fileDir:
    :return:
    """
    data = open(fileDir, 'r', encoding='utf-8')
    res = yaml.load(data, Loader=yaml.FullLoader)
    return res