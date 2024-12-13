# Bitcoin Price Prediction with Azure Event Hub and Machine Learning

This project demonstrates an **Extract, Load, and Transform (ELT)** pipeline for real-time **Bitcoin price prediction** using **Azure Event Hub**, **Azure Functions**, **MongoDB**, and **Machine Learning** (ML). The goal is to fetch Bitcoin price data, process it, and make predictions using a machine learning model.

## Project Overview

Due to the requirement of having at least 7 days of data to complete the analysis, **pre-collected data from CoinMarketCap** has been used. This dataset closely simulates the results that would be obtained from real-time data collection using the CoinGecko API. The project pipeline is designed to work seamlessly with both live data and the pre-collected dataset.

## Project Structure

```
.
├── event producer/
│   ├── function_app.py        # Azure Function to fetch data and send to Event Hub
│   └── requirements.txt       # Dependencies for the producer function
│
├── event consumer/
│   ├── function_app.py        # Azure Function to consume data and store in MongoDB
│   └── requirements.txt       # Dependencies for the consumer function
│
└── bit coin ML/
    ├── ML.ipynb                              # Jupyter Notebook for ML analysis and prediction
    ├── fetch data.py                         # Script to fetch and preprocess data
    ├── BTC_1M_graph_coinmarketcap.csv        # Pre-collected 1-minute interval data
    └── BTC_7D_graph_coinmarketcap (1).csv    # Pre-collected 7-day data
```

## Workflow

1. **Fetch Data**:
   - The producer function fetches Bitcoin price data from the **CoinGecko API** (or pre-collected data from CoinMarketCap).
   - Sends the data to **Azure Event Hub**.

2. **Process Data**:
   - The consumer function listens to the Event Hub and inserts the received data into **MongoDB**.

3. **Machine Learning**:
   - The Jupyter Notebook (`ML.ipynb`) contains the machine learning analysis.
   - It uses the pre-collected data to train and evaluate the prediction model.

## Skills Demonstrated

- **Azure Functions**: For serverless data processing.
- **Azure Event Hub**: For real-time data streaming.
- **MongoDB**: For storing and querying the collected data.
- **Python**: For data fetching, processing, and analysis.
- **Pandas**: For data manipulation and saving data to CSV.
- **Machine Learning**: For analyzing and predicting Bitcoin prices.
- **Git**: For version control and project management.

## How to Run the Project

### 1. Set Up Environment Variables

Ensure the following environment variables are configured in your `local.settings.json`:

```json
{
  "IsEncrypted": false,
  "Values": {
    "AzureWebJobsStorage": "UseDevelopmentStorage=true",
    "FUNCTIONS_WORKER_RUNTIME": "python",
    "EventHubConnectionString": "<Your_EventHub_Connection_String>",
    "CONNECTION_STRING": "<Your_MongoDB_Connection_String>"
  }
}
```

### 2. Run the Producer Function

```bash
cd event producer
func host start --port 7071
```

### 3. Run the Consumer Function

```bash
cd event consumer
func host start --port 7072
```

### 4. Run the Machine Learning Analysis

- Open the `ML.ipynb` Jupyter Notebook in your favorite IDE (e.g., **VS Code** or **Jupyter Lab**).
- Execute the cells to train and evaluate the model using the pre-collected data.

## Conclusion

This project showcases a complete **ELT pipeline** integrating cloud services, real-time data processing, and machine learning for Bitcoin price prediction. It highlights key skills in **cloud computing**, **data engineering**, and **machine learning**.
