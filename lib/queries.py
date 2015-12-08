from lib.connection import get_connection


class Reader:

    def __init__(self):
        self.con = get_connection()

    def chat_channel(self, channel):
        with self.con:
            cur = self.con.cursor()
            cur.execute(
                """SELECT message FROM messages
                    WHERE channel = %s""", [channel])
            messages = cur.fetchall()
            return messages
