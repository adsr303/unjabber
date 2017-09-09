#!/usr/bin/env python3

import argparse
import cmd
import sqlite3
from datetime import datetime
from itertools import zip_longest

from unjabberlib.messages import Message
from unjabberlib.payloads import parse_payload


def make_message_from_db(when, who, what):
    return Message(datetime.fromtimestamp(when // 1_000_000), who,
                   parse_payload(what))


PEOPLE = """
SELECT jid FROM history_participant
WHERE islocal = 0 AND number = '' AND phonetype = 0
GROUP BY jid
"""

PEOPLE_LIKE = """
SELECT jid FROM history_participant
WHERE islocal = 0 AND number = '' AND phonetype = 0 AND jid LIKE ?
GROUP BY jid
"""

MESSAGES = """
SELECT date, sender, payload FROM history_message
WHERE item IN (SELECT item FROM history_participant WHERE jid LIKE ?)
ORDER BY id
"""

MESSAGES_LIKE = """
SELECT date, sender, payload FROM history_message
WHERE payload MATCH ? ORDER BY id
"""


class Unjabber(cmd.Cmd):
    def __init__(self, dbconnection, **cmdargs):
        super().__init__(**cmdargs)
        self.connection = dbconnection
        self.connection.create_function('match', 2, payload_match)

    def do_who(self, arg):
        """Show list of people. Add part of a name to narrow down."""
        query = (PEOPLE_LIKE, (like_arg(arg),)) if arg else (PEOPLE,)
        for row in self.connection.execute(*query):
            print(row[0])

    def do_show(self, arg):
        """Show conversations with people matching name (or part of)."""
        previous = None
        for row in self.connection.execute(MESSAGES, (like_arg(arg),)):
            message = make_message_from_db(*row)
            print_message(previous, message)
            previous = message

    def do_grep(self, arg):
        """Show messages containing text."""
        for row in self.connection.execute(MESSAGES_LIKE, (arg,)):
            print(make_message_from_db(*row))

    def do_quit(self, arg):
        """Exit the program."""
        return True


def like_arg(arg):
    return '%{}%'.format(arg)


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
        sub_print_message(5*' ', message.what)
    else:
        sub_print_message(hour if hour else 5*' ', message.what)


def sub_print_message(hour, what):
    for h, line in zip_longest([hour], what.split('\n'), fillvalue=5*' '):
        print(h, line)


def payload_match(text, payload):
    p = parse_payload(payload)
    return text.lower() in p.lower()


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Read Cisco Jabber database')
    parser.add_argument('database', help='the database file')
    args = parser.parse_args()

    with sqlite3.connect(args.database) as con:
        Unjabber(con).cmdloop()

"""
CREATE TABLE history_item(id INTEGER PRIMARY KEY AUTOINCREMENT,calltype INTEGER,mediatype INTEGER,date INTEGER,duration INTEGER,isconf INTEGER,isread INTEGER,isdeleted INTEGER,uid TEXT,protocoltype INTEGER);
CREATE TABLE history_participant(id INTEGER PRIMARY KEY AUTOINCREMENT,islocal INTEGER,contacttype INTEGER,phonetype INTEGER,account TEXT,name TEXT,number TEXT,jid TEXT,item INTEGER,homephone TEXT,businessphone TEXT,mobilephone TEXT,otherphone TEXT,defaultphone TEXT,photouri TEXT,contactresolved INTEGER,huntgroup TEXT,FOREIGN KEY(item) REFERENCES history_item(id) ON DELETE CASCADE);
CREATE TABLE history_message(id INTEGER PRIMARY KEY AUTOINCREMENT,type INTEGER,payload CLOB,date INTEGER,sender TEXT,item INTEGER,label INTEGER,FOREIGN KEY(item) REFERENCES history_item(id) ON DELETE CASCADE,FOREIGN KEY(label) REFERENCES im_label(id) ON DELETE CASCADE);
"""
