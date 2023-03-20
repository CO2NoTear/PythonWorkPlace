cipher = list("edsgickxhuklzveqzvkxwkzukvcuh")
dictionary = {}
counts = {}
for i in range(26):
    dictionary[chr(i+97)] = i
    counts[chr(i+97)] = cipher.count(chr(i+97))
print(dictionary)
print(counts)
# 3的逆元是9
multi_factor = 3
add_factor = 10
cipher_arr = []
for char in cipher:
    cipher_arr.append(dictionary[char])
print(cipher_arr)
message = []
for char in cipher_arr:
    message.append(chr((char - add_factor)*multi_factor%26 + 97))
print(''.join(message))

