'''
Created on 13.05.2021

@author: Mircea
'''
#https://www.postgresqltutorial.com/postgresql-python/
import psycopg2
from config import config

def insert_log(message):
    """ insert one line into the logs table  """
    sql = "INSERT INTO website_logs(message) VALUES(%s)"
    conn = None
    try:
        # read database configuration
        params = config()
        # connect to the PostgreSQL database
        conn = psycopg2.connect(**params)
        # create a new cursor
        cur = conn.cursor()
        # execute the INSERT statement
        cur.execute(sql,(message,))
        # commit the changes to the database
        conn.commit()
        # close communication with the database
        cur.close()
    except (Exception, psycopg2.DatabaseError) as error:
        print(error)
    finally:
        if conn is not None:
            conn.close()