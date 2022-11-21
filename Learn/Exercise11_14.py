def login_check(username="", password=""):
    if username == "admin":
        length = len(password)
        if length < 4:
            return "password too short"
        elif length > 18:
            return "password too long"
        if password == "1234567":
            return "Login successfully!"
        else:
            return "Login failed: Wrong password!"
    else:
        return "Username not found!"

'''
print('expected: too short')
print('result: ' + login_check(username='admin', password='123')) 
print("expected: too long")
print('result: ' + login_check(username='admin', password='12367812638712378618236')) 
print('expected: Username not found!')
print('result: ' + login_check(username='CO2', password='1234567')) 
print('expected: Login failed: Wrong password!')
print('result: ' + login_check(username='admin', password='adminadmin'))
print('expected: Login successfully!')
print('result: ' + login_check(username='admin', password='1234567'))
'''
print('Username:')
Username = input()
print('Password:')
Password = input()

print(login_check(Username,Password))