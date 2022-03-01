_1st = 0
_2nd = 1
new = 0
for count in range(1,30):
    print(_1st,',')
    new = _1st + _2nd
    _1st = _2nd
    _2nd = new
print(_1st,',',_2nd)