import mysql.connector
import threading

# MySQL connection parameters
host = "localhost"
user = "your_username"
password = "your_password"
database = "your_database"
table_name = "your_table"

# Number of concurrent connections
num_connections = 10

# Function to execute queries
def execute_queries():
    try:
        # Establishing the connection
        connection = mysql.connector.connect(
            host=host,
            user=user,
            password=password,
            database=database
        )

        print("Connection successful!")

        # Perform database operations
        cursor = connection.cursor()
        
        query = f"SELECT * FROM {table_name}"
        cursor.execute(query)

        # Fetch all rows
        rows = cursor.fetchall()
        for row in rows:
            print(row)


    except mysql.connector.Error as error:
        print("Failed to connect to MySQL database:", error)


    finally:
        if connection.is_connected():
            connection.close()
            print("Connection closed.")

# Create multiple threads for concurrent connections
threads = []
for _ in range(num_connections):
    thread = threading.Thread(target=execute_queries)
    threads.append(thread)

# Start the threads
for thread in threads:
    thread.start()

# Wait for all threads to complete
for thread in threads:
    thread.join()