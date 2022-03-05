from random import randint

n = int(randint(1,100))  # destination
# n = 24
i = -1
print('Which number you wanna guess?\n')
while i != n:
    i = int(input())
    if i < 0:
        print('Error, input a positive number,plz\n')
        continue
    if i < n:
        print('Too Small\n')
    elif i > n: print('Too big\n')
print('Congratulations!')
