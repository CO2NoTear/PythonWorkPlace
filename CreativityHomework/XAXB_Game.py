import random

def getinput() -> list:
    rawlist = list(input())     # in rawlist, items are char like '1' '3'...
    intlist = []
    for item in rawlist:
        if not item.isnumeric():
            print('Error input! Input a num xxxx, plz!\n')
            return getinput()
        intlist.append(int(item))   #convert char into int
    return intlist

print('''
    The number you have to guess is xxxx, 
    everytime you guess a number, the process will return a sequence
    xAyB, which represents in your answer, 'x' num(s) is(are) right both its val and position,
    while 'y' num(s) is(are) at a wrong position with a right val.
    JUST TRY GUESS THE FINAL ANSWER!
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
        