import io
import unittest
from unjabberlib.formatters import *


class PlainBufferFormatter(Formatter):
    def __init__(self, buffer):
        super().__init__()
        self.buffer = buffer

    def append(self, text, tag=None):
        self.buffer.write(text)


class TestPlainBufferFormatter(unittest.TestCase):
    def setUp(self):
        self.buffer = io.StringIO()
        self.formatter = PlainBufferFormatter(self.buffer)

    def value(self):
        return self.buffer.getvalue()

    def test_show(self):
        self.formatter.show(False, None, None, None, 'something something')
        self.assertEqual(self.value(), '      something something\n')

    def test_show_with_hour(self):
        self.formatter.show(False, None, '10:01', None, 'something something')
        self.assertEqual(self.value(), '10:01 something something\n')

    def test_show_with_hour_name(self):
        self.formatter.show(False, None, '10:01', 'somebody', 'foo bar blah')
        self.assertEqual(self.value(), '\n10:01 somebody\n      foo bar blah\n')

    def test_show_with_day_hour_name(self):
        self.formatter.show(False, '2017-10-22', '10:01', 'somebody',
                            'foo bar blah')
        self.assertEqual(self.value(),
                         '2017-10-22\n10:01 somebody\n      foo bar blah\n')

    def test_show_with_previous(self):
        self.formatter.show(object(), '2017-10-22', '10:01', 'somebody',
                            'foo bar blah')
        self.assertEqual(self.value(),
                         '\n2017-10-22\n10:01 somebody\n      foo bar blah\n')

    def test_multiline_with_hour(self):
        self.formatter.show_multiline('12:34', 'abc\ndef')
        self.assertEqual(self.value(), '12:34 abc\n      def\n')

    def test_multiline_without_hour(self):
        self.formatter.show_multiline(None, 'abc\ndef')
        self.assertEqual(self.value(), '      abc\n      def\n')

    def test_println_string(self):
        self.formatter.println('abc')
        self.assertEqual(self.value(), 'abc\n')

    def test_println_strings(self):
        self.formatter.println('abc', 'xyz')
        self.assertEqual(self.value(), 'abc xyz\n')

    def test_println_format(self):
        self.formatter.println(('jkl', DAY))
        self.assertEqual(self.value(), 'jkl\n')
