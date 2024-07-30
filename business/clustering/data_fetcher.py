import pymongo
from datetime import datetime, timedelta, timezone
# def fetch_posts_from_mongodb(uri, database_name, collection_name):
#     client = pymongo.MongoClient(uri, tlsAllowInvalidCertificates=True)
#     db = client[database_name]
#     collection = db[collection_name]
#     posts = list(collection.find().limit(1000).sort("time", -1))
#     texts = [post['summary'] for post in posts if post['summary'] is not None]
#     return texts
def fetch_posts_from_mongodb(uri, database_name, collection_name):
    client = pymongo.MongoClient(uri, tlsAllowInvalidCertificates=True)
    db = client[database_name]
    collection = db[collection_name]

    now = datetime.now()
    # Định nghĩa đầu ngày hiện tại (giữa đêm) và cuối ngày
    start_of_day = datetime(now.year, now.month, now.day) - timedelta(days=1)
    end_of_day = start_of_day + timedelta(days=1) - timedelta(seconds=1)
    print(start_of_day)
    print(end_of_day)
    # Query to fetch posts created today
    posts = list(collection.find({
        "time": {
            "$gt": start_of_day,
            "$lt": end_of_day
        }
    }).sort("time", -1))
    texts = [post.get('summary') for post in posts if post.get('summary') is not None]
    return texts
