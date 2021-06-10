import re


def extract_gene(results, genpanel):
    genes = {}
    diseases = {}
    results = results.split("\n")
    results_it = iter(results)
    for line in results_it:
        filterlist = []
        if re.match(r'^\d+\t\d+\t\d+\t', line) is not None:
            line_list = line.upper().strip().split('\t')
            articleid = line_list[0]
            name = line_list[3]
            annotype = line_list[4]
            if annotype == "GENE":
                if genpanel != "None":
                    for key in genpanel:
                        if name in key or name in list(key.values())[0]:
                            filterlist.append(name)
                if name in filterlist:
                    continue
                elif articleid in genes.keys() and name in genes[articleid]:
                    genes[articleid][2] += 1
                else:
                    try:
                        print(name, "toegevoegd")
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
