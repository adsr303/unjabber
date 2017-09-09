class Message:
    def __init__(self, when, who, what):
        self.when = when
        self.who = who
        self.what = what

    def __str__(self):
        return '{} {} {}'.format(self.when, self.who, self.what)

    def __repr__(self):
        return '{}({}, {}, {})'.format(
            self.__class__.__name__,
            *(repr(x) for x in [self.when, self.who, self.what]))

    @property
    def day(self):
        return str(self.when)[:10]

    @property
    def hour(self):
        return str(self.when)[11:16]

    @property
    def shortname(self):
        return self.who[:self.who.find('@')]

    def after(self, other):
        if not other:
            return self.day, self.hour, self.shortname
        day = self.day if self.day != other.day else None
        if self.who == other.who:
            hour = self.hour if self.hour != other.hour else None
            shortname = self.shortname if day else None
        else:
            hour = self.hour
            shortname = self.shortname
        return day, hour, shortname
