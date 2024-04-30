#!/usr/bin/env python3
"""
Write a Python function that lists all documents in a collection:
"""
import pymongo


def list_all(mongo_collection):
    """
    List all documents in Python
    """
    if not mongo_collection:
        return []
    return list(mongo_collection.find())
