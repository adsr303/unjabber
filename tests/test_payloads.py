import unittest

from unjabberlib.payloads import parse_payload

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
