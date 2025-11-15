"""
Created on 9 Nov 2025

@author: Bruno Beloff (bbeloff@me.com)

A structured representation of a message

{
    "routing": "TST.001.002.MPU.001.100",
    "body": "hello"
}

https://www.geeksforgeeks.org/python/python-sqlite-working-with-date-and-datetime/
https://stackoverflow.com/questions/17574784/sqlite-current-timestamp-with-milliseconds
https://forum.xojo.com/t/sqlite-return-id-of-record-inserted/37896/3
"""

from abc import ABC

from mrcs_core.data.persistence import PersistentObject
from mrcs_core.db.dbclient import DBClient


# --------------------------------------------------------------------------------------------------------------------

class MessagePersistence(PersistentObject, ABC):
    """
    classdocs
    """

    __DATABASE = 'Logging'

    @classmethod
    def create_tables(cls):
        client = DBClient.instance(cls.__DATABASE)

        sql = '''
            CREATE TABLE IF NOT EXISTS messages (
            id INTEGER PRIMARY KEY, 
            rec TIMESTAMP NOT NULL DEFAULT(datetime('subsec')), 
            routing TEXT NOT NULL, 
            body TEXT NOT NULL 
        )'''
        client.execute(sql)

        sql = 'CREATE INDEX IF NOT EXISTS messages_id ON messages(id)'
        client.execute(sql)

        sql = 'CREATE INDEX IF NOT EXISTS messages_rec ON messages(rec)'
        client.execute(sql)

        sql = 'CREATE INDEX IF NOT EXISTS messages_routing ON messages(routing)'
        client.execute(sql)

        client.commit()


    @classmethod
    def drop_tables(cls):
        client = DBClient.instance(cls.__DATABASE)

        sql = 'DROP INDEX IF EXISTS messages_id'
        client.execute(sql)

        sql = 'DROP INDEX IF EXISTS messages_rec'
        client.execute(sql)

        sql = 'DROP INDEX IF EXISTS messages_routing'
        client.execute(sql)

        sql = 'DROP TABLE IF EXISTS messages'
        client.execute(sql)

        client.commit()


    # ----------------------------------------------------------------------------------------------------------------

    @classmethod
    def find_all(cls):
        client = DBClient.instance(cls.__DATABASE)

        sql = 'SELECT * FROM messages'
        client.execute(sql)
        client.commit()

        rows = client.fetchall()

        return (cls.construct_from_db(*fields) for fields in rows)


    @classmethod
    def find(cls, id: int):      # TODO: not needed here?
        client = DBClient.instance(cls.__DATABASE)

        sql = 'SELECT * FROM messages WHERE id = ?'
        data = (id,)
        client.execute(sql, data=data)
        client.commit()

        rows = client.fetchall()

        if not rows:
            return None

        return cls.construct_from_db(*rows[0])

    # TODO: find most recent N messages

    # ----------------------------------------------------------------------------------------------------------------

    @classmethod
    def insert(cls, entry: PersistentObject):
        client = DBClient.instance(cls.__DATABASE)

        sql = 'INSERT INTO messages (routing, body) VALUES (?,?)'
        client.execute(sql, data=entry.as_db_fields())

        sql = 'SELECT last_insert_rowid()'
        client.execute(sql)
        client.commit()

        rows = client.fetchall()

        return int(rows[0][0])


    @classmethod
    def test_insert(cls, rec, entry: PersistentObject):
        client = DBClient.instance(cls.__DATABASE)

        sql = 'INSERT INTO messages (rec, routing, body) VALUES (?,?,?)'
        client.execute(sql, data=(rec,) + entry.as_db_fields())

        sql = 'SELECT last_insert_rowid()'
        client.execute(sql)
        client.commit()

        rows = client.fetchall()

        return int(rows[0][0])
