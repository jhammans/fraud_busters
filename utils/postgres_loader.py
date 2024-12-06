# Standard library imports
import csv
import logging
from pathlib import Path
from urllib.parse import quote_plus

# Import Dependencies
import psycopg2
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine

# Local application imports
from .config_loader import load_config

def postgresGetCredentials(engine_type="sqlalchemy"):
    """
    Reads a JSON configuration file and returns a PostgreSQL connection string for either psycopg2 or SQLAlchemy.

    Args:
        engine_type (str): Specify which connection string to return, either "psycopg2" or "sqlalchemy".
    
    Returns:
        str: PostgreSQL connection string for the specified engine.
    
    Raises:
        ValueError: If required credentials are missing or an invalid engine_type is provided.
    
    Example usage:
        conn_str_psycopg2 = postgresGetCredentials(engine_type="psycopg2")
        conn_str_sqlalchemy = postgresGetCredentials(engine_type="sqlalchemy")
    """
    # Load the configuration from a JSON file
    config = load_config('config.json')

    # Retrieve the database credentials from the configuration
    postgres_user = config.get('postgres_connection', {}).get('user')
    postgres_pswd = config.get('postgres_connection', {}).get('password')
    postgres_srvr = config.get('postgres_connection', {}).get('server')
    postgres_port = config.get('postgres_connection', {}).get('port')       

    # Validate the credentials
    if not postgres_user or not postgres_pswd or not postgres_srvr:
        logging.error("Postgres credentials not found in the configuration file.")
        raise ValueError("Incomplete Postgres credentials in configuration.")

    # URL encode the credentials
    user = quote_plus(postgres_user)
    password = quote_plus(postgres_pswd)

    # Return the appropriate connection string based on the engine_type
    if engine_type == "psycopg2":
        # Connection string for psycopg2
        return f"user='{postgres_user}' password='{postgres_pswd}' host='{postgres_srvr}' port='{postgres_port}'"
    elif engine_type == "sqlalchemy":
        # Connection string for SQLAlchemy with psycopg2 driver
        return f"postgresql+psycopg2://{user}:{password}@{postgres_srvr}:{postgres_port}"
    else:
        logging.error("Invalid engine type specified. Use 'psycopg2' or 'sqlalchemy'.")
        raise ValueError("Invalid engine type. Please specify either 'psycopg2' or 'sqlalchemy'.")

def postgresListDatabases():
    """
    Connects to the PostgreSQL server using the provided connection string 
    and retrieves a list of available databases.

    Returns:
    list: A list of database names, excluding system databases (postgres, template0, template1).
    """
    # Get PostgresSQL credentials and establish a connection
    postgres_uri = postgresGetCredentials(engine_type="psycopg2")

    try:
        with psycopg2.connect(f"{postgres_uri} dbname='postgres'") as conn:
            with conn.cursor() as cursor:
                # Execute the SQL command to list databases
                cursor.execute("SELECT datname FROM pg_database WHERE datistemplate = false;")

                # Fetch all database names excluding the system databases
                databases = [db[0] for db in cursor.fetchall() if db[0] not in ['postgres', 'template0', 'template1']]

                logging.info(f"Databases retrieved: {databases}")

                return databases

    except psycopg2.Error as e:
        logging.error(f"An error occurred while retrieving databases: {e}")
        return []

def postgresListTables(db_name):
    """
    Lists all the tables in the specified PostgreSQL database using psycopg2.

    Args:
        db_name (str): The name of the PostgreSQL database.

    Returns:
        list: A list of table names in the database.
    """
    # Get PostgresSQL credentials and establish a connection
    postgres_uri = postgresGetCredentials(engine_type="psycopg2")

    # Use a context manager to handle the connection and cursor
    try:
        with psycopg2.connect(f"{postgres_uri} dbname='{db_name}'") as conn:
            with conn.cursor() as cursor:
                # Query to list all tables
                query = """
                SELECT table_name 
                FROM information_schema.tables 
                WHERE table_schema = 'public'
                ORDER BY table_name;
                """
                cursor.execute(query)
                tables = cursor.fetchall()

                # Extract table names from the result
                table_list = [table[0] for table in tables]
                logging.info(f"Tables in database {db_name}: {table_list}")
                
                return table_list

    except psycopg2.Error as e:
        logging.error(f"Error listing tables in database {db_name}: {e}")
        return []

def postgresRunSqlScript(db_name, sql_file):
    """
    Executes an SQL script in a PostgreSQL database using psycopg2.

    Args:
        db_name (str): The name of the PostgreSQL database.
        sql_file (str): The SQL script file path.

    Returns:
        str: A message indicating the result of the execution.
    """
    # Get PostgreSQL credentials and construct the connection URI
    postgres_uri = postgresGetCredentials(engine_type="psycopg2")
    connection_string = f"{postgres_uri} dbname='{db_name}'"

    try:
        # Establish connection to the database using a context manager
        with psycopg2.connect(connection_string) as conn:
            with conn.cursor() as cursor:
                # Read the SQL script
                with open(sql_file, 'r') as file:
                    sql_script = file.read()

                # Split the script into individual commands
                commands = sql_script.split(';')
                
                executed_commands = 0  # Track the number of executed commands
                # Execute each command separately
                for command in commands:
                    if command.strip():  # Avoid empty commands
                        try:
                            cursor.execute(command)
                            executed_commands += 1
                        except psycopg2.Error as e:
                            logging.error(f"Error executing command: {command.strip()}. Error: {e}")

                return f"Successfully executed {executed_commands} commands from {sql_file}."
    
    except Exception as e:
        logging.error(f"Error executing SQL script {sql_file}: {e}")
        return f"An error occurred while executing the SQL script: {e}"

def postgresImportFile(db_name, table_name, file_location, delimiter=',', headerline=True):
    """
    Imports data from a specified file into a PostgreSQL table, and compares the number of records in the file 
    to the number of records actually inserted into the table, taking into account records already present.

    Args:
        db_name (str): The name of the PostgreSQL database.
        table_name (str): The name of the table to import data into.
        file_location (str): The filepath of the file to import.
        delimiter (str): The delimiter used in the file (default is ',').
        headerline (bool): Indicates if the first line of the file contains headers (default is True).

    Returns:
        str: A success or warning message.
        int: The number of records imported into the table.
    """
    # Get PostgreSQL credentials and establish a connection
    postgres_uri = postgresGetCredentials(engine_type="psycopg2")

    try:
        # Open the file and calculate the number of records in it
        with open(file_location, 'r') as file:
            reader = csv.reader(file, delimiter=delimiter)
            
            if headerline:
                next(reader)  # Skip header line if necessary
            
            file_record_count = sum(1 for row in reader)  # Count the rows in the file
            
        with psycopg2.connect(f"{postgres_uri} dbname='{db_name}'") as conn:
            conn.autocommit = False

            with conn.cursor() as cursor:
                # Count the records in the table before import
                cursor.execute(f"SELECT COUNT(*) FROM {table_name};")
                table_record_count_before = cursor.fetchone()[0]

                # Open the file again for the COPY command
                with open(file_location, 'r') as file:
                    if headerline:
                        headers = next(file)  # Skip header line if necessary
                        headers_str = ', '.join(headers.strip().split(delimiter))  # Convert header list to string
                        sql_copy = f"COPY {table_name} ({headers_str}) FROM STDIN WITH CSV HEADER DELIMITER '{delimiter}';"
                    else:
                        sql_copy = f"COPY {table_name} FROM STDIN WITH CSV DELIMITER '{delimiter}';"

                    # Move the file pointer back to the beginning to reuse in COPY
                    file.seek(0)
                    cursor.copy_expert(sql_copy, file)

                # Commit the transaction after COPY operation
                conn.commit()

                # Count the records in the table after import
                cursor.execute(f"SELECT COUNT(*) FROM {table_name};")
                table_record_count_after = cursor.fetchone()[0]

                # Calculate the number of new records inserted
                records_inserted = table_record_count_after - table_record_count_before

                # Handle success and error logging
                if records_inserted == file_record_count:
                    logging.info(f"Successfully imported {records_inserted} new records into table {table_name}.")
                    return f"Successfully imported {file_record_count} records from {file_location} into {table_name}.", records_inserted
                else:
                    logging.warning(f"Imported records mismatch: expected {file_record_count}, but added {records_inserted}.")
                    return f"Warning: Imported records mismatch. Expected {file_record_count}, but added {records_inserted}.", records_inserted

    except psycopg2.Error as e:
        # Rollback transaction if an error occurs
        if conn:
            conn.rollback()
        logging.error(f"Error importing file {file_location} into table {table_name}: {e}")
        return f"Error: Failed to import {file_location} into {table_name}.", 0