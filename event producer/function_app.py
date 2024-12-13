import azure.functions as func
import logging
from azure.eventhub import EventHubProducerClient, EventData
import os
import json
import requests
from datetime import datetime
import pytz
import pandas as pd

# Environment variables
url = os.getenv("url")
headers = json.loads(os.getenv("headers"))  # Parse headers from JSON string
connection_string = os.getenv("EventHubConnectionString")
EVENT_HUB_NAME = 'pricetopic'

app = func.FunctionApp()

@app.function_name('send_to_eventhub')
@app.timer_trigger(schedule="0 */1 * * * *", arg_name="timer")
def send_to_eventhub(timer: func.TimerRequest):
    try:
        # Create the Event Hub producer client
        producer = EventHubProducerClient.from_connection_string(
            conn_str=connection_string,
            eventhub_name=EVENT_HUB_NAME
        )

        gmt_tz = pytz.timezone('GMT')
        today = datetime.now(gmt_tz).strftime("%Y-%m-%d %H:%M:%S")

        # Make the API request
        response = requests.get(url, headers=headers, params={"ids": "bitcoin", "vs_currencies": "usd"})
        response.raise_for_status()  # Ensure the request was successful

        # Prepare the event data
        price_now = {
            'date': today,
            'price': response.json().get('bitcoin', {}).get('usd')
        }

        # Send the event data to Event Hub
        with producer:
            event = EventData(json.dumps(price_now))
            producer.send_batch([event])
            logging.info(f"Sent event to Event Hub: {price_now}")

    except Exception as e:
        logging.error(f"Error sending event to Event Hub: {e}")
