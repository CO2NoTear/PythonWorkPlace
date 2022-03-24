import random

def getinput() -> list:
    print("You guess it is...\n")
    rawlist = list(input())     # in rawlist, items are char like '1' '3'...
    intlist = []
    for item in rawlist:
        if not item.isnumeric():
            print('Error input! Input a num xxxx, plz!\n')
            return getinput()
        elif int(item) in intlist:
            print("You typed a repeated number! Don't do that!")
            return getinput()
        else:
            intlist.append(int(item))   #convert char into int
    return intlist

print('''
    The number you have to guess is xxxx, without same number.
    everytime you guess a number, the process will return a sequence:
    xAyB, which represents in your answer, 'x' num(s) is(are) right both its val and position,
    while 'y' num(s) is(are) at a wrong position with a right val.
    JUST TRY GUESS THE FINAL ANSWER!
    猜数游戏：输入一个不含重复数字的四位数，程序会给出形如xAyB的返回值，
    其中x代表值、位置都正确的数字个数，y代表值正确，但位置有误的个数。
    尽你所能猜出正确答案吧！
''')
num = random.sample(range(0,9),k=4)
while True:
    inputstr = getinput()
    if len(inputstr) > 4:
        print("your answer is too long! type a num xxxx, plz.\n")
        continue
    # print(inputstr)
    cntA = 0
    cntB = 0
    for item in num[0:4]:   #oops, the latter val isn't in it. 
                            #you just have item to be num[0],[1],[2],[3]
        # print(item,end=' ')       # to debug
        if item in inputstr:
            if inputstr.index(item) == num.index(item):
                cntA += 1
            else: cntB += 1
    if cntA == 4:
        print('Wow! You won!\n')
        break
    else:
        print(cntA,'A',cntB,'B\n',sep='')
        