import io
import sys
from html.parser import HTMLParser


class PayloadParser(HTMLParser):
    def __init__(self):
        super().__init__()
        self.stream = io.StringIO()

    def error(self, message):
        print(message, file=sys.stderr)

    def handle_starttag(self, tag, attrs):
        if tag == 'img':
            self.stream.write(dict(attrs)['title'])

    def handle_startendtag(self, tag, attrs):
        if tag == 'br':
            self.stream.write('\n')
        else:
            super().handle_startendtag(tag, attrs)

    def handle_data(self, data):
        self.stream.write(data)

    @property
    def text(self):
        return self.stream.getvalue()


def parse_payload(payload):
    p = PayloadParser()
    p.feed(payload)
    p.close()
    return p.text
