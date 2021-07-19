import json

import pytest

from common import project_path, do_excel, my_log
from common.http_request import HttpRequest
from ddt import ddt
from common import get_data
from common.get_data import GetData
from common.do_pymysql import DoMysql

test_data = do_excel.DoExcel(project_path.case_path, "recharge").read_case("RechargeCase")
my_log = my_log.MyLog()


@ddt
class TestCase:

    @pytest.mark.all
    @pytest.mark.recharge
    @pytest.mark.parametrize("case", test_data)
    def test_recharge(self, case, recharge_setup):
        t = recharge_setup
        method = case["Method"]
        url = case["Url"]
        param = eval(get_data.re_p(case["Params"]))
        my_log.info('-------正在测试{}模块里面第{}条测试用例：{}'.format(case['Module'], case['CaseId'], case['Title']))
        my_log.info('测试数据是：{}'.format(case))

        if case["sql"] is not None:
            sql = eval(case["sql"])["sql"]
            before_amount = DoMysql().do_mysql(sql, 1)[0]

        res = HttpRequest().http_request(method, url, param, getattr(GetData, "COOKIES"))
        if res.cookies:
            setattr(GetData, "COOKIES", res.cookies)

        if case["sql"] is not None:
            sql = eval(case["sql"])["sql"]
            after_amount = DoMysql().do_mysql(sql, 1)[0]
            recharge_amount = int(param["amount"])
            expect_amount = before_amount + recharge_amount
            assert(expect_amount == after_amount)

        if case["ExpectedResult"].find("exp_amount") > -1:
            # case["ExpectedResult"].replace("exp_amount", str(expect_amount)) #错了
            case['ExpectedResult'] = case['ExpectedResult'].replace('exp_amount', str(expect_amount))
        try:
            assert(json.loads(case["ExpectedResult"]) == res.json())
            TestResult = "Pass"
        except AssertionError as e:
            TestResult = "Failed"
            raise e
        finally:
            t.write_back(case["CaseId"] + 1, 9, res.text)
            t.write_back(case["CaseId"] + 1, 10, TestResult)
        my_log.info('实际结果是:{}'.format(res.json()))


if __name__ == '__main__':
    pytest.main(["-m recharge", "--html=test_result/test_report/report.html"])
