# Standard library imports
import logging
import subprocess
from pathlib import Path
from urllib.parse import quote_plus

# # Import Dependencies
from pymongo import MongoClient
from pprint import pprint

# Local application imports
from .config_loader import load_config

def mongoGetCredentials():
    """
    Reads a json file to construct a MongoDB connection string

    Returns:
        str: MongoDB connection string.
    """
    # Call utils function to load configuration from a JSON file
    config = load_config('config.json')

    # Retrieve the database credentials from the configuration
    mongodb_user = config.get('mongodb_cluster', {}).get('user')
    mongodb_pswd = config.get('mongodb_cluster', {}).get('password')
    mongodb_srvr = config.get('mongodb_cluster', {}).get('server')

    # Validate the credentials
    if not mongodb_user or not mongodb_pswd or not mongodb_srvr:
        logging.error("MongoDB credentials not found in the configuration file.")
        raise ValueError("Incomplete MongoDB credentials in configuration.")
    
    # URL encode the credentials
    user = quote_plus(mongodb_user)
    password = quote_plus(mongodb_pswd)

    # Return MongoDB connection string
    return f"mongodb+srv://{user}:{password}@{mongodb_srvr}/?tls=true"

def mongoListDatabases():
    """
    Connects to MongoDB and retrieves a list of all available databases.

    Returns:
        list: A list of database names.
    """
    # Get MongoDB credentials and establish a connection
    mongo_uri = mongoGetCredentials()
    
    try:
        client = MongoClient(mongo_uri)

        # List all databases on the server
        databases = client.list_database_names()

        # Exclude 'admin' and 'local' databases
        excluded_databases = ['admin', 'local']
        filtered_databases = [db for db in databases if db not in excluded_databases]

        return filtered_databases
        
    except Exception as e:
        logging.error(f"An error occurred while retrieving databases: {e}")
        return []
    
    finally:
        # Close the client connection
        client.close()

def mongoListCollections(db_name):
    """
    Connects to MongoDB, retrieves a list of collections from the specified database.

    Args:
        db_name (str): The name of the database from which to retrieve collections.

    Returns:
        list: A list of collection names in the specified database, or an empty list if an error occurs.
    """
    # Get MongoDB credentials and establish a connection
    mongo_uri = mongoGetCredentials()
    
    try:
        client = MongoClient(mongo_uri)
        # Check if the database already exists
        existing_databases = mongoListDatabases()
        if db_name not in existing_databases:
            logging.warning(f"Database '{db_name}' does not exist.")
            return []

        # Get the specified database
        db = client[db_name]
        # List all collections in the database
        collections = db.list_collection_names()
        
        return collections

    except Exception as e:
        logging.error(f"An error occurred while retrieving collections from database '{db_name}': {e}")
        return []
    
    finally:
        # Close the client connection
        client.close()

def mongoCreateDatabase(db_name):
    """
    Creates a MongoDB database if it doesn't exist by inserting a sample document.

    Args:
        db_name (str): The name of the database to create.

    Returns:
        str: The database name if it was created or already exists,
             or an error message if the database name is restricted.
    """
    # Prevent creating databases named 'local' or 'admin'
    if db_name in ['local', 'admin']:
        logging.error(f"Attempted to create a restricted database '{db_name}'.")
        return f"Error: The database name '{db_name}' is not allowed."

    # Get MongoDB credentials and establish a connection
    mongo_uri = mongoGetCredentials()
    
    try:
        client = MongoClient(mongo_uri)

        # Check if the database already exists
        existing_databases = mongoListDatabases()
        if db_name in existing_databases:
            return db_name

        # Reference the new database
        db = client[db_name]

        # Insert a sample document to create the database
        sample_collection = db['sample_collection']
        sample_collection.insert_one({"message": "This is a sample document to create the database."})

        return db_name

    except Exception as e:
        logging.error(f"An error occurred while creating database '{db_name}': {e}")
        return ""
    
    finally:
        # Close the client connection
        client.close()

def mongoImportFile(db_name, collection_name, file_type, file_path, headerline=True, drop=False):
    """
    Imports a data file into a specified MongoDB collection and returns the count of records imported.

    Args:
        db_name (str): The name of the database to import data into.
        collection_name (str): The name of the collection to import data into.
        file_type (str): The type of the file to import (e.g., 'csv', 'json', 'tsv').
        file_path (str): The path to the file to be imported.
        headerline (bool): Indicates whether the first line of a CSV/TSV file contains header fields. Default is True.
        drop (bool): Indicates whether to drop the collection before importing data. Default is False.

    Returns:
        int: The count of records imported.
    """
    # Get MongoDB credentials and establish a connection
    mongo_uri = mongoGetCredentials()
    
    # Create a MongoClient instance
    client = MongoClient(mongo_uri)

    # Build the mongoimport command
    command = [
        'mongoimport',
        '--uri', mongo_uri,
        '--db', db_name,
        '--collection', collection_name,
        '--type', file_type,
        '--file', str(file_path)
    ]

    # Include headerline option if specified
    if headerline and file_type in ['csv', 'tsv']:
        command.append('--headerline')

    # Include drop option if specified
    if drop:
        command.append('--drop')
        initial_count = 0
    else:
        # Get the initial document count
        initial_count = client[db_name][collection_name].count_documents({}) if collection_name in client[db_name].list_collection_names() else 0

    # Execute the command
    try:
        subprocess.run(command, check=True)
        logging.info(f"Imported {file_path} into collection {collection_name}.")

        # Check the number of records imported from the file
        imported_count = get_file_record_count(file_path, headerline)

        # After a successful import, retrieve the new document count in the collection
        new_count = client[db_name][collection_name].count_documents({})

        # Calculate the number of new records added
        new_records_added = new_count - initial_count

        # Log the results
        if new_records_added == imported_count:
            logging.info(f"Successfully imported {imported_count} new records.")
            return f"Imported {file_path} into collection {collection_name} successfully.", imported_count
        else:
            logging.warning(f"Imported records mismatch: expected {imported_count}, but added {new_records_added}.")
            return f"Warning: Imported records mismatch. Expected {imported_count}, but added {new_records_added}.", imported_count
    
    except subprocess.CalledProcessError as e:
        logging.error(f"Error importing {file_path}: {e}")
        return f"Error importing {file_path}: {e}", 0
    
    finally:
        # Close the client connection
        client.close()

def get_file_record_count(file_path, headerline=True):
    """
    Get the number of records in a file, accounting for header lines if specified.

    Args:
        file_path (str): The path to the file to count records in.
        headerline (bool): Indicates whether the first line is a header. Default is True.

    Returns:
        int: The number of records in the file.
    """
    record_count = 0
    if file_path.endswith('.csv') or file_path.endswith('.tsv'):
        with open(file_path, 'r', encoding='utf-8') as file:
            record_count = sum(1 for line in file)  # Count all lines
            if headerline:
                record_count -= 1  # Subtract 1 for the header line if applicable
    elif file_path.endswith('.json'):
        with open(file_path, 'r', encoding='utf-8') as file:
            record_count = sum(1 for _ in file)  # Each line is a separate document
    else:
        logging.error("Unsupported file type.")
    
    return max(0, record_count)  # Ensure we don't return a negative count
