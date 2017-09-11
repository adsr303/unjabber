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
        self.text.delete('1.0', END)
        column = 0
        row = 1
        messages = self.queries.messages_for_whom(self.who_var.get())
        for index, message in enumerate(messages):
            when = str(message.when)
            self.text.insert(END, when)
            self.text.insert(END, ' ')
            self.text.insert(END, message.shortname)
            tag_name = 'when{}'.format(index)
            self.text.tag_add(tag_name, position(row, column),
                              position(row, column + len(when)))
            self.text.tag_configure(tag_name, foreground='blue')
            self.text.insert(END, '\n')
            row += 1
            self.text.insert(END, message.what)
            self.text.insert(END, '\n')
            row += 1


def position(row, column):
    return '{}.{}'.format(row, column)
