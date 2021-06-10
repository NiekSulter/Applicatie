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
    results_it = iter(results)
    for line in results_it:
        filterlist = []
        print(line)
        if re.match(r'^\d+\t\d+\t\d+\t', line) is not None:
            line_list = line.upper().strip().split('\t')
            articleid = line_list[0]
            name = line_list[3]
            annotype = line_list[4]
            if annotype == "GENE":
                # if genpanel != "None":
                #     for key in genpanel:
                #         if name in key or name in list(key.values())[0]:
                #             filterlist.append(name)
                # if name in filterlist:
                #     continue
                if articleid not in genes.keys():
                    genes[articleid] = {}
                    try:
                        genes[articleid][name] = [name, line_list[5], 1]
                    except IndexError:
                        genes[articleid][name] = [name, '-', 1]
                elif articleid in genes.keys():
                    if name in genes[articleid].keys():
                        genes[articleid][name][2] += 1
                    else:
                        try:
                            genes[articleid][name] = [name, line_list[5], 1]
                        except IndexError:
                            genes[articleid][name] = [name, '-', 1]
            elif annotype == "DISEASE":
                if articleid not in diseases.keys():
                    diseases[articleid] = {}
                    try:
                        diseases[articleid][name] = [name, line_list[5], 1]
                    except IndexError:
                        diseases[articleid][name] = [name, '-', 1]
                elif articleid in diseases.keys():
                    if name in diseases[articleid].keys():
                        diseases[articleid][name][2] += 1
                    else:
                        try:
                            diseases[articleid][name] = [name, line_list[5], 1]
                        except IndexError:
                            diseases[articleid][name] = [name, '-', 1]

    return genes, diseases
