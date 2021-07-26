import pandas as pd
import networkx as nx


seconds_in_a_day = 86400


def extract_satellite_names_from_analysis_label(analysis_label: str):
    return analysis_label.split(" sees ")


def create_graph_from_data(filepath):
    dataframe = pd.read_csv(filepath)

    # 1. Get all of the satellite names from the "Anlaysis" column
    satellite_name_arrays = [extract_satellite_names_from_analysis_label(
        x) for x in dataframe["Analysis"]]
    satellite_names_with_duplicates = [
        item for sublist in satellite_name_arrays for item in sublist]
    satellite_name_list = list(set(satellite_names_with_duplicates))

    # 2. Create nodes in graphs with labels of the satellites
    G = nx.Graph()
    G.add_nodes_from(satellite_name_list)

    # 3. Create graph where edges weights is percent true
    # e.g. G.add_edge("a", "b", weight=0.6)

    def add_edge_from_row(row):
        nodes_for_edge = extract_satellite_names_from_analysis_label(
            row["Analysis"])
        time_true = row["Time True"]
        percent_true = time_true / seconds_in_a_day

        G.add_edge(nodes_for_edge[0], nodes_for_edge[1], weight=percent_true)

    [add_edge_from_row(row) for index, row in dataframe.iterrows()]

    print(G.nodes(), G.edges())


if __name__ == "__main__":
    create_graph_from_data('./data/sample_soap_pared_down.csv')
