#!/usr/bin/env python3
"""
Write a Python script that provides some stats about Nginx logs stored
in MongoDB:
"""
import pymongo


client = pymongo.MongoClient("mongodb://localhost:27017/")
db = client["logs"]
collection = db["nginx"]

# Count total logs
total_logs = collection.count_documents({})

# Count logs by method
methods = ["GET", "POST", "PUT", "PATCH", "DELETE"]
method_counts = {method: collection.count_documents({
    "method": method}) for method in methods}

# Count logs with method GET and path /status
status_check_count = collection.count_documents(
        {"method": "GET", "path": "/status"})

# Print stats
print(f"{total_logs} logs")
print("Methods:")
for method, count in method_counts.items():
    print(f"\tmethod {method}: {count}")
print(f"{status_check_count} status check")
