import os
import psycopg2
from flask import current_app


def migrate():
    """ Droping all tables and creating the again"""

    queries = [
        'DROP TABLE IF EXISTS users',
        'DROP TABLE IF EXISTS fooditems',
        'DROP TABLE IF EXISTS foodorders',
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
            name VARCHAR NOT NULL  UNIQUE,
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

    conn = None

    try:
        conn = psycopg2.connect(
            host=os.getenv("HOST"), database=os.getenv("DATABASE"),
            user=os.getenv("USER"), password=os.getenv("PASSWORD")
        )
        cur = conn.cursor()

        for query in queries:
            cur.execute(query)
        conn.commit()
        cur.close()

    except (Exception, psycopg2.DatabaseError) as error:
        print(error)
    finally:
        if conn is not None:
            conn.close()


if __name__ == '__main__':
    migrate()
