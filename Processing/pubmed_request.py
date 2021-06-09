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
    print(date)

    handle = Entrez.esearch(db="pubmed", term=term, mindate=date)
    record = Entrez.read(handle)
    handle.close()

    idList = record['IdList']
    return idList


def annotate_search(idList, term):
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
    Entrez.email = email
    #Entrez.api_key = NCBI_API_KEY

    idList = article_search(term, date)

    return annotate_search(idList, term)

