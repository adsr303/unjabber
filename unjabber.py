#!/usr/bin/env python3

import argparse
import cmd
import sqlite3
from itertools import zip_longest

from unjabberlib.queries import Queries


class Unjabber(cmd.Cmd):
    def __init__(self, queries, **cmdargs):
        super().__init__(**cmdargs)
        self.queries = queries

    def do_who(self, arg):
        """Show list of people. Add part of a name to narrow down."""
        for name in self.queries.who(arg):
            print(name)

    def do_show(self, arg):
        """Show conversations with people matching name (or part of)."""
        previous = None
        for message in self.queries.messages_for_whom(arg):
            print_message(previous, message)
            previous = message

    def do_grep(self, arg):
        """Show messages containing text."""
        for message in self.queries.grep(arg):
            print(message)

    def do_quit(self, arg):
        """Exit the program."""
        return True


def print_message(previous, message):
    day, hour, shortname = message.after(previous)
    if day:
        if previous:
            print()
        print('==', day, '==')
    if shortname:
        if not day:
            print()
        print(hour, ' -- ', shortname)
        sub_print_message(5 * ' ', message.what)
    else:
        sub_print_message(hour if hour else 5 * ' ', message.what)


def sub_print_message(hour, what):
    for h, line in zip_longest([hour], what.split('\n'), fillvalue=5 * ' '):
        print(h, line)


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Read Cisco Jabber database')
    parser.add_argument('database', help='the database file')
    args = parser.parse_args()

    with sqlite3.connect(args.database) as con:
        Unjabber(Queries(con)).cmdloop()
