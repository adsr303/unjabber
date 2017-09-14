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
        self.text.tag_configure('day', foreground='red')
        self.text.tag_configure('hour', foreground='blue')
        self.text.tag_configure('shortname', foreground='green')
        previous = None
        for message in self.queries.messages_for_whom(self.who_var.get()):
            day, hour, shortname = message.after(previous)
            if day:
                if previous:
                    self.text.insert(END, '\n')
                self.text.insert(END, day, 'day')
                self.text.insert(END, '\n')
            if hour:
                self.text.insert(END, hour, 'hour')
            else:
                self.text.insert(END, INDENT)
            self.text.insert(END, ' ')
            if shortname:
                self.text.insert(END, shortname, 'shortname')
                self.text.insert(END, '\n')
                self.text.insert(END, INDENT)
                self.text.insert(END, ' ')
            self.text.insert(END, message.what)
            self.text.insert(END, '\n')
            previous = message
