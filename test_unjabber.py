import unittest

from datetime import datetime

from unjabber import Message, parse_payload

PAYLOAD = ('<span style="font-family:Segoe UI;color:#1a1a1a;font-size:10pt;'
           'font-weight:normal;font-style:normal;text-decoration:none;"><div>'
           "But he could play the guitar just like a ringin' a bell "
           '<img title=":)" src="file:///C:/Program Files (x86)/Cisco Systems/'
           'Cisco Jabber/Emoticons/smile.png"/></div></span>')


class TestPayloadParser(unittest.TestCase):
    def test_parse_payload(self):
        self.assertEqual(
            parse_payload(PAYLOAD),
            "But he could play the guitar just like a ringin' a bell :)")


class TestMessage(unittest.TestCase):
    def test_properties(self):
        d = datetime(2017, 9, 5, 14, 32, 16, 14230)
        m = Message(d, 'johnny.b.goode@rocknroll.com', 'some payload')
        self.assertEqual(m.day, '2017-09-05')
        self.assertEqual(m.hour, '14:32')
        self.assertEqual(m.shortname, 'johnny.b.goode')


if __name__ == '__main__':
    unittest.main()
