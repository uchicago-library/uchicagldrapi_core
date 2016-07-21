from random import choice
from string import digits, ascii_letters
from sys import stdout
from argparse import ArgumentParser

def main(num=None, to_stdout=True):
    if num is None:
        parser = ArgumentParser()
        parser.add_argument("num_chars", help="How many characters long the " +
                            "generated private key will be.",
                            type=int, action="store")
        args = parser.parse_args()
        num = args.num_chars
    else:
        if not isinstance(num, int):
            raise ValueError("num must be an int")
    chars = digits+ascii_letters
    key = []
    for x in range(num):
        key.append(choice(chars))
    key_str = "".join(key)
    if to_stdout is True:
        stdout.write(key_str+"\n")
    else:
        return key_str

if __name__ == "__main__":
    main()
