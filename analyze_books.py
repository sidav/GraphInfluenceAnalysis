import networkx as nx

COUNT_MISSING_DATES = False
PRINT_TOP_N = 10


def normalize_dict(dct):  # makes all the values in range [0,1]
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


def sort_list(in_list):
    return sorted(in_list.items(), key=lambda x: x[1])


def progressBar(title, value, endvalue, bar_length=20):
    import sys
    percent = float(value) / endvalue
    arrow = '-' * int(round(percent * bar_length) - 1) + '>'
    spaces = ' ' * (bar_length - len(arrow))

    sys.stdout.write("\r" + title + " [{0}] {1}% ({2} out of {3})".format(arrow + spaces, int(round(percent * 100)), value, endvalue))
    if value == endvalue:
        sys.stdout.write("\n")
    sys.stdout.flush()


def get_book_by_id(books_dict, requested_id):
    requested_id = int(requested_id)
    if len(books_dict) > requested_id:
        # TODO: dichotomia usage for faster search
        # actual_index = requested_id-1
        # curr_id = 0
        # while curr_id != requested_id:
        #     curr_id = int(books_dict[actual_index]['book_id'])
        #     if curr_id < requested_id:
        #         actual_index = curr_id + (requested_id - curr_id) // 2 - 1
        #     elif curr_id > requested_id:
        #         actual_index = requested_id + (curr_id - requested_id) // 2 - 1
        for actual_index in range(1, len(books_dict)):
            if len(books_dict[actual_index]['book_id']) > 0 and int(books_dict[actual_index]['book_id']) == requested_id:
                return books_dict[actual_index]


########### MEAN CENTRALITY #########


def calculate_mean_of_values_for_keys(d1, d2, d3, d4):
    final_dict = {}
    for key in d1.keys():
        final_dict[key] = (d1[key]+d2[key]+d3[key]+d4[key]) / 4
    return final_dict


def calculate_mean_centrality(graph):
    idg = normalize_dict(nx.in_degree_centrality(graph))
    cls = normalize_dict(nx.closeness_centrality(graph))
    hrm = normalize_dict(nx.harmonic_centrality(graph))
    pgr = normalize_dict(nx.pagerank(graph))
    final = normalize_dict(calculate_mean_of_values_for_keys(idg, cls, hrm, pgr))
    return final
    # print(idg[4325])


##########################################################


def print_top_n(books_dict, all_list):
    top = all_list[-PRINT_TOP_N:]
    for ind in reversed(range(PRINT_TOP_N)):
        i = top[ind]
        if len(books_dict) > i[0]:
            book = get_book_by_id(books_dict, int(i[0]))
            print(i[0], book['book_id'], '"' + book['book_title'] + '"', book['book_author'], "(" + book['book_release_year'] + ")", book['book_score'], i[1])
        else:
            print('Неопознанная книга, id =', i[0])


def analyze_books(books_dict):
    g = nx.DiGraph()

    # read all the books and append'em to the graph.
    cites_accounted = 0
    total_cites = 0
    for book_index in range(len(books_dict)):
        progressBar("Building the books influence graph...", book_index, len(books_dict)-1, 20)
        book = books_dict[book_index]
        if book['book_id_exists'] == 'True':
            book_id = int(book['book_id'])

            if len(book['book_similar']) > 0:
                book_similar_list = list(map(lambda x: int(x), book['book_similar'].split(';')))
                for i in book_similar_list:
                    total_cites += 1
                    sim_book = get_book_by_id(books_dict, i)
                    if COUNT_MISSING_DATES:
                        if sim_book is not None and (sim_book["book_release_year"] == '' or book["book_release_year"] == '' or int(sim_book["book_release_year"]) < int(book["book_release_year"])):
                            cites_accounted += 1
                            g.add_edge(book_id, i)
                    else:
                        if sim_book is not None and (sim_book["book_release_year"] != '' and book["book_release_year"] != '' and int(sim_book["book_release_year"]) < int(book["book_release_year"])):
                            cites_accounted += 1
                            g.add_edge(book_id, i)

    # MEASUREMENTS
    print('------- BOOKS INFLUENCE ANALYSIS -------')
    print('Graph is built. Calculating in-degree centrality...')
    print_top_n(books_dict,sort_list(normalize_dict(nx.in_degree_centrality(g))))

    print()
    print('Calculating closeness centrality...')
    print_top_n(books_dict,sort_list(normalize_dict(nx.closeness_centrality(g))))

    print()
    print('Calculating harmonic centrality...')
    print_top_n(books_dict,sort_list(normalize_dict(nx.harmonic_centrality(g))))


    print()
    print('Calculating PageRank centrality...')
    print_top_n(books_dict,sort_list(normalize_dict(nx.pagerank(g))))

    print()
    print('Calculating mean centrality...')
    print_top_n(books_dict, sort_list(calculate_mean_centrality(g)))

    print()
    print("TOTAL:", total_cites, "cites;", "ACCOUNTED:", cites_accounted, "cites.")
