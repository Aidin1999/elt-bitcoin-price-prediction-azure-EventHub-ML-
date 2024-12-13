from pymongo import MongoClient, errors
import pandas as pd
import os
import logging

# Configure logging
logging.basicConfig(level=logging.INFO)

# MongoDB connection string (use environment variable for security)
CONNECTION_STRING = os.getenv("MONGODB_CONNECTION_STRING", "******")

DB_NAME = "price"
COLLECTION_NAME = "prices"
OUTPUT_FILE = "queried_data.csv"

def query_all_documents(collection):
    """Query all documents in the collection and save them to a CSV file"""
    try:
        documents = collection.find()  # Retrieve all documents
        data = list(documents)  # Convert cursor to a list

        if not data:
            logging.info("No documents found in the collection.")
            return

        # Convert MongoDB ObjectId to string for CSV serialization
        for doc in data:
            doc['_id'] = str(doc['_id'])

        # Convert the list of dictionaries to a DataFrame
        df = pd.DataFrame(data)

        # Save the DataFrame to a CSV file
        df.to_csv(OUTPUT_FILE, index=False)
        
        logging.info(f"Data successfully saved to {OUTPUT_FILE}")

    except errors.PyMongoError as e:
        logging.error(f"Error querying documents: {e}")

def main():
    """Connect to MongoDB, access the collection, and query all data"""
    client = MongoClient(CONNECTION_STRING)
    try:
        # Validate connection string
        client.server_info()
        logging.info("Successfully connected to MongoDB")
    except errors.ServerSelectionTimeoutError:
        logging.error("Invalid MongoDB connection string or timed out when attempting to connect")
        return

    # Access the collection
    db = client[DB_NAME]
    collection = db[COLLECTION_NAME]

    # Query and save all documents
    query_all_documents(collection)

if __name__ == '__main__':
    main()
