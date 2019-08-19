import pandas as pd
import seaborn as sns
import numpy as np

def sort_list(in_list):
    return sorted(in_list.items(), key=lambda x: x[1])


def correlation_between(list1, list2, top_n):  # lists are already sorted
    correlated = 0
    for elem in list1[-top_n:]:
        for elem2 in list2[-top_n:]:
            if elem[0] == elem2[0]:
                correlated += 1
    return float(correlated) / float(top_n)


def calc_corrs_for_dict(cents_dict, top_n):
    print()
    print("CUSTOM Centrality metrics correlation for top %d " % top_n)
    already_checked = []
    for key1 in cents_dict.keys():
        for key2 in cents_dict.keys():
            if key1 != key2 and key2 not in already_checked:
                print(" Between %s and %s: %.2f" % (key1, key2,
                                                    correlation_between(cents_dict[key1], cents_dict[key2], top_n)))
                already_checked.append(key1)


def pandas_corr(cents_dict, top_n, fig_name):
    print()
    print("PANDAS Centrality metrics correlation for top %d " % top_n)
    df = pd.DataFrame()
    for metricName in cents_dict.keys():
        df[metricName] = [i[1] for i in cents_dict[metricName][-top_n:]]
        # print(df[metricName])
    result = df.corr()
    plot_corr_to_file(result, fig_name)
    print(result)


def plot_corr_to_file(result, name):
    mask = np.zeros_like(result)
    mask[np.triu_indices_from(mask, k=1)] = True
    resmap = sns.heatmap(result, xticklabels=result.columns, yticklabels=result.columns, annot=True, mask=mask,
                         cmap="YlGn").get_figure()
    resmap.savefig("corr_matrix_%s.png" % name)
