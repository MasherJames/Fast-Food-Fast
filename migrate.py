import os
import psycopg2
from flask import current_app


class TablesSetup:

    def __init__(self):

        try:
            self.conn = psycopg2.connect(
                host=os.getenv("HOST"), database=os.getenv("DATABASE"),
                user=os.getenv("USER"), password=os.getenv("PASSWORD")
            )
            self.cur = self.conn.cursor()

        except (Exception, psycopg2.DatabaseError) as error:
            print(error)

    def drop_tables(self):
        """ Dropping all tables """
        queries = [
            'DROP TABLE IF EXISTS users',
            'DROP TABLE IF EXISTS fooditems',
            'DROP TABLE IF EXISTS foodorders'
        ]
        for query in queries:
            self.cur.execute(query)
        self.conn.commit()
        self.cur.close()

    def migrate(self):
        """ Creating tables """

        queries = [
            '''
            CREATE TABLE users(
                id serial PRIMARY KEY,
                username VARCHAR NOT NULL UNIQUE,
                email VARCHAR NOT NULL UNIQUE,
                password VARCHAR NOT NULL,
                is_admin BOOLEAN NOT NULL
            )
            ''',
            '''
            CREATE TABLE fooditems(
                id serial PRIMARY KEY,
                name VARCHAR NOT NULL ,
                description VARCHAR NOT NULL,
                price INTEGER NOT NULL,
                date TIMESTAMP
            )
            ''',
            '''
            CREATE TABLE foodorders(
                id serial PRIMARY KEY,
                name VARCHAR NOT NULL,
                destination VARCHAR NOT NULL,
                status VARCHAR NOT NULL,
                date TIMESTAMP
            )
            '''
        ]

        for query in queries:
            self.cur.execute(query)
        self.conn.commit()
        self.cur.close()


if __name__ == '__main__':
    TablesSetup().drop_tables()
    TablesSetup().migrate()
