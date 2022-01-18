import pymongo

def connect_db(collection='employees'):
    myclient = pymongo.MongoClient("mongodb://localhost:27017/")
    mydb = myclient["anapaula_database"]
    mycol = mydb[collection]

    return mycol