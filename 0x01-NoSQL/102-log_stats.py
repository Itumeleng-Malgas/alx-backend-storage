#!/usr/bin/env python3
"""
Improve 12-log_stats.py by adding the top 10 of the most present IPs in the
collection nginx of the database logs
"""
from pymongo import MongoClient


def print_nginx_logs():
    """ Log stats - new version """
    client = MongoClient('mongodb://127.0.0.1:27017')
    nginx_collection = client.logs.nginx
    
    # Count total logs
    total_logs = nginx_collection.count_documents({})
    print(f"{total_logs} logs")
    
    # Count logs by method
    print('Methods:')
    methods = ['GET', 'POST', 'PUT', 'PATCH', 'DELETE']
    for method in methods:
        method_count = nginx_collection.count_documents({'method': method})
        print(f"\tmethod {method}: {method_count}")
    
    # Count status checks
    status_check_count = nginx_collection.count_documents({'method': 'GET', 'path': '/status'})
    print(f"{status_check_count} status check")
    
    # List top 10 IPs
    print('IPs:')
    sorted_ips = nginx_collection.aggregate([
        {'$group': {'_id': "$ip", 'totalRequests': {'$sum': 1}}},
        {'$sort': {'totalRequests': -1}},
        {'$limit': 10},
    ])
    for sorted_ip in sorted_ips:
        ip = sorted_ip['_id']
        ip_count = sorted_ip['totalRequests']
        print(f"\t{ip}: {ip_count}")


if __name__ == '__main__':
    print_nginx_logs()
