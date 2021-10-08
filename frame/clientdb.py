# Customer Table 접속
from frame.sql import Sql
from frame.db import DB
from frame.vo import ClientVO


class ClientDB(DB):
    def selectOne(self, pwd, email):
        con  = super().getcon()
        cursor = con.cursor()
        cursor.execute(Sql.selone %(pwd, email))
        c = cursor.fetchone()
        client = ClientVO(c[0], c[1], c[2], c[3], c[4])
        super().close(cursor, con)
        return client

    def selectAll(self):
        custall = []       # 반환할 ClientVO 객체 리스트
        con = super().getcon()
        cursor = con.cursor()
        cursor.execute(Sql.selall)
        cs = cursor.fetchall()
        for c in cs:
            client = ClientVO(c[0], c[1], c[2], c[3], c[4])
            custall.append(client)
        return custall

    def insert(self, pwd, name, email, phone_num):
        con = super().getcon()
        cursor = con.cursor()
        cursor.execute(Sql.insert %(pwd, name, email, phone_num))
        con.commit()
        super().close(cursor, con)

    def update(self, pwd, name, phone_num, email):
        con = super().getcon()
        cursor = con.cursor()
        try:
            cursor.execute(Sql.update %(pwd, name, phone_num, email))
            con.commit()
        except Exception as err:
            con.rollback()
            print('에러:', err)
        finally:
            super().close(cursor, con)

    def delete(self, email):
        con = super().getcon()
        cursor = con.cursor()
        try:
            cursor.execute(Sql.delete %(email))
            con.commit()
        except Exception as err:
            con.rollback()
            print(err)
        finally:
            super().close(cursor, con)



if __name__ == '__main__':
    client = ClientDB().insert('123456','김말숙','123456@gmail.com','010-1234-5678')
    print(client)

    # client = ClientDB().selectOne('123456', '123456@gmail.com')
    # print(client)

    # ClientDB().update('1', '123456','김말숙','123456@gmail.com','010-1234-5678')

    # clientall = ClientDB().selectAll()
    # for client in clientall:
    #     print(client)