# -*- coding: utf-8 -*-
# @Time : 2021/7/18 4:13
# @Author : liyusheng
# @File : run_pytest.py
import pytest

if __name__ == '__main__':
    # pytest.main(["-m all", "--html=test_result/test_report/all_report.html"])
    pytest.main(["-m all ", r"--html=report\test.html", r"--alluredir=report\allure"])