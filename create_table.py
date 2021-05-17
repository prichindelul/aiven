'''
Created on 13.05.2021

@author: Mircea
'''
#https://www.postgresqltutorial.com/postgresql-python/

import psycopg2
from config import config


def create_table():
    """ create table in the PostgreSQL database"""
    command = (
        """
        CREATE TABLE website_logs (
			request_id serial PRIMARY KEY,
			created_at timestamp default current_timestamp,
			message VARCHAR ( 120 )  NOT NULL
		)
        """)
    conn = None
    try:
        # read the connection parameters
        params = config()
        # connect to the PostgreSQL server
        conn = psycopg2.connect(**params)
        cur = conn.cursor()
        # create table if it doesn't exist
        cur.execute(command)
        """
        if not check_table_exists:
            cur.execute(command)
        else:
            print("Table already exists")
        """
        # close communication with the PostgreSQL database server
        cur.close()
        # commit the changes
        conn.commit()
    except (Exception, psycopg2.DatabaseError) as error:
        print(error)
    finally:
        if conn is not None:
            conn.close()

def check_table_exists(name):
	conn = None
	# read the connection parameters
	params = config()
    # connect to the PostgreSQL server
	conn = psycopg2.connect(**params)
	cur = conn.cursor()
	#check if table already exists
	cur.execute("select exists(select * from information_schema.tables where table_name=%s)", ('website_logs',))
	return cur.fetchone()[0]

if __name__ == '__main__':
    create_table()