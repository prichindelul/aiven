'''
Created on 13.05.2021

@author: Mircea
'''
import psycopg2
from config import config


def get_logs():
    """ query data from the website_logs table """
    conn = None
    try:
        params = config()
        conn = psycopg2.connect(**params)
        cur = conn.cursor()
        cur.execute("SELECT created_at, request_id, message FROM website_logs ORDER BY created_at")
        print("The number of log lines: ", cur.rowcount)
        row = cur.fetchone()

        while row is not None:
            print(row)
            row = cur.fetchone()

        cur.close()
    except (Exception, psycopg2.DatabaseError) as error:
        print(error)
    finally:
        if conn is not None:
            conn.close()


if __name__ == '__main__':
    get_logs()