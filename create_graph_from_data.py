import pandas as pd
import networkx as nx
import matplotlib.pyplot as plt


seconds_in_a_day = 86400


def extract_satellite_names_from_analysis_label(analysis_label: str):
    return analysis_label.split(" sees ")


def create_graph_from_data(filepath):
    # TODO: pre-process SOAP data

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

        if (percent_true == 0):
            return

        G.add_edge(nodes_for_edge[0], nodes_for_edge[1], weight=percent_true)

    [add_edge_from_row(row) for index, row in dataframe.iterrows()]

    print('eigenvector_centrality', nx.eigenvector_centrality(G))
    print('betweenness_centrality', nx.betweenness_centrality(G))
    print('current_flow_betweenness_centrality',
          nx.current_flow_betweenness_centrality(G))

    # 4. Visualize the graph
    # elarge = [(u, v) for (u, v, d) in G.edges(data=True) if d["weight"] > 0.5]
    # esmall = [(u, v) for (u, v, d) in G.edges(data=True) if d["weight"] <= 0.5]

    # pos = nx.spring_layout(G)  # positions for all nodes

    # # nodes
    # nx.draw_networkx_nodes(G, pos, node_size=700)

    # # edges
    # nx.draw_networkx_edges(G, pos, edgelist=elarge, width=6)
    # nx.draw_networkx_edges(
    #     G, pos, edgelist=esmall, width=6, alpha=0.5, edge_color="b", style="dashed"
    # )

    # # labels
    # nx.draw_networkx_labels(G, pos, font_size=20, font_family="sans-serif")

    # plt.axis("off")
    # plt.show()


if __name__ == "__main__":
    create_graph_from_data('./data/sample_soap_pared_down.csv')
