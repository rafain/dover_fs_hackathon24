import json
import os
import sys
import uuid
import config

from azure.core.exceptions import AzureError
from azure.cosmos import CosmosClient, PartitionKey

client = CosmosClient.from_connection_string(conn_str=config.nosql['dfslogs'])
data = client.get_database_client("dfslogs").query_containers("SELECT * FROM logs")

for item in data:
    print(item)