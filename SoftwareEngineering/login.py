def login_check(username,password):
    '''
    :param username: 登录用户名
    :param password: 登录密码
    :return:
    '''
    if  6<=len(password)<=18:
        if username=='admin' and  password=='123456':
            return {'code':0,'msg':'登录成功'}
        else:
            return {'code':1,'msg':'账号密码不正确'}
    else:
        return {'code':1,'msg':'密码长度在6-18之间'}