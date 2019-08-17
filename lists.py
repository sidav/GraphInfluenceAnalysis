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
    already_checked = []
    for key1 in cents_dict.keys():
        for key2 in cents_dict.keys():
            if key1 != key2 and key2 not in already_checked:
                print(" Between %s and %s: %.2f" % (key1, key2,
                                                    correlation_between(cents_dict[key1], cents_dict[key2], top_n)))
                already_checked.append(key1)
