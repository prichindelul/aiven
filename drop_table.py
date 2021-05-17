'''
Created on 13.05.2021

@author: Mircea
'''
import psycopg2
from config import config


def drop_table():
    """ drop tables in the PostgreSQL database"""
    sql = "DROP TABLE website_logs"
    conn = None
    try:
        # read the connection parameters
        params = config()
        # connect to the PostgreSQL server
        conn = psycopg2.connect(**params)
        cur = conn.cursor()
        # drop table 
        cur.execute(sql)
        # close communication with the PostgreSQL database server
        cur.close()
        # commit the changes
        conn.commit()
    except (Exception, psycopg2.DatabaseError) as error:
        print(error)
    finally:
        if conn is not None:
            conn.close()


if __name__ == '__main__':
    drop_table()