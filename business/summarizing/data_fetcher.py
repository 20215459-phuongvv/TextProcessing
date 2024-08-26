import pymongo
from datetime import datetime, timedelta, timezone
from schema.response import SummarizeResponse
from bson import ObjectId

def save_summarized_clusters(uri: str, database_name: str, collection_name: str, summarized_cluster: SummarizeResponse):
    client = pymongo.MongoClient(uri, tlsAllowInvalidCertificates=True)
    db = client[database_name]
    collection = db[collection_name]
    for cluster in summarized_cluster.summarized_cluster:
      if hasattr(cluster, 'id') and cluster.id is not None:
          existing_cluster = collection.find_one({"_id": ObjectId(cluster.id)})
          update_data = {
              "last_updated": cluster.last_updated,
              "summarized_events": [
                  {
                      "time": doc.time,
                      "text": doc.text
                  } for doc in cluster.summarized_events
              ] + [
                  {
                      "time": doc["time"],
                      "text": doc["text"]
                  } for doc in existing_cluster["summarized_events"]
              ],
          }
          collection.update_one({"_id": ObjectId(cluster.id)}, {"$set": update_data})
      else:
        cluster = {
          "last_updated": cluster.last_updated,
          "title": cluster.title,
          "summarized_events": [ 
            {
                "time": doc.time,
                "text": doc.text
            } for doc in cluster.summarized_events
          ],
          "documents": [
            {
              "time": doc.time, 
              "text": doc.text
            } for doc in cluster.documents
          ]
        }
        collection.insert_one(cluster)
    client.close()