import cmd
from functools import partial

from unjabberlib import formatters

trim_print = partial(print, sep='', end='')


class StdoutFormatter(formatters.Formatter):
    def append(self, text, format=None):
        if format is None or format == formatters.HOUR:
            trim_print(text)
        elif format == formatters.NAME:
            trim_print(' --  ', text)
        elif format == formatters.DAY:
            trim_print('== ', text, ' ==')


class UnjabberCmd(cmd.Cmd):
    def __init__(self, queries, **cmdargs):
        super().__init__(**cmdargs)
        self.formatter = StdoutFormatter()
        self.queries = queries

    def do_who(self, arg):
        """Show list of people. Add part of a name to narrow down."""
        for name in self.queries.who(arg):
            print(name)

    def do_show(self, arg):
        """Show conversations with people matching name (or part of)."""
        previous = None
        for message in self.queries.messages_for_whom(arg):
            day, hour, shortname = message.after(previous)
            self.formatter.show(previous, day, hour, shortname, message.what)
            previous = message

    def do_grep(self, arg):
        """Show messages containing text."""
        for message in self.queries.grep(arg):
            print(message)

    def do_quit(self, arg):
        """Exit the program."""
        return True
