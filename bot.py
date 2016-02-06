#!/usr/bin/env python2.7
import sys
from config import mysql_credentials as login
from config import bearer

import MySQLdb as mdb
import requests


class Connection:

    def __init__(self):
        self.login = login
        self.con = mdb.connect(
            self.login[0], self.login[1], self.login[2], self.login[3])

    def get_message(self):
        with self.con:
            cur = self.con.cursor()
            cur.execute("""
                SELECT id, time, message FROM messages WHERE uploaded = 0 LIMIT 1
            """)
            message = cur.fetchone()
            cur.close()
            return message

    def upload_message(self, message, day):
        url = "https://api.wit.ai/message"
        params = {
            "v": day, "q": message
        }
        headers = {
            "Authorization": "Bearer " + bearer
        }
        resp = requests.post(url=url, params=params, headers=headers)
        data = resp.content
        print data
        return data

    def mark_as_uploaded(self, message_id):
        with self.con:
            cur = self.con.cursor()
            cur.execute("""
                UPDATE messages SET uploaded = 1 WHERE id = %s
            """, [message_id])
            cur.close()


if __name__ == "__main__":
    connect = Connection()
    while True:
        data = connect.get_message()
        if data is None:
            sys.exit()
        message_id = data[0]
        day = data[1].strftime("%Y%m%d")  # "20160205"
        message = data[2]
        connect.upload_message(message, day)
        connect.mark_as_uploaded(message_id)
        print message_id, day, message
