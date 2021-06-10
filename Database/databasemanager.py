from pymongo import MongoClient
import uuid
from Processing import variables


class DatabaseManager:
    """
    Management class for database interactions
    """

    def __init__(self):
        """
        Starting database connection
        """
        usr = variables.MONGO_ATLAS_USER
        pwd = variables.MONGO_ATLAS_PASS
        self.client = MongoClient(
            f"mongodb+srv://{usr}:{pwd}@cluster0.thgnd.mongodb.net/myFirstDatabase?retryWrites=true&w=majority")
        self.db = self.client.Course8_test

    def insert_zoekopdracht(self, genes, diseases, query):
        """
        inserting a search into the database
        :param genes: dictionary with genes
        :param diseases: dictionary with diseases
        :param query: the user submitted query
        :return: universally unique identifier which identifies the search
        query.
        """
        collection = self.db.Zoekopdrachten

        # generating the uuid
        uniqueid = str(uuid.uuid1())

        # the genes and diseases dictionaries are combined into a new dict
        # along with the uuid and search query. This datastructure
        # encapsulates a single search
        d = {"_id": uniqueid, "res": [genes, diseases], "query": query}

        self.db.collection.insert_one(d)

        return uniqueid

    def retreieve_zoekopdracht(self, userid):
        """
        function for retrieving a single search from the database
        :param userid: universally unique identifier which identifies a single
        search
        :return: the two dictionaries with genes & diseases,
        the uuid and the search query
        """

        print("USERID", userid)

        out = self.db.collection.find_one({"_id": userid})

        print("OUT", out)

        genes = out['res'][0]
        diseases = out['res'][1]
        query = out['query']

        return genes, diseases, userid, query

    def insert_genpanels(self, genpanel_dict):
        """
        function for inserting the genpanels into the database
        :param genpanel_dict: a dictionary with the genpanels
        :return: None
        """
        for key, value in genpanel_dict.items():
            self.db.genpanels.insert_one({"_id": key, "genes": value})

    def retrieve_genpanel_ids(self):
        """
        functie om de genpanel namen op te halen uit de database, met deze
        functie worden alleen de namen opgehaald voor de website.

        function for retrieving the genpanel names, to keep the loading times
        as low as possible only the names are retrieved
        :return: a list with the genpanel names
        """
        out = []
        for i in self.db.genpanels.distinct("_id"):
            out.append(i)

        return out

    def retrieve_genpanel(self, gp):
        """
        function to retrieve a single complete genpanel from the database
        :return: the user selected genpanel
        """
        out = self.db.genpanels.find_one({"_id": gp})

        gp = out["genes"]

        return gp

    def close_conn(self):
        """
        function to close the database connection
        :return: None
        """
        self.client.close()
