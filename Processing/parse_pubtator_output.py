import re


def extract_gene(results):
    genes = {}
    diseases = {}
    results = results.split("\n")
    for line in results:
        if re.match(r'^\d+\t\d+\t\d+\t', line) is not None:
            line_list = line.upper().strip().split('\t')
            name = line_list[3]
            anno_type = line_list[4]
            if anno_type == "GENE":
                if name in genes.keys():
                    genes[name][2] += 1
                else:
                    genes[name] = [line_list[0], line_list[5], 1]
            elif anno_type == "DISEASE":
                if anno_type in diseases:
                    genes[name][2] += 1
                else:
                    genes[name] = [line_list[0], line_list[5], 1]

    return genes, diseases
