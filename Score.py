"""
Score.py
A package that is in charge of managing the scores file.
The scores file at this point will consist of only a number. That number is the accumulation of the
winnings of the user. Amount of points for winning a game is as follows:
POINTS_OF_WINNING = (DIFFICULTY X 3) + 5
Each time the user is winning a game, the points he one will be added to his current amount of
point saved in a file.
Methods
1. add_score - The function’s input is a variable called difficulty. The function will try to read
the current score in the scores file, if it fails it will create a new one and will use it to save
the current score.
"""

import os
import pymysql

# Connect to sql container:

def connect_to_sql():
    connection = None
    cursor = None
    try:
        connection = pymysql.connect(
            host=os.getenv("DB_HOST"),
            port=int(os.getenv("DB_PORT", 3306)),
            user=os.getenv("DB_USER", "root"),
            password=os.getenv("DB_PASSWORD", "gamespass"),
            database=os.getenv("DB_NAME", "games_db")
        )
        cursor = connection.cursor()
        # Create the users table if it doesn't exist
        create_table_query = """
            CREATE TABLE IF NOT EXISTS users_scores (
                name VARCHAR(50) NOT NULL,
                score VARCHAR(50) NOT NULL
            );
        """
        cursor.execute(create_table_query)
        print("Table 'users_scores' created or already exists.")

        return connection, cursor
  
    except Exception as e:
        print(f"Error connecting to database: {e}")
        return None,None


def add_score(difficulty,name):

    # Connect to database:
    conn , cursor = connect_to_sql()
    
    # if the connection in the function above returns None:
    if not conn and not cursor:
        print("Connection has failed!")
        return None 
    
    points_of_winning = (difficulty * 3) + 5
    
    try:
        cursor.execute(""" INSERT INTO users_scores (name,score) VALUE (%s,%s) """,(name,points_of_winning))
        conn.commit()
    except Exception as e:
        print(f"Error inserting score: {e}")
    finally:
        cursor.close()
        conn.close()

    return points_of_winning