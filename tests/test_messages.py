import unittest
from datetime import datetime

from unjabberlib.messages import Message


class TestMessage(unittest.TestCase):
    def test_properties(self):
        d = datetime(2017, 9, 5, 14, 32, 16, 14230)
        m = Message(d, 'johnny.b.goode@rocknroll.com', 'some payload')
        self.assertEqual(m.day, '2017-09-05')
        self.assertEqual(m.hour, '14:32')
        self.assertEqual(m.shortname, 'johnny.b.goode')

    def test_after_same_user_other_day(self):
        m1 = Message(datetime(2017, 9, 4, 12, 1), 'chuck.berry@guitar.info',
                     'Sing la la la')
        m2 = Message(datetime(2017, 9, 6, 9, 12), 'chuck.berry@guitar.info',
                     'Play more')
        self.assertEqual(m2.after(m1), ('2017-09-06', '09:12', 'chuck.berry'))

    def test_after_same_user_same_day(self):
        m1 = Message(datetime(2017, 9, 4, 12, 1), 'chuck.berry@guitar.info',
                     'Sing la la la')
        m2 = Message(datetime(2017, 9, 4, 12, 3), 'chuck.berry@guitar.info',
                     'Play more')
        self.assertEqual(m2.after(m1), (None, '12:03', None))

    def test_after_same_user_same_hour(self):
        m1 = Message(datetime(2017, 9, 4, 12, 1), 'chuck.berry@guitar.info',
                     'Sing la la la')
        m2 = Message(datetime(2017, 9, 4, 12, 1), 'chuck.berry@guitar.info',
                     'Play more')
        self.assertEqual(m2.after(m1), (None, None, None))

    def test_after_different_user_other_day(self):
        m1 = Message(datetime(2017, 9, 4, 12, 1), 'chuck.berry@guitar.info',
                     'Sing la la la')
        m2 = Message(datetime(2017, 9, 6, 9, 12),
                     'johnny.b.goode@rocknroll.com', 'Play more')
        self.assertEqual(m2.after(m1),
                         ('2017-09-06', '09:12', 'johnny.b.goode'))

    def test_after_different_user_same_day(self):
        m1 = Message(datetime(2017, 9, 4, 12, 1), 'chuck.berry@guitar.info',
                     'Sing la la la')
        m2 = Message(datetime(2017, 9, 4, 12, 3),
                     'johnny.b.goode@rocknroll.com', 'Play more')
        self.assertEqual(m2.after(m1), (None, '12:03', 'johnny.b.goode'))

    def test_after_different_user_same_hour(self):
        m1 = Message(datetime(2017, 9, 4, 12, 1), 'chuck.berry@guitar.info',
                     'Sing la la la')
        m2 = Message(datetime(2017, 9, 4, 12, 1),
                     'johnny.b.goode@rocknroll.com', 'Play more')
        self.assertEqual(m2.after(m1), (None, '12:01', 'johnny.b.goode'))

    def test_after_none(self):
        m2 = Message(datetime(2017, 9, 4, 12, 1),
                     'johnny.b.goode@rocknroll.com', 'Play more')
        self.assertEqual(m2.after(None),
                         ('2017-09-04', '12:01', 'johnny.b.goode'))
