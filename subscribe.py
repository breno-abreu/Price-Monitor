import psycopg2
from dotenv import load_dotenv
import os
from psycopg2.extras import DictCursor

def get_conn_string():
    # Load the environmental variables. Secrets that are stored in my machine.
    load_dotenv()
    sqluser = os.getenv("SQLUSER")
    sqlpass = os.getenv("SQLPASS")
    
    # Get server data
    host = '127.0.0.1'
    database = 'my_projects'
    
    # Create the path to the database
    return f'postgresql://{sqluser}:{sqlpass}@{host}/{database}'


def post_subscribers(link: str, element_name: str, element_type: str, site_name: str) -> str:
    try:

        if element_type == 'css':
            element_name = f".{element_name.replace(' ', '.')}"
        
        conn_string = get_conn_string()
    
        with psycopg2.connect(conn_string) as conn:
    
            # Creates the cursor to run queries
            with conn.cursor(cursor_factory=DictCursor) as cursor:
        
                # Runs a query to select everyhing from table person, the newly created table. This is just to check if the data was uploaded correctly
                query = f"INSERT INTO price_monitor_subscriptions (link, element_name, element_type, site_name) VALUES ('{link}', '{element_name}', '{element_type}', '{site_name}');"
                cursor.execute(query) 
    
        return 'OK'

    except Exception as err:
        return err


def get_subscribers():
    try:
        conn_string = get_conn_string()

        with psycopg2.connect(conn_string) as conn:
        
                # Creates the cursor to run queries
                with conn.cursor(cursor_factory=DictCursor) as cursor:
            
                    # Runs a query to select everything from table person, the newly created table. This is just to check if the data was uploaded correctly
                    query = f"SELECT * FROM price_monitor_subscriptions;"
                    cursor.execute(query)
                    return cursor.fetchall()

    except Exception as err:
        return err