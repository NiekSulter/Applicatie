from Bio import Entrez
import requests
from Processing import parse_pubtator_output
from Database.databasemanager import DatabaseManager


# def build_term(TOR, TAND):
#     term = ""
#     AND = ' AND '.join(TOR)
#     OR = ' OR '.join(TAND)
#
#     term = AND + " OR " + OR
#
#     print(term)
#
#     return term


def article_search(term, date):
    """
    Makes an entrez search using search terms and a date.
    :param term:
    :param date:
    :return: a list containing all ID's from the entrez request
    """
    print(date)

    handle = Entrez.esearch(db="pubmed", term=term, mindate=date)
    record = Entrez.read(handle)
    handle.close()

    idList = record['IdList']
    return idList


def annotate_search(idList, term):
    """
    Makes a search request using the pubtator api, then extracts and formats the results.
    :param idList:
    :param term:
    :return:
    """
    ids = ','.join(idList)

    url = f"https://www.ncbi.nlm.nih.gov/research/pubtator-api/publications" \
          f"/export/pubtator?pmids={ids}&concepts=gene,disease"
    result = requests.get(url)

    genes, diseases = parse_pubtator_output.extract_gene(result.text)

    dm = DatabaseManager()

    uuid = dm.insert_zoekopdracht(genes, diseases, term)

    dm.close_conn()

    return genes, diseases, uuid


def make_request(term, date, email):
    """
    Entry point of the script, calls functions that do the actual request
    :param term: search terms given by the user
    :param date: date inputted by the user
    :param email: email inputted by the user
    :return: Returns the annotated results of the search request in a predetermined format
    """
    Entrez.email = email
    #Entrez.api_key = NCBI_API_KEY

    idList = article_search(term, date)

    return annotate_search(idList, term)

