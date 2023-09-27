import psycopg2
from psycopg2 import Error
import psycopg2.extras as extras
import numpy as np
import pandas as pd

def connect():
    try:
        connection = psycopg2.connect(
            user="postgres",
            password="34567",
            host="localhost",
            port="5432",
            database="sasa"
        )

        cursor = connection.cursor()
        print("Server info", connection.get_dsn_parameters(), '\n')

        cursor.execute("SELECT version();")
        record = cursor.fetchone()
        print("Connected to", record, '\n')

        return connection

    except (Exception, Error) as error:
        print("Error connecting to postgresql", error)
        return False


def create_table():
    command = (
    """
    CREATE TABLE skin_care (
        id SERIAL PRIMARY KEY,
        Product_ID VARCHAR(255) NOT NULL,
        Product_Name VARCHAR(255) NULL,
        Brand VARCHAR(255) NULL,
        Restock VARCHAR(255) NULL,
        Sold_out VARCHAR(255) NULL,
        Tags VARCHAR(255) NULL,
        Original_Price VARCHAR(255) NULL,
        Discount_price VARCHAR(255) NULL,
        Created_Date date NULL
    )
    """
    )
    try:
      
        #connect to the PostgreSQL
        connection = connect()
        cur = connection.cursor()
        resp = cur.execute(command)
        print('resp:', resp)

        cur.close()

        connection.commit()
        print("Created table in postgreSQL")

    except (Exception, Error) as error:
        print("Error creating table", error)

    finally:
        if connection is not None:
            connection.close()




def insertDf(connection, df, table):

    # row of df = tuple
    tuple_list = [tuple(x) for x in df.to_numpy()]
    print('Tuple')    

    for _tuple in tuple_list[0:3]:
        print(_tuple)

    cols = ','.join(list(df.columns))
    #%s : table
    #(%s): column
    query = "INSERT INTO %s(%s) VALUES %%s" %(table, cols)
    print(f'\n\nQuery: {query}')
    cursor = connection.cursor()

    # insert into table multiple times
    try:
        extras.execute_values(cursor, query, tuple_list) #batch running the insert query
        connection.commit()
    except (Exception, Error) as error:
        print("Error creating table", error)
        cursor.close()
        return False
    
    finally:
        cursor.close()
        return True

