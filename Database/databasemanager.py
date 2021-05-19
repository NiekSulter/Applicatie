from pymongo import MongoClient
import uuid
from Processing import variables


class DatabaseManager:

    def __init__(self):
        usr = variables.MONGO_ATLAS_USER
        pwd = variables.MONGO_ATLAS_PASS
        self.client = MongoClient(
            f"mongodb+srv://{usr}:{pwd}@cluster0.thgnd.mongodb.net/myFirstDatabase?retryWrites=true&w=majority")
        self.db = self.client.Course8_test

    def insert_zoekopdracht(self, genes, diseases):
        collection = self.db.Zoekopdrachten

        uniqueid = str(uuid.uuid1())
        d = {"_id": uniqueid, "res": [genes, diseases]}

        self.db.collection.insert_one(d)

        return uniqueid

    def retreieve_zoekopdracht(self, userid):
        # collection = self.db.collection

        out = self.db.collection.find_one({"_id": userid})

        genes = out['res'][0]
        diseases = out['res'][1]

        return genes, diseases, userid

    def close_conn(self):
        self.client.close()
