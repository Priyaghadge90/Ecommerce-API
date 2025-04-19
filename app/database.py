import pymongo
def get_db():
    url="mongodb://localhost:27017/"
    mongo_client=pymongo.MongoClient(url)
    db=mongo_client["Mini_Ecommerce_db"]
    collection=db["Product_details"]
    return collection
