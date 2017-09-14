import io
import unittest
from unjabberlib.formatters import *


class PlainBufferFormatter(Formatter):
    def __init__(self, buffer):
        super().__init__()
        self.buffer = buffer

    def append(self, text, format=None):
        self.buffer.write(text)


class TestPlainFormatter(unittest.TestCase):
    def setUp(self):
        self.buffer = io.StringIO()
        self.formatter = PlainBufferFormatter(self.buffer)

    def test_multiline_with_hour(self):
        self.formatter.show_multiline('12:34', 'abc\ndef')
        self.assertEqual(self.buffer.getvalue(), '12:34 abc\n      def\n')

    def test_multiline_without_hour(self):
        self.formatter.show_multiline(None, 'abc\ndef')
        self.assertEqual(self.buffer.getvalue(), '      abc\n      def\n')
