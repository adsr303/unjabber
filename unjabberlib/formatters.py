from itertools import zip_longest

DAY = 'day'
HOUR = 'hour'
NAME = 'name'


class Formatter:
    def __init__(self, indent=5 * ' '):
        self.indent = indent

    def append(self, text, format=None):
        raise NotImplementedError('Must override append() in derived class')

    def println(self, *args):
        sep = None
        for a in args:
            if sep:
                self.append(sep)
            else:
                sep = ' '
            if isinstance(a, str):
                self.append(a)
            else:
                self.append(*a)
        self.append('\n')

    def show(self, previous, day, hour, name, text):
        if day:
            if previous:
                self.println()
            self.println((day, DAY))
        if name:
            if not day:
                self.println()
            self.println((hour, HOUR), (name, NAME))
            self.show_multiline(None, text)
        else:
            self.show_multiline(hour, text)

    def show_multiline(self, hour, text):
        hh = [(hour, HOUR)] if hour else []
        for h, line in zip_longest(hh, text.split('\n'), fillvalue=self.indent):
            self.println(h, line)
