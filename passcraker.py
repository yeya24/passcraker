#!/usr/bin/python3
import argparse
from crypt import *
from queue import Queue
from threading import Thread
import sys
from collections import namedtuple

q = Queue(400)
crack = namedtuple('crack', ['secret', 'password'])


def calculate_hash():
    while True:
        c = q.get()
        fields = c.secret.split('*')
        if crypt(c.password, fields[1][:11]) == fields[1]:
            print("Found passwd for user {}: {} ".format(fields[0], c.password))


def main(args):
    words = args.dictionary.readlines()
    pass_lines = args.password.readlines()

    for i in range(100):
        t = Thread(target=calculate_hash)
        t.daemon = True
        t.start()

    try:
        for line in pass_lines:
            columns = str.split(line.strip(), ":", 2)
            if columns[1] != "*":
                for word in words:
                    q.put(crack(secret=columns[0] + "*" + columns[1], password=word.strip()))
        q.join()
    except KeyboardInterrupt:
        sys.exit(1)


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("dictionary", type=argparse.FileType('r'),
                        help="The dictionary file you want to use to crack password")
    parser.add_argument("password", type=argparse.FileType('r'), help="The victim password file")
    args = parser.parse_args()
    main(args)
