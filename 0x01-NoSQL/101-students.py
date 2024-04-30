#!/usr/bin/env python3
"""
Python function that returns all students sorted by average score
"""


def top_students(mongo_collection):
    """Returns students by score."""
    pipeline = [
        {
            "$project": {
                "name": "$name",
                "averageScore": {"$avg": "$topics.score"}
            }
        },
        {
            "$sort": {
                "averageScore": -1
            }
        }
    ]
    return mongo_collection.aggregate(pipeline)

