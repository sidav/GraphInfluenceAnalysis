import networkx as nx


class book_with_ratings:
    id = 0
    idg = harm = clos = pr = 0.0


def normalize(dct): # makes all the values in range [0,1]
    lowest_val = 9999999.0
    highest_val = 0.0
    for key, value in dct.items():
        if value < lowest_val:
            lowest_val = value
        if value > highest_val:
            highest_val = value
            print(key)
    for key in dct.keys():
        dct[key] = (dct[key] - lowest_val) / (highest_val - lowest_val)
    return dct


def calculate_total_measurement(graph):
    print()
    lst = []
    idg = normalize(nx.in_degree_centrality(graph))
    cls = normalize(nx.closeness_centrality(graph))
    hrm = normalize(nx.harmonic_centrality(graph))
    pgr = normalize(nx.pagerank(graph))

    print(idg)
    # print(idg[4325])
