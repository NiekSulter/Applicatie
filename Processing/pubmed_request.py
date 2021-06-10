from Bio import Entrez
import requests
from Processing import parse_pubtator_output
from Database.databasemanager import DatabaseManager


def article_search(term, date):
    """
    functie om artikelen van pubmed op te halen.
    :param term: de zoekterm die door de gebruiker is ingevoerd op de website
    :param date: de datum die door de gebruiker is ingevoerd op de website
    :return: een lijst met de pubmed id's van alle gevonden artikelen
    """
    handle = Entrez.esearch(db="pubmed", term=term, mindate=date)
    record = Entrez.read(handle)
    handle.close()

    idList = record['IdList']
    return idList


def annotate_search(idList, genpanel):
    """
    functie om de gevonden artikelen op pubmet te annoteren m.b.v. de pubtator
    api
    :param idList: een lijst met de pubmed id's van alle gevonden artikelen
    :return: twee dictionaries, een met genen en een met diseases.
    """
    ids = ','.join(idList)

    url = f"https://www.ncbi.nlm.nih.gov/research/pubtator-api/publications" \
          f"/export/pubtator?pmids={ids}&concepts=gene,disease"
    result = requests.get(url)

    genes, diseases = parse_pubtator_output.extract_gene(result.text, genpanel)

    return genes, diseases


def database_insert(genes, diseases, term):
    """
    functie voor het inserten van een zoekopdracht in de database
    :param genes: dictionary met gevonden genen-
    :param diseases: dictionary met gevonden diseases
    :param term: de zoekterm die door de gebruiker is ingevoerd op de website
    :return: een universally unique identifier die de zoekopdracht
    identificeert
    """
    dm = DatabaseManager()

    uuid = dm.insert_zoekopdracht(genes, diseases, term)

    dm.close_conn()

    return uuid


def make_request(term, date, email, genpanel):
    """
    functie om de request pipeline aan te sturen
    :param term: de zoekterm die door de gebruiker is ingevoerd op de website
    :param date: de datum die door de gebruiker is ingevoerd op de website
    :param email: de email die door de gebruiker is ingevoerd op de website
    :return: een universally unique identifier die de zoekopdracht
    identificeert
    """
    Entrez.email = email

    idList = article_search(term, date)

    dm = DatabaseManager()

    if genpanel != "None":
        gp = dm.retrieve_genpanel(genpanel)
    else:
        gp = "None"

    genes, diseases = annotate_search(idList, gp)

    return database_insert(genes, diseases, term)
