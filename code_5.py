#CODE 5
# MongoDB query

from pymongo import MongoClient
import pprint
import pandas as pd


def get_db(db_name):
    client = MongoClient('localhost:27017')
    db = client.my_map.harrisburg_pennsylvania   # 'one' here is the database name. It will be created if it does not exist.
    return db


def get_sources(db, pipeline):
    return [doc for doc in db.aggregate(pipeline)]

if __name__ == '__main__':
    db = get_db('harrisburg_pennsylvania')
    
    #how many records
    print ("Number of records:")
    print (harrisburg.find().count())
    
    # how many nodes
    print ("Number of nodes:")
    print (harrisburg.find({"record_type":"node"}).count())
 
    #how many ways
    print ("Number of ways: ")
    print (harrisburg.find({"record_type":"way"}).count())
 
                                                
    # Number of unique users
    print ("Number of unique users: ")                                            
    print (len(harrisburg.find().distinct("record_created.user")))
    
    # zipcode list
    print ("Zipcode：")
    print ((harrisburg.find().distinct("zip"))) 
    
    # Top 1 contributing user
    print ("Top 1 contribution user: ")
    pipeline = [{"$group":{"_id":"$record_created.user","count":{"$sum":1}}},
                {"$sort":{"count":-1}},
                {"$limit":1}]
    result = get_sources(db, pipeline)
    pprint.pprint(result[0] )
    
                                              
    # Number of users appearing only once (having 1 post)  {"$limit":1}   
    print ("Number of users appearing only once")                                            
    pipeline =[{"$group":{"_id":"$record_created.user", "count":{"$sum":1}}}, 
               {"$group":{"_id":"$count", "num_users":{"$sum":1}}}, 
               {"$sort":{"_id":1}},
               {"$limit":1}]
    result = get_sources(db, pipeline)
    pprint.pprint(result[0]['num_users'])
                                                                                           
 
    # Top 10 amenity
    print ("Top 10 amenity:")
    pipeline =([{"$match":{"amenity":{"$exists":1}}}, 
                 {"$group":{"_id":"$amenity","count":{"$sum":1}}}, 
                 {"$sort":{"count":-1}}, 
                 {"$limit":10}])

    result = get_sources(db, pipeline)
    pprint.pprint (result) 
