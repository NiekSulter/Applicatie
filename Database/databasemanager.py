from pymongo import MongoClient
import uuid
from Processing import variables


class DatabaseManager:
    """
    class om de interacties met de database te regelen
    """

    def __init__(self):
        """
        aanmaken van de connectie met de database
        """
        usr = variables.MONGO_ATLAS_USER
        pwd = variables.MONGO_ATLAS_PASS
        self.client = MongoClient(
            f"mongodb+srv://{usr}:{pwd}@cluster0.thgnd.mongodb.net/myFirstDatabase?retryWrites=true&w=majority")
        self.db = self.client.Course8_test

    def insert_zoekopdracht(self, genes, diseases, query):
        """
        inserten van een zoekopdracht in de database
        :param genes: dictionary met genen
        :param diseases: dictionary met diseases
        :param query: de door de gebruiker ingevoerde zoek query
        :return: een universally unique identifier die de zoekopdracht
        identificeert
        """
        collection = self.db.Zoekopdrachten

        # uuid wordt gegenereerd
        uniqueid = str(uuid.uuid1())

        # de twee meegegeven dicts worden samen met de query en het uuid in een
        # nieuwe dict gestopt, deze wordt geinsert in de database.
        d = {"_id": uniqueid, "res": [genes, diseases], "query": query}

        self.db.collection.insert_one(d)

        return uniqueid

    def retreieve_zoekopdracht(self, userid):
        """
        functie om een zoekopdracht op te halen uit de database
        :param userid: een universally unique identifier die de zoekopdracht
        identificeert
        :return: de onderdelen van de zoekopdracht, twee dicts met de genes
        & diseases, het uuid van de zoekopdracht en de gebruikte query
        """
        out = self.db.collection.find_one({"_id": userid})

        genes = out['res'][0]
        diseases = out['res'][1]
        query = out['query']

        return genes, diseases, userid, query

    def insert_genpanels(self, genpanel_dict):
        """
        functie om de genpanels uit het genpanel bestand te inserten
        in de database
        :param genpanel_dict: een dictionary met de genpanels
        :return: None
        """
        for key, value in genpanel_dict.items():
            self.db.genpanels.insert_one({"_id": key, "genes": value})

    def retrieve_genpanel_ids(self):
        """
        functie om de genpanel namen op te halen uit de database, met deze
        functie worden alleen de namen opgehaald voor de website.
        :return: een lijst met de namen van de genpanels
        """
        out = []
        for i in self.db.genpanels.distinct("_id"):
            out.append(i)

        return out

    def retrieve_genpanel(self, gp):
        """
        functie om de genpanel namen op te halen uit de database
        :return: een lijst met de genpanels
        """
        out = self.db.genpanels.find_one({"_id": gp})

        gp = out["genes"]

        return gp

    def close_conn(self):
        """
        functie om de connectie met de database te sluiten
        :return: None
        """
        self.client.close()
