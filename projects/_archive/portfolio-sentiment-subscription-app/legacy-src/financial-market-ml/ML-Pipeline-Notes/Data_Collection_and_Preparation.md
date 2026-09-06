# Data Collection & Preparation

This document outlines the steps and methods for the Data Collection & Preparation stage in the process of predicting major incidents in AKS clusters, on-premise k8 clusters, or app services.

## Table of Contents

1. [Objective](#objective)
2. [Implementation Steps](#implementation-steps)
3. [Key Features](#key-features)
4. [Data Sources](#data-sources)
5. [Code Snippets](#code-snippets)
6. [Tools and Technologies](#tools-and-technologies)
7. [Challenges and Solutions](#challenges-and-solutions)

---

## Objective

To establish a reliable and scalable data pipeline that collects and prepares data for subsequent analysis and modeling.

## Implementation Steps

1. **Define Metrics**: Decide on features to collect. Typical features include CPU usage, memory usage, disk I/O, network latency, error rates, and request latency.
2. **Data Collection**: Collect data from various sources like logs, metrics systems, and monitoring tools.
3. **Data Storage**: Store the collected data in a scalable and secure storage system.
4. **Data Labeling**: Label data points for supervised learning if applicable. For instance, label data points where user experience lagged for more than the SLO as '1' (incident) and others as '0' (no incident).

## Key Features

- **CPU Usage**: Measures the computational power being consumed.
- **Memory Usage**: Quantifies the RAM usage in the system.
- **Disk I/O**: Measures the read/write operations on disk.
- **Network Latency**: Measures the time taken to transfer data over the network.
- **Error Rates**: Quantifies the number of errors in a given time frame.
- **Request Latency**: Measures the time taken to complete a request.

## Data Sources

- **Logs**: Text files that store a record of system events.
- **Metrics Systems**: Tools like Prometheus that capture numerical data.
- **Monitoring Tools**: Software like Grafana that provides a real-time view of system performance.
## Code Snippets

### Fetching Logs from Azure

Here's a Python example using Azure SDK to fetch logs:

```python
from azure.loganalytics import LogAnalyticsDataClient
from azure.loganalytics.models import QueryBody

client = LogAnalyticsDataClient(credentials)
workspace_id = "<Workspace_ID>"

query = "AzureActivity | limit 10"
body = QueryBody(query=query)
response = client.query(workspace_id, body)
print(response)
```

``` python
import splunklib.client as client

# Create a Service instance and log in 
service = client.connect(
    host='localhost',
    port=8089,
    username='admin',
    password='changeme')

# Fetch logs
kwargs_export = {"search_mode": "normal"}
searchquery_export = "search * | head 10"

exportsearch_results = service.jobs.export(searchquery_export, **kwargs_export)

# Output results
for result in exportsearch_results:
    print(result)

```


## Tools and Technologies

- **Data Collection**: Prometheus, Fluentd
- **Data Storage**: InfluxDB, Elasticsearch
- **Monitoring**: Grafana

## Challenges and Solutions

- **Scalability**: As the system grows, the volume of data will increase. Using scalable storage solutions like InfluxDB can mitigate this issue.
- **Data Integrity**: Ensuring that the data collected is accurate and free from errors is critical. Validation checks can be implemented to overcome this challenge.
