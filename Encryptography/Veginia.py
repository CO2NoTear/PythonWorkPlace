cipher = "vemaildytophtcpystnqzahj"
key = list('aef')
dictionary = {}
for i in range(26):
    dictionary[chr(i+97)] = i
key_arr = []
for k in key:
    key_arr.append(dictionary[k])
cipher_arr = []
for char in cipher:
    cipher_arr.append(dictionary[char])
back_replace = {0:2, 1:4, 2:0, 3:1, 4:3, 5:5}
message = []
for i in range(len(cipher_arr)):
    cipher_arr[i] -= key_arr[i%3]
    cipher_arr[i] %= 26
    message.append(chr(cipher_arr[i]+97))
print("".join(message))
for i in range(4):
    message[i*6+2], message[i*6+0] = message[i*6+0], message[i*6+2]
    message[i*6+4], message[i*6+1], message[i*6+3] = message[i*6+1], message[i*6+3], message[i*6+4]

print(''.join(message))
