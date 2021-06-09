import pandas
import re
from Database.databasemanager import DatabaseManager


def read_file(bestand):
    df = pandas.read_excel(bestand, dtype=str)
    df = df[df.columns[df.columns.isin(['Symbol_HGNC', 'Aliases', 'GenePanels_Symbol', 'GenePanel', 'GenePanelCount'])]]
    Symbols = df["Symbol_HGNC"].values
    Aliases = df["Aliases"].values
    GenePanel_symbols = df["GenePanels_Symbol"].values
    GenePanel = df["GenePanel"].values
    GenePanelCount = df["GenePanelCount"].values
    return df


def make_dict(df):
    genepanel_dict = {}
    aliases_dict = {}
    for index, row in df.iterrows():

        line = row["GenePanel"]

        m = re.findall("(?<=\().+?(?=\))", line)

        # [line.replace(";", ",") for g in m.groups() if ";" in g]

        for x in m:
            line = line.replace(x, x.replace(";", ","))


        panels = line.split(";")#regex maken die kijk of er haakjes staan om de ";"

        # print(panels)

        symbol = row['Symbol_HGNC']
        aliases = row['Aliases']
        #if isinstance(aliases, float):
        #    aliases_dict[symbol] = []

        #else:
        #    split_aliases = aliases.split("|")
        #    aliases_dict[symbol] = split_aliases
        for i in range(len(panels)):
            if isinstance(aliases, float):
                aliases_dict[symbol] = []
            else:
                split_aliases = aliases.split("|")
                aliases_dict[symbol] = split_aliases

            if panels[i] in genepanel_dict.keys():
                genepanel_dict[panels[i]].append(aliases_dict)
            else:
                genepanel_dict[panels[i]] = [aliases_dict]
            aliases_dict = {}
    return genepanel_dict


def main():
    bestand = "GenPanelOverzicht_DG-3.1.0_HAN.xlsx"
    df = read_file(bestand)
    genepanel_dict = make_dict(df)

    dbm = DatabaseManager()

    dbm.insert_genpanels(genepanel_dict)

    dbm.close_conn()




main()

