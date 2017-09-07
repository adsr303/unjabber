#!/usr/bin/env python3

import argparse
import cmd
from contextlib import closing
from datetime import datetime
from html.parser import HTMLParser
import io
import sqlite3
import sys


class PayloadParser(HTMLParser):
    def __init__(self):
        super().__init__()
        self.stream = io.StringIO()

    def error(self, message):
        print(message, file=sys.stderr)

    def handle_starttag(self, tag, attrs):
        if tag == 'img':
            self.stream.write(dict(attrs)['title'])

    def handle_data(self, data):
        self.stream.write(data)

    @property
    def text(self):
        return self.stream.getvalue()


def parse_payload(payload):
    p = PayloadParser()
    p.feed(payload)
    p.close()
    return p.text


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
SELECT payload, date, sender FROM history_message
WHERE item IN (SELECT item FROM history_participant WHERE jid LIKE ?)
ORDER BY id
"""


class Unjabber(cmd.Cmd):
    def __init__(self, dbconnection, **cmdargs):
        super().__init__(**cmdargs)
        self.connection = dbconnection

    def do_who(self, arg):
        """Show list of people. Add part of a name to narrow down."""
        query = (PEOPLE_LIKE, (like_arg(arg),)) if arg else (PEOPLE,)
        with self.cursor() as cur:
            cur.execute(*query)
            for row in cur:
                print(row[0])

    def do_show(self, arg):
        """Show conversations with people matching name (or part of)."""
        with self.cursor() as cur:
            cur.execute(MESSAGES, (like_arg(arg),))
            for what, when, who in cur:
                print(datetime.fromtimestamp(when//1_000_000), who,
                      parse_payload(what))

    def do_quit(self, arg):
        """Exit the program."""
        return True

    def cursor(self):
        return closing(self.connection.cursor())


def like_arg(arg):
    return '%{}%'.format(arg)


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
