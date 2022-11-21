from login_test import Login_test
from unittest import TestSuite, TestResult

suite = TestSuite()

suite.addTest(Login_test('test_login','admin','123456','登录成功'))
suite.addTest(Login_test('test_login','admin','1234567','账号密码不正确'))
suite.addTest(Login_test('test_login','admin','1234','密码长度在6-18之间'))
suite.addTest(Login_test('test_login','admin','12345678910123123624','密码长度在6-18之间'))
suite.addTest(Login_test('test_login','administrator','123456','账号密码不正确'))
#print('suite add, successfully')
result = TestResult()
suite.run(result)