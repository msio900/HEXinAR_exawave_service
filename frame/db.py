# Sqlite3 Connection Setting

import sqlite3

class DB:
    def getcon(self):
        con = sqlite3.connect('db.sqlite3')
        return con

    def close(self, cursor, con):
        if cursor != None:
            cursor.close()
        if con != None:
            con.close()