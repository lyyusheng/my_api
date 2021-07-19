import json

import pytest

from common import project_path, do_excel, my_log
from common.http_request import HttpRequest
from ddt import ddt
from common import get_data
from common.get_data import GetData
from common.do_pymysql import DoMysql

test_data = do_excel.DoExcel(project_path.case_path, "invest").read_case("InvestCase")
my_log = my_log.MyLog()


@ddt
class TestCase:

    @pytest.mark.all
    @pytest.mark.invest
    @pytest.mark.parametrize("case", test_data)
    def test_invest(self, case, invest_setup):
        t = invest_setup
        method = case["Method"]
        url = case["Url"]
        param = eval(get_data.re_p(case["Params"]))
        my_log.info('-------正在测试{}模块里面第{}条测试用例：{}'.format(case['Module'], case['CaseId'], case['Title']))
        my_log.info('测试数据是：{}'.format(case))

        if case["sql"] is not None:
            sql = eval(case["sql"])["sql"]
            before_amount = DoMysql().do_mysql(sql, 1)[0]
            invest_amount = int(param["amount"])

        res = HttpRequest().http_request(method, url, param, cookies=getattr(GetData, "COOKIES"))
        if res.cookies:
            setattr(GetData, "COOKIES", res.cookies)

        if case["sql"] is not None:
            sql = eval(case["sql"])["sql"]
            after_amount = DoMysql().do_mysql(sql, 1)[0]
            expect_amount = before_amount - invest_amount
            assert (after_amount == expect_amount)

        try:
            assert (json.loads(case["ExpectedResult"]) == res.json())
            # self.assertEqual(eval(case["ExpectedResult"]), res.json())
            test_result = "Pass"
        except AssertionError as e:
            test_result = "Failed"
            my_log.error("http请求出错了，错误是{}".format(e))
            raise e
        finally:
            t.write_back(case["CaseId"] + 1, 9, res.text)
            t.write_back(case["CaseId"] + 1, 10, test_result)


# 报错json.decoder.JSONDecodeError: Expecting property name enclosed in double quotes: line 1 column 2 (char 1)
# 原因：json.loads() ，Excel的数据必须用双引号，不能用单引号


if __name__ == '__main__':
    pytest.main(["-m invest", "--html=test_result/test_report/report.html"])
