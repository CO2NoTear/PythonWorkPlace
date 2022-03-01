""" 
1, 8, 27, 64
  7, 19, 37
    12, 18
      6
"""


origin = 1
_1st_diffence = 7
_2st_diffence = 12
_3st_diffence = 6 # constant
# origin = origin + _1st_diffence
while origin <1000:
    print(origin)
    origin = origin + _1st_diffence
    _1st_diffence = _2st_diffence + _1st_diffence
    _2st_diffence = _2st_diffence + _3st_diffence
print(origin)