import pandas

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
        panels = row["GenePanel"].split(";")#regex maken die kijk of er haakjes staan om de ";"
        symbol = row['Symbol_HGNC']
        aliases = row['Aliases']
        if isinstance(aliases, float):
            aliases_dict[symbol] = []

        else:
            split_aliases = aliases.split("|")
            aliases_dict[symbol] = split_aliases
        for i in panels:
            if i in genepanel_dict.keys():
                genepanel_dict[i].append(symbol)
            else:
                genepanel_dict[i] = [symbol]
    return aliases_dict, genepanel_dict


def main():
    bestand = "GenPanelOverzicht_DG-3.1.0_HAN.xlsx"
    df = read_file(bestand)
    aliases_dict, genepanel_dict = make_dict(df)


main()
