from functools import partial
from tkinter import *
from tkinter.scrolledtext import ScrolledText

INDENT = 5 * ' '


class UnjabberTk(Tk):
    def __init__(self, queries, *args, title=None, **kwargs):
        super().__init__(*args, **kwargs)
        self.title(title)
        self.queries = queries
        self.who_var = StringVar(self)
        self.who_var.trace_add('write', lambda *_: self.who())
        w = OptionMenu(self, self.who_var, *self.queries.who(None))
        w.pack()
        self.text = ScrolledText(self)
        self.text.pack(expand=True, fill=BOTH)

    def who(self):
        self.text.delete('1.0', END)
        self.text.tag_configure('day', foreground='red', justify='center')
        self.text.tag_configure('hour', foreground='blue')
        self.text.tag_configure('shortname', foreground='green')
        append = partial(self.text.insert, END)
        previous = None
        for message in self.queries.messages_for_whom(self.who_var.get()):
            day, hour, shortname = message.after(previous)
            if day:
                if previous:
                    append('\n')
                append(day, 'day')
                append('\n')
            if hour:
                append(hour, 'hour')
            else:
                append(INDENT)
            append(' ')
            if shortname:
                append(shortname, 'shortname')
                append('\n')
                append(INDENT)
                append(' ')
            append(message.what)
            append('\n')
            previous = message
