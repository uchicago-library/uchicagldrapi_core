from random import choice
from string import digits, ascii_letters
from sys import argv, stderr, stdout

try:
    num = argv[1]
    for x in num:
        assert(x in digits)
    num = int(num)
    assert(isinstance(num, int))
except:
    stderr.write("This script takes a single int argument - the length of " +
                 "the secret key.\n")

choices = digits+ascii_letters

key = []

for x in range(num):
    key.append(choice(choices))

stdout.write("".join(key)+"\n")
