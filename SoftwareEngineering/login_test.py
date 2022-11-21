from tkinter import Widget
import unittest
import login


class Login_test(unittest.TestCase):
    def __init__(self, methodName, username, password, ex) -> None:
        super().__init__(methodName)
        self.username = username
        self.password = password
        # expectation -> msg
        self.ex = ex

    def test_login(self):
        result = login.login_check(self.username, self.password)
        expected = result['msg']

        try:
            self.assertEqual(expected, self.ex)
        except AssertionError as e:
            print("该用例未通过")
            result = '不通过'
            raise e
        else:
            print("该用例通过")
            result = '通过'


if __name__ == "__main__":
    test_case1 = Login_test(username='admin', password='123456', ex='登录成功', methodName='test_login')
    print('实例初始化成功')
    test_case1.run()