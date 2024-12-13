import azure.functions as func
import logging
import json
from pymongo import MongoClient
import warnings

# Suppress the CosmosDB warning
warnings.filterwarnings('ignore', message='You appear to be connected to a CosmosDB cluster.')

app = func.FunctionApp()

# MongoDB Connection String
CONNECTION_STRING = os.getenv('CONNECTION_STRING')

# Connect to MongoDB
try:
    mongo_client = MongoClient(CONNECTION_STRING)
    db = mongo_client['price']
    collection = db['prices']
    logging.info("Successfully connected to MongoDB")
except Exception as e:
    logging.error(f"Failed to connect to MongoDB: {e}")

@app.event_hub_message_trigger(
    arg_name="azeventhub",
    event_hub_name="pricetopic",
    connection="EventHubConnectionString"  # Reference the key in local.settings.json
)
def eventhub_trigger(azeventhub: func.EventHubEvent):
    try:
        # Decode and log the message
        event_data = azeventhub.get_body().decode('utf-8')
        logging.info('Python EventHub trigger processed an event: %s', event_data)

        # Convert the event data to a Python dictionary
        data = json.loads(event_data)

        # Insert data into MongoDB
        collection.insert_one(data)
        logging.info("Inserted event data into MongoDB: %s", data)

    except Exception as e:
        logging.error(f"Error processing EventHub event or inserting into MongoDB: {e}")

