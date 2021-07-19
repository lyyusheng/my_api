import json

from common.do_excel import DoExcel
from common import project_path
from common.http_request import HttpRequest
from common.my_log import MyLog
from ddt import ddt
import pytest

# test_data = DoExcel(case_path, "register").read_case("CASE")
test_data = DoExcel(project_path.case_path, "register").read_case('RegisterCase')
my_log = MyLog()


@ddt
class TestCase:

    @pytest.mark.register
    @pytest.mark.all
    @pytest.mark.parametrize("case", test_data)
    def test_register(self, case, register_setup):
        t = register_setup
        method = case['Method']
        url = case['Url']
        param = eval(case['Params'])  # 讀出來是個字符串，必須eval()變回原來字典類型
        my_log.info('-----正在测试{}模块里面第{}条测试用例：{},'.format(case['Module'], case['CaseId'], case['Title']))
        my_log.info('测试数据是：{}'.format(case['Params']))
        res = HttpRequest().http_request(method, url, param, cookies=None)
        try:
            # self.assertEqual(case["ExpectedResult"], res.text)
            assert (json.loads(case["ExpectedResult"]) == res.json())
            test_result = "Pass"
        except Exception as e:
            my_log.error("http请求出错了，错误是：{}".format(e))
            test_result = "Failed"
            raise e  # 抛出错误，否则测试报告那里全部都是通过
        finally:
            t.write_back(case['CaseId'] + 1, 9, res.text)  # 写回实际结果字符串类型不能用json，参数：行 列 实际结果
            t.write_back(case['CaseId'] + 1, 10, test_result)
        my_log.info('实际结果是:{}'.format(res.json()))


# param = eval(case['Params'])一直报错KeyError:'Parmas',原因是Excel中的Resgister模块的Params写成了Parmas,改回来之后还是错，原因是
# do_excel模块的Params也写成了Parmas

if __name__ == '__main__':
    pytest.main(["-m register", "--html=test_result/test_report/report.html"])
