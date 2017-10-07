import unittest

from unjabberlib.payloads import parse_payload

SMILEY = ('<span style="font-family:Segoe UI;color:#1a1a1a;font-size:10pt;'
          'font-weight:normal;font-style:normal;text-decoration:none;"><div>'
          "But he could play the guitar just like a ringin' a bell "
          '<img title=":)" src="file:///C:/Program Files (x86)/Cisco Systems/'
          'Cisco Jabber/Emoticons/smile.png"/></div></span>')

SCREENGRAB = ('<span style="font-family:Segoe UI;color:#1a1a1a;font-size:10pt;'
              'font-weight:normal;font-style:normal;text-decoration:none;">'
              '<div><div style="overflow-x:auto; overflow-y:hidden;'
              'padding-bottom:1.3em"><img alt="Screen capture" '
              'id="{73DEFD96-9027-456E-B88E-0AFF281C16C5}.png" '
              'name="connect_screen_capture" '
              'src="file:///C:/Users/Angus/Documents/MyJabberFiles/'
              'angus@young.com/{73DEFD96-9027-456E-B88E-0AFF281C16C5}.png"/>'
              '</div></div></span>')


class TestPayloadParser(unittest.TestCase):
    def test_parse_payload_with_emoticon(self):
        self.assertEqual(
            parse_payload(SMILEY),
            "But he could play the guitar just like a ringin' a bell :)")

    def test_parse_payload_with_screengrab(self):
        self.assertEqual(parse_payload(SCREENGRAB),
                         'Screen capture: file:///C:/Users/Angus/Documents/'
                         'MyJabberFiles/angus@young.com/'
                         '{73DEFD96-9027-456E-B88E-0AFF281C16C5}.png')
