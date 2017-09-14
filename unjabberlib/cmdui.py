import cmd
from itertools import zip_longest

INDENT = 5 * ' '


class UnjabberCmd(cmd.Cmd):
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
        sub_print_message(INDENT, message.what)
    else:
        sub_print_message(hour if hour else INDENT, message.what)


def sub_print_message(hour, what):
    for h, line in zip_longest([hour], what.split('\n'), fillvalue=INDENT):
        print(h, line)
