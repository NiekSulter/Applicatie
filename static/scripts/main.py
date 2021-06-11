import pandas
import re
from Database.databasemanager import DatabaseManager


def read_file(file):
    """ reads file with pandas, and converts it into a dataframe.
    :param file
    :return: df(dataframe)
    """
    df = pandas.read_excel(file, dtype=str)
    df = df[df.columns[df.columns.isin(['Symbol_HGNC',
                                        'Aliases', 'GenePanels_Symbol',
                                        'GenePanel', 'GenePanelCount'])]]
    return df


def make_dict(df):
    """ Makes a nested dictionary of the useful data from the dataframe
    :param df(dataframe):
    :return genepanel_dict(nested dictionary):
    """
    # Makes 2 empty dictionaries
    genepanel_dict = {}
    aliases_dict = {}
    # Regex to replace a ; with , if the ; is within ().
    for index, row in df.iterrows():

        line = row["GenePanel"]

        m = re.findall("(?<=\().+?(?=\))", line)

        for x in m:
            line = line.replace(x, x.replace(";", ","))

        # Spilts the panels if there are multiple
        panels = line.split(";")

        symbol = row['Symbol_HGNC']
        aliases = row['Aliases']
        for i in range(len(panels)):
            # Sometimes there are no aliases, if this is the case no value
            # is added to the dictionary
            if isinstance(aliases, float):
                aliases_dict[symbol] = []
            else:
                # if there are multple aliases they are split, and added
                # to the dictionary
                split_aliases = aliases.split("|")
                aliases_dict[symbol] = split_aliases
            # A nested dictionary is made, or new data is added to it
            if panels[i] in genepanel_dict.keys():
                genepanel_dict[panels[i]].append(aliases_dict)
            else:
                genepanel_dict[panels[i]] = [aliases_dict]
            # Empties the aliases dict
            aliases_dict = {}
    return genepanel_dict


def main():
    file = "GenPanelOverzicht_DG-3.1.0_HAN.xlsx"
    df = read_file(file)
    genepanel_dict = make_dict(df)

    dbm = DatabaseManager()

    dbm.insert_genpanels(genepanel_dict)

    dbm.close_conn()


main()
