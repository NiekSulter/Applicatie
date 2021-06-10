import re


def extract_gene(results):
    """
    Extracts the genes and diseases from the annotated search results.
    :param results:
    :return: genes, diseases. two dictionaries containing gene names, nr. of occurences and original article ID's
    """
    genes = {}
    diseases = {}
    results = results.split("\n")
    for line in results:
        if re.match(r'^\d+\t\d+\t\d+\t', line) is not None:
            line_list = line.upper().strip().split('\t')
            articleid = line_list[0]
            name = line_list[3]
            annotype = line_list[4]
            if annotype == "GENE":
                if articleid in genes.keys() and name in genes[articleid]:
                    genes[articleid][2] += 1
                else:
                    try:
                        genes[articleid] = [name, line_list[5], 1]
                    except IndexError:
                        genes[articleid] = [name, '-', 1]
            elif annotype == "DISEASE":
                if articleid in diseases.keys() and name in diseases[articleid]:
                    diseases[articleid][2] += 1
                else:
                    try:
                        diseases[articleid] = [name, line_list[5], 1]
                    except IndexError:
                        diseases[articleid] = [name, '-', 1]

    return genes, diseases
