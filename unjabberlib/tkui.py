from tkinter import *
from tkinter.scrolledtext import ScrolledText

from unjabberlib import formatters


class ScrolledTextFormatter(formatters.Formatter):
    def __init__(self, scrolled_text):
        super().__init__()
        self.text = scrolled_text
        self.text.tag_configure(formatters.DAY, foreground='red',
                                justify='center')
        self.text.tag_configure(formatters.HOUR, foreground='blue')
        self.text.tag_configure(formatters.NAME, foreground='green')

    def append(self, text, tag=None):
        self.text.insert(END, text, tag)


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
        self.formatter = ScrolledTextFormatter(self.text)

    def who(self):
        self.text.delete('1.0', END)
        previous = None
        for message in self.queries.messages_for_whom(self.who_var.get()):
            day, hour, name = message.after(previous)
            self.formatter.show(previous, day, hour, name, message.what)
            previous = message
