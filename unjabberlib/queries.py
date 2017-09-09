from datetime import datetime

from unjabberlib.messages import Message
from unjabberlib.payloads import parse_payload

PEOPLE = """
SELECT jid FROM history_participant
WHERE islocal = 0 AND number = '' AND phonetype = 0
GROUP BY jid
"""

PEOPLE_LIKE = """
SELECT jid FROM history_participant
WHERE islocal = 0 AND number = '' AND phonetype = 0 AND jid LIKE ?
GROUP BY jid
"""

MESSAGES = """
SELECT date, sender, payload FROM history_message
WHERE item IN (SELECT item FROM history_participant WHERE jid LIKE ?)
ORDER BY id
"""

MESSAGES_LIKE = """
SELECT date, sender, payload FROM history_message
WHERE payload MATCH ? ORDER BY id
"""


def like_arg(arg):
    return '%{}%'.format(arg)


def payload_match(text, payload):
    p = parse_payload(payload)
    return text.lower() in p.lower()


def make_message_from_db(when, who, what):
    return Message(datetime.fromtimestamp(when // 1_000_000), who,
                   parse_payload(what))


class Queries:
    def __init__(self, dbconnection):
        self.connection = dbconnection
        self.connection.create_function('match', 2, payload_match)

    def who(self, text):
        query = (PEOPLE_LIKE, (like_arg(text),)) if text else (PEOPLE,)
        for row in self.connection.execute(*query):
            yield row[0]

    def messages_for_whom(self, text):
        for row in self.connection.execute(MESSAGES, (like_arg(text),)):
            yield make_message_from_db(*row)

    def grep(self, text):
        for row in self.connection.execute(MESSAGES_LIKE, (text,)):
            yield make_message_from_db(*row)


# CREATE TABLE history_item(
#     id INTEGER PRIMARY KEY AUTOINCREMENT,
#     calltype INTEGER,
#     mediatype INTEGER,
#     date INTEGER,
#     duration INTEGER,
#     isconf INTEGER,
#     isread INTEGER,
#     isdeleted INTEGER,
#     uid TEXT,
#     protocoltype INTEGER);
#
# CREATE TABLE history_participant(
#     id INTEGER PRIMARY KEY AUTOINCREMENT,
#     islocal INTEGER,
#     contacttype INTEGER,
#     phonetype INTEGER,
#     account TEXT,
#     name TEXT,
#     number TEXT,
#     jid TEXT,
#     item INTEGER,
#     homephone TEXT,
#     businessphone TEXT,
#     mobilephone TEXT,
#     otherphone TEXT,
#     defaultphone TEXT,
#     photouri TEXT,
#     contactresolved INTEGER,
#     huntgroup TEXT,
#     FOREIGN KEY(item) REFERENCES history_item(id) ON DELETE CASCADE);
#
# CREATE TABLE history_message(
#     id INTEGER PRIMARY KEY AUTOINCREMENT,
#     type INTEGER,
#     payload CLOB,
#     date INTEGER,
#     sender TEXT,
#     item INTEGER,
#     label INTEGER,
#     FOREIGN KEY(item) REFERENCES history_item(id) ON DELETE CASCADE,
#     FOREIGN KEY(label) REFERENCES im_label(id) ON DELETE CASCADE);
