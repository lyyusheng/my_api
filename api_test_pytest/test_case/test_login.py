import json
import pytest
from common import project_path, do_excel, my_log
from common.http_request import HttpRequest
from ddt import ddt

my_log = my_log.MyLog()

test_data = do_excel.DoExcel(project_path.case_path, "login").read_case("LoginCase")
print(test_data)


@pytest.mark.m
@ddt
class TestCase:

    @pytest.mark.all
    @pytest.mark.parametrize("case", test_data)
    def test_login(self, case, login_set_up):
        t = login_set_up
        method = case['Method']
        url = case['Url']
        param = eval(case['Params'])
        my_log.info('-----正在测试{}模块里面第{}条测试用例：{},'.format(case['Module'], case['CaseId'], case['Title']))
        my_log.info("测试数据是：{}".format(param))
        res = HttpRequest().http_request(method, url, param, cookies=None)
        try:
            # self.assertEqual(case["ExpectedResult"], res.json())
            # self.assertEqual(json.loads(case["ExpectedResult"]), res.json())    # 用了json.loads()包括Excel都不要用单引号，全部用双引号
            assert(json.loads(case["ExpectedResult"]) == res.json())
            test_result = "Pass"
        except Exception as e:
            my_log.error("http请求出错了，错误是：{}".format(e))
            test_result = "Failed"
            raise e  # 抛出错误，否则测试报告那里全部都是通过
        finally:
            t.write_back(case["CaseId"] + 1, 9, res.text)
            t.write_back(case["CaseId"] + 1, 10, test_result)
        my_log.info('实际结果是:{}'.format(res.json()))


# 出现Empty suite，一条用例都没有执行。原因是：函数名没有以test_开头，没识别出来

# 报错 json.decoder.JSONDecodeError: Expecting value: line 1 column 40 (char 39)。
# 原因：Excel中ExpectedResult的null写成None，如果双引号写成单引号也会

if __name__ == '__main__':
    pytest.main(["-m m", "--html=test_result/test_report/report.html"])
