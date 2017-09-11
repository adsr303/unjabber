from tkinter import *


class UnjabberTk(Tk):
    def __init__(self, queries, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.queries = queries
        self.who_var = StringVar(self)
        self.who_var.trace_add('write', lambda *args: self.who())
        w = OptionMenu(self, self.who_var, *self.queries.who(None))
        w.pack()
        self.text = Text(self)
        self.text.pack()

    def who(self):
        self.text.delete(1.0, END)
        for message in self.queries.messages_for_whom(self.who_var.get()):
            self.text.insert(END, str(message))
            self.text.insert(END, '\n')
