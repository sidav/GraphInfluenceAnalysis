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
    for key in dct.keys():
        dct[key] = (dct[key] - lowest_val) / (highest_val - lowest_val)
    return dct


def get_mean_for_dicts_values(d1, d2, d3, d4):
    final_dict = {}
    for key in d1.keys():
        final_dict[key] = (d1[key]+d2[key]+d3[key]+d4[key]) / 4
    return final_dict


def calculate_total_measurement(graph):
    idg = normalize(nx.in_degree_centrality(graph))
    cls = normalize(nx.closeness_centrality(graph))
    hrm = normalize(nx.harmonic_centrality(graph))
    pgr = normalize(nx.pagerank(graph))
    final = normalize(get_mean_for_dicts_values(idg, cls, hrm, pgr))
    return final
    # print(idg[4325])
