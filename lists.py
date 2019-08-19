import pandas as pd
import seaborn as sns
import numpy as np

def sort_list(in_list):
    return sorted(in_list.items(), key=lambda x: x[1])


# def correlation_between(list1, list2, top_n):  # lists are already sorted
#     correlated = 0
#     for elem in list1[-top_n:]:
#         for elem2 in list2[-top_n:]:
#             if elem[0] == elem2[0]:
#                 correlated += 1
#     return float(correlated) / float(top_n)
#
#
# def calc_corrs_for_dict(cents_dict, top_n):
#     print()
#     print("CUSTOM Centrality metrics correlation for top %d " % top_n)
#     already_checked = []
#     for key1 in cents_dict.keys():
#         for key2 in cents_dict.keys():
#             if key1 != key2 and key2 not in already_checked:
#                 print(" Between %s and %s: %.2f" % (key1, key2,
#                                                     correlation_between(cents_dict[key1], cents_dict[key2], top_n)))
#                 already_checked.append(key1)


def pandas_corr(cents_dict, top_n, fig_name):
    print()
    print("PANDAS Centrality metrics correlation for top %d " % top_n)
    prepared_dict = prepare_arrays_dict(cents_dict, top_n)
    result = calculate_pandas_corr(prepared_dict)
    plot_corr_to_file(result, fig_name)
    print(result)


def prepare_arrays_dict(cents_dict, top_n):
    new_dict = {}
    means = sort_list(cents_dict["Mean"])
    # now for a list of same ids order for each of the lists in cents_dict
    for key in cents_dict.keys():
        if key == "Mean":
            continue
        new_list = []
        for id, _ in means[-top_n:]:
            new_list.append((id, cents_dict[key][id]))
        new_dict[key] = new_list

    return new_dict


def calculate_pandas_corr(cents_dict):
    df = pd.DataFrame()
    for metricName in cents_dict.keys():
        df[metricName] = [i[1] for i in cents_dict[metricName]]
        # print(df[metricName])
    return df.corr(method='spearman')


def plot_corr_to_file(d, name):
    import matplotlib.pyplot as plt

    mask = np.zeros_like(d)
    mask[np.triu_indices_from(mask, k=1)] = True
    f, ax = plt.subplots(figsize=(5, 5))
    resmap = sns.heatmap(d, xticklabels=d.columns, yticklabels=d.columns, annot=True, fmt=".2f", ax=ax,
                         mask=mask, cmap="YlGn"
                         ).get_figure()

    resmap.savefig("corr_matrix_%s.png" % name)
