# -*- coding: utf-8 -*-
# @Time : 2021/7/17 22:31
# @Author : liyusheng
# @File : conftest.py
import sys
import os

# 应对明明导入模块没问题，却提示No Module Name ****（导入模块的父文件夹），必须放在import之前
current_directory = os.path.dirname(os.path.abspath(__file__))
rootPath = os.path.split(current_directory)[0]
sys.path.append(rootPath)
import pytest
from common.my_log import MyLog
from common import project_path, do_excel

# print(current_directory)
# print(rootPath)
# print(sys.path)
my_log = MyLog()


@pytest.fixture()
def login_set_up():
    t = do_excel.DoExcel(project_path.case_path, "login")

    # my_log.info("开始执行新一条测试用例")
    yield t
    my_log.info("一条测试用例执行完毕")


@pytest.fixture()
def register_setup():
    t = do_excel.DoExcel(project_path.case_path, 'register')
    yield t
    my_log.info("一条测试用例执行完毕")


@pytest.fixture()
def recharge_setup():
    t = do_excel.DoExcel(project_path.case_path, "recharge")
    yield t
    my_log.info("一条测试用例执行完毕")


@pytest.fixture()
def invest_setup():
    t = do_excel.DoExcel(project_path.case_path, "invest")
    yield t
    my_log.info("一条测试用例执行完毕")


@pytest.fixture()
def add_loan_setup():
    t = do_excel.DoExcel(project_path.case_path, "add_loan")
    yield t
    my_log.info("一条测试用例执行完毕")
