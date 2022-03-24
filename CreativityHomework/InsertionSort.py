from os import sep
import random
import time

# A random list of numbers, which contains uncertain numbers of number. :)
num = random.sample(range(1,1000007),100000)

st = time.time()
lenth_of_num = len(num)
# From the second to the last
for i in range(1,lenth_of_num):
    key = num[i]
    num.pop(i)
    #To insert key to the right position
    j = i-1    #i-1 represents the rare of the sorted sequence
    while j >= 0 and num[j] > key:
        j -= 1
    num.insert(j+1,key)
print(*num,sep=',')
# for item in num:
#     print(item,end=' ')
ed = time.time()
print('cost time: ',ed-st)
