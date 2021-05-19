from Bio import Entrez
import requests
from Processing import parse_pubtator_output
#from .variables import NCBI_API_KEY, NCBI_API_MAIL


def build_term(TOR, TAND):
    term = ""
    AND = ' AND '.join(TOR)
    OR = ' OR '.join(TAND)

    term = AND + " OR " + OR

    print(term)

    return term


def article_search(term, date):
    print(date)

    handle = Entrez.esearch(db="pubmed", term=term, field="title",
                            mindate=date)
    record = Entrez.read(handle)
    handle.close()

    idList = record['IdList']
    return idList


def annotate_search(idList):
    ids = ','.join(idList)

    url = f"https://www.ncbi.nlm.nih.gov/research/pubtator-api/publications" \
          f"/export/pubtator?pmids={ids}&concepts=gene,disease"
    result = requests.get(url)

    genes, diseases = parse_pubtator_output.extract_gene(result.text)

    return genes, diseases


def make_request(TOR, TAND, date):
    #Entrez.email = NCBI_API_MAIL
    #Entrez.api_key = NCBI_API_KEY

    term = build_term(TOR, TAND)
    idList = article_search(term, date)

    return annotate_search(idList)

'''
class PubmedPipeline:

    def __init__(self):
        self.API_email = NCBI_API_MAIL
        self.API_KEY = NCBI_API_KEY

    def build_term(self, TOR, TAND):
        term = ""
        AND = ' AND '.join(TOR)
        OR = ' OR '.join(TAND)

        term = AND + " OR " + OR

        return term

    def article_search(self, term, date):
        print(date)

        handle = Entrez.esearch(db="pubmed", term=term, field="title",
                                mindate=date)
        record = Entrez.read(handle)
        handle.close()

        idList = record['IdList']
        return idList

    def pubtator_annotation(self, idList):
        ids = ','.join(idList)

        url = f"https://www.ncbi.nlm.nih.gov/research/pubtator-api/publications" \
              f"/export/pubtator?pmids={ids}&concepts=gene"
        result = requests.get(url)

        print(result.text)
'''
