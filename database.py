import pymongo

def connect_db():
    myclient = pymongo.MongoClient("mongodb://localhost:27017/")
    mydb = myclient["anapaula_database"]
    mycol = mydb["employees"]

    return mycol