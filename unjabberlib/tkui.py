from tkinter import *
from tkinter.scrolledtext import ScrolledText
from tkinter.ttk import *

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

        top_frame = Frame(self)
        top_frame.pack(fill=X)

        self.who_narrow_var = StringVar(self)
        self.who_narrow_var.trace_add('write', lambda *_: self.narrow_who())
        e = Entry(top_frame, textvariable=self.who_narrow_var)
        e.pack(side=LEFT)

        self.text = ScrolledText(self)
        self.text.pack(expand=True, fill=BOTH)
        self.formatter = ScrolledTextFormatter(self.text)

        self.who_var = StringVar(self)
        self.who_var.trace_add('write', lambda *_: self.who())
        self.who_menu = OptionMenu(top_frame, self.who_var, '',
                                   *self.queries.who(None))
        self.who_menu.pack(side=LEFT)

    def who(self):
        self.text.delete('1.0', END)
        previous = None
        for message in self.queries.messages_for_whom(self.who_var.get()):
            day, hour, name = message.after(previous)
            self.formatter.show(previous, day, hour, name, message.what)
            previous = message

    def narrow_who(self):
        menu = self.who_menu['menu']
        menu.delete(0, END)
        like = self.who_narrow_var.get() or None
        for name in self.queries.who(like):
            menu.add_command(label=name,
                             command=lambda x=name: self.who_var.set(x))
