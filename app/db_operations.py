import psycopg2

def get_db_connection():
    connection = psycopg2.connect(
        database="yourDatabase",
        user="yourUser",
        password="yourPassword",
        host="localhost"
    )
    return connection
           
    
# INSERT QUERY
def execute_create_query(query, params=None):
    connection = get_db_connection()
    cursor = connection.cursor()

    try:
        cursor.execute(query, params)
        connection.commit()
        print("Insert query executed successfully.")
    except Exception as e:
        print(f"Error executing insert query: {e}")

    cursor.close()
    connection.close()


# READ QUERY
def execute_read_query(query, params=None):
    connection = get_db_connection()
    cursor = connection.cursor()

    try:
        cursor.execute(query, params)
        result = cursor.fetchall()
        print("Select query execute successfully.")
        return result
    except Exception as e:
        print(f"Error executing select query: {e}")

    cursor.close()
    connection.close()
    return None


# UPDATE QUERY
def execute_update_query(query, params=None):
    connection = get_db_connection()
    cursor = connection.cursor()

    try:
        cursor.execute(query, params)
        connection.commit()
        print("Update query executed successfully.")
    except Exception as e:
        print(f"Error executing update query: {e}")

    cursor.close()
    connection.close()


# DELETE QUERY
def execute_delete_query(query, params=None):
    connection = get_db_connection()
    cursor = connection.cursor()

    try:
        cursor.execute(query, params)
        connection.commit()
        print("Delete query executed successfully.")
    except Exception as e:
        print(f"Error executing delete query: {e}")

    cursor.close()
    connection.close()