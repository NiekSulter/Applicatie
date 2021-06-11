from Bio import Entrez
import requests
from Processing import parse_pubtator_output
from Database.databasemanager import DatabaseManager


def article_search(term, date):
    """
    Makes an entrez search using search terms and a date.
    :param term: search query
    :param date: date inputted by the user
    :return: a list containing all ID's from the entrez request
    """

    handle = Entrez.esearch(db="pubmed", term=term, mindate=date)
    record = Entrez.read(handle)
    handle.close()

    idList = record['IdList']
    return idList


def annotate_search(idList, genpanel):
    """
    Makes a search request using the pubtator api, then extracts and formats the results.
    :param idList: list with article ids
    :param term: search query
    :return: dictionaries with the genes and diseases
    """
    ids = ','.join(idList)

    url = f"https://www.ncbi.nlm.nih.gov/research/pubtator-api/publications" \
          f"/export/pubtator?pmids={ids}&concepts=gene,disease"
    result = requests.get(url)

    genes, diseases = parse_pubtator_output.extract_gene(result.text, genpanel)

    return genes, diseases


def database_insert(genes, diseases, term, genpanel, date):
    """
    Makes a DatabaseManager instance to insert the search into the database.
    :param genes: dictionary with genes
    :param diseases: dictionary with diseases
    :param term: search query
    :return: universally unique identifier which identifies the search
        query.
    """

    dm = DatabaseManager()

    uuid = dm.insert_zoekopdracht(genes, diseases, term, genpanel, date)

    dm.close_conn()

    return uuid


def get_panel(genpanel):
    """
    If the user selected a genpanel to exclude in the search, this function
    will retrieve aforementioned genpanel from the database.
    :param genpanel: user selected genpanel
    :return: user selected genpanel OR None if no genpanel was selected
    """
    if genpanel != "None":
        dm = DatabaseManager()

        gp = dm.retrieve_genpanel(genpanel)

        dm.close_conn()

        return gp

    else:

        return genpanel


def make_request(term, date, email, genpanel):
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

    gp = get_panel(genpanel)

    genes, diseases = annotate_search(idList, gp)

    return database_insert(genes, diseases, term, genpanel, date)

