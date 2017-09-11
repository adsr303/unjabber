#!/usr/bin/env python3

import argparse
import sqlite3

from unjabberlib.cmdui import UnjabberCmd
from unjabberlib.queries import Queries

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Read Cisco Jabber database')
    parser.add_argument('database', help='the database file')
    args = parser.parse_args()

    with sqlite3.connect(args.database) as con:
        UnjabberCmd(Queries(con)).cmdloop()
