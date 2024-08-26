import pymongo
from datetime import datetime, timedelta, timezone
from schema.response import ClusterResponse
from typing import List, Dict, Any

now = datetime.now()
start_of_day = datetime(now.year, now.month, now.day) - timedelta(days=8)
end_of_day = start_of_day + timedelta(days=1) - timedelta(seconds=1)
def fetch_posts(uri, database_name, collection_name):
    client = pymongo.MongoClient(uri, tlsAllowInvalidCertificates=True)
    db = client[database_name]
    collection = db[collection_name]
    # Query to fetch posts created today
    posts = list(collection.find({
        "time": {
            "$gte": start_of_day,
            "$lte": end_of_day
        }
    })
    .sort("time", -1))
    documents = [
        {
            'text': post.get('summary'),
            'time': post.get('time')
        }
        for post in posts
        if post.get('summary') is not None and post.get('time') is not None
    ]
    return documents

def fetch_events(uri, database_name, collection_name):
    client = pymongo.MongoClient(uri, tlsAllowInvalidCertificates=True)
    db = client[database_name]
    collection = db[collection_name]

    # Query to fetch posts created today
    clusters = list(collection.find({
        "last_updated": {
            "$gte": start_of_day - timedelta(days=1),
            "$lte": end_of_day
        }
    })
    .sort("last_updated", -1))
    events = []
    for cluster in clusters:
        summarized_events = cluster.get("summarized_events", [])
        if summarized_events:
            most_recent_event = max(summarized_events, key=lambda event: event['time'])
            if most_recent_event:
                events.append(most_recent_event)
    return events

def fetch_clusters(uri, database_name, collection_name):
    client = pymongo.MongoClient(uri, tlsAllowInvalidCertificates=True)
    db = client[database_name]
    collection = db[collection_name]

    # Query to fetch posts created today
    clusters = list(collection.find({
        "last_updated": {
            "$gte": start_of_day - timedelta(days=1),
            "$lte": end_of_day
        }
    })
    .sort("last_updated", -1))
    return clusters

def save_clusters(uri: str, database_name: str, collection_name: str, cluster_response: ClusterResponse):
    client = pymongo.MongoClient(uri, tlsAllowInvalidCertificates=True)
    db = client[database_name]
    collection = db[collection_name]
    for cluster in cluster_response.clusters:
        cluster = {
                "cluster_id": cluster.cluster_id,
                "last_updated": datetime.now(timezone.utc),
                "documents": [
                    {
                        "time": doc.time, 
                        "text": doc.text
                    } for doc in cluster.documents
                ]
        }
        collection.insert_one(cluster)
    client.close()

def find_cluster_by_event(events: List[Dict[str, Any]], clusters: List[Dict[str, Any]], event_to_find: Dict[str, Any]) -> Dict[str, Any]:
    for cluster in clusters:
        summarized_events = cluster.get('summarized_events', [])
        if summarized_events:
            most_recent_event = max(summarized_events, key=lambda event: event['time'])
            if most_recent_event['time'] == event_to_find['time'] and most_recent_event['text'] == event_to_find['text']:
                return cluster
    return None

def update_cluster(cluster_to_find: Dict[str, Any], uri: str, database_name: str, collection_name: str):
    client = pymongo.MongoClient(uri, tlsAllowInvalidCertificates=True)
    db = client[database_name]
    collection = db[collection_name]

    collection.update_one(
        {"_id": cluster_to_find["_id"]},
        {"$set": {"documents": cluster_to_find["documents"]}}
    )
    client.close()