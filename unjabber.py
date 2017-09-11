#!/usr/bin/env python3

import argparse
import sqlite3

from unjabberlib.cmdui import UnjabberCmd
from unjabberlib.queries import Queries
from unjabberlib.tkui import UnjabberTk

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Read Cisco Jabber database')
    parser.add_argument('-g', '--graphical', action='store_true',
                        help='launch graphical interface')
    parser.add_argument('database', help='the database file')
    args = parser.parse_args()

    with sqlite3.connect(args.database) as con:
        queries = Queries(con)
        if args.graphical:
            UnjabberTk(queries).mainloop()
        else:
            UnjabberCmd(queries).cmdloop()
