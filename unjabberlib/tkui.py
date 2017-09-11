from tkinter import *
from tkinter.scrolledtext import ScrolledText


class UnjabberTk(Tk):
    def __init__(self, queries, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.queries = queries
        self.who_var = StringVar(self)
        self.who_var.trace_add('write', lambda *args: self.who())
        w = OptionMenu(self, self.who_var, *self.queries.who(None))
        w.pack()
        self.text = ScrolledText(self)
        self.text.pack()

    def who(self):
        self.text.delete('1.0', END)
        self.text.tag_configure("when", foreground='blue')
        messages = self.queries.messages_for_whom(self.who_var.get())
        for index, message in enumerate(messages):
            when = str(message.when)
            self.text.insert(END, when, "when")
            self.text.insert(END, ' ')
            self.text.insert(END, message.shortname)
            self.text.insert(END, '\n')
            self.text.insert(END, message.what)
            self.text.insert(END, '\n')
