#!/usr/bin/python3
import argparse
from crypt import *
from queue import Queue
from threading import Thread
import time
import sys
from collections import namedtuple

crack = namedtuple('crack', ['user', 'secret', 'password'])


# Worker class for cracking passwords.
class CrackThread(Thread):
    def __init__(self, queue, users, sleep_time):
        Thread.__init__(self, daemon=True)
        self.queue = queue
        self.sleep_time = sleep_time
        self.users = users

    def run(self):
        time.sleep(self.sleep_time)
        while not self.queue.empty():
            c = self.queue.get()
            # Check if we already get the password of this user.
            if not self.users[c.user]:
                if crypt(c.password, c.secret[:11]) == c.secret:
                    self.users[c.user] = True
                    print("Found passwd for user {}: {} ".format(c.user, c.password))
            self.queue.task_done()


def main(arg):
    threads = arg.threads
    words = arg.dictionary.readlines()
    pass_lines = arg.password.readlines()
    q = Queue(arg.queue_size)
    users = {}
    print('Start cracking password file {} with wordlist {}'.format(args.password.name, args.dictionary.name))

    for i in range(threads):
        t = CrackThread(q, users, 0.5)
        t.start()

    try:
        for line in pass_lines:
            columns = str.split(line.strip(), ":", 2)
            if columns[1] != "*":
                for word in words:
                    if columns[0] not in users:
                        users[columns[0]] = False
                    elif users[columns[0]]:
                        continue
                    q.put(crack(user=columns[0], secret=columns[1], password=word.strip()))

        q.join()
        print('Cracking passwords finish')
    except KeyboardInterrupt:
        sys.exit(1)


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("dictionary", type=argparse.FileType('r'),
                        help="The dictionary file you want to use to crack password")
    parser.add_argument("password", type=argparse.FileType('r'), help="The victim password file")
    parser.add_argument("--threads", type=int, default=10, required=False,
                        help="The number of running threads when cracking passwords")
    parser.add_argument("--queue_size", type=int, default=200, required=False,
                        help="The maximum size of the queue")
    args = parser.parse_args()
    main(args)
