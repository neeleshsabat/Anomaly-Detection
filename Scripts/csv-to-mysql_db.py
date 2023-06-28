import pandas as pd
import mysql.connector

# Connect to the MySQL database
db = mysql.connector.connect(
host='localhost',
user='root',
password='root',
database='mydb01'
)

# Create a cursor object to interact with the database
cursor = db.cursor()

# Read the CSV file using pandas
csv_file = 'C:/Users/10710484/Downloads/unscaled train data.csv'
data = pd.read_csv(csv_file)

# Get the column names and data types from the CSV file
columns = data.columns.tolist()
data_types = data.dtypes.tolist()

# Define the desired truncation length for column names
truncation_length = 64 # Adjust the length as per your requirements

# Create a list of truncated column names
truncated_columns = [column[:truncation_length] for column in columns]

# Create a list of column definitions for the CREATE TABLE statement
column_definitions = []
for truncated_column, data_type in zip(truncated_columns, data_types):
    if data_type == 'object':
        column_definitions.append(f'`{truncated_column}` VARCHAR(255)')
    elif data_type == 'int64':
        column_definitions.append(f'`{truncated_column}` INT')
    elif data_type == 'float64':
        column_definitions.append(f'`{truncated_column}` FLOAT')
    # Add more data type mappings as needed for your specific CSV data

# Create the CREATE TABLE statement
table_name = 'your_table2'
create_table_query = f"CREATE TABLE `{table_name}` ({', '.join(column_definitions)})"

# Execute the CREATE TABLE statement
cursor.execute(create_table_query)

# Iterate over the rows of the dataframe and insert them into the database
for index, row in data.iterrows():
    # Create a list of column values
    values = [str(row[column]) for column in columns]

    # Create the placeholders for the VALUES clause in the INSERT statement
    placeholders = ', '.join(['%s'] * len(columns))

    # Create the INSERT statement
    insert_query = f"INSERT INTO `{table_name}` ({', '.join([f'`{truncated_column}`' for truncated_column in truncated_columns])}) VALUES ({placeholders})"

    # Execute the query with the column values
    cursor.execute(insert_query, values)


# Commit the changes to the database
db.commit()

# Close the database connection
db.close()

print('CSV data has been saved to the MySQL database.')