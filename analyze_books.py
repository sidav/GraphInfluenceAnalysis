import networkx as nx

COUNT_MISSING_DATES = False

def sort_list(in_list):
    return sorted(in_list.items(), key=lambda x: x[1])


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


def analyze_books(books_dict):
    g = nx.DiGraph()

    # read all the books and append'em to the graph.
    for book in books_dict:
        if book['book_id_exists'] == 'True':
            book_id = int(book['book_id'])

            if len(book['book_similar']) > 0:
                book_similar_list = list(map(lambda x: int(x), book['book_similar'].split(';')))
                for i in book_similar_list:
                    sim_book = get_book_by_id(books_dict, i)
                    if COUNT_MISSING_DATES:
                        if sim_book is not None and (sim_book["book_release_year"] == '' or book["book_release_year"] == '' or int(sim_book["book_release_year"]) < int(book["book_release_year"])):
                            g.add_edge(book_id, i)
                    else:
                        if sim_book is not None and (sim_book["book_release_year"] != '' and book["book_release_year"] != '' and int(sim_book["book_release_year"]) < int(book["book_release_year"])):
                            g.add_edge(book_id, i)

    # MEASUREMENTS
    print('------- BOOKS INFLUENCE ANALYSIS -------')
    print('Graph is built. Calculating in-degree centrality...')
    top = sort_list(nx.in_degree_centrality(g))[-5:]
    for i in top:
        if len(books_dict) > i[0]:
            book = get_book_by_id(books_dict, int(i[0]))
            print(i[0], book['book_id'], '"' + book['book_title'] + '"', book['book_author'], "(" + book['book_release_year'] + ")", book['book_score'], i[1])
        else:
            print('Неопознанная книга, id =', i[0])

    print()
    print('Calculating closeness centrality...')
    top = sort_list(nx.closeness_centrality(g))[-5:]
    for i in top:
        if len(books_dict) > i[0]:
            book = get_book_by_id(books_dict, int(i[0]))
            print(i[0], book['book_id'], '"' + book['book_title'] + '"', book['book_author'], "(" + book['book_release_year'] + ")", book['book_score'], i[1])
        else:
            print('Неопознанная книга, id =', i[0])

    print()
    print('Calculating harmonic centrality...')
    top = sort_list(nx.harmonic_centrality(g))[-5:]
    for i in top:
        if len(books_dict) > i[0]:
            book = get_book_by_id(books_dict, int(i[0]))
            print(i[0], book['book_id'], '"' + book['book_title'] + '"', book['book_author'], "(" + book['book_release_year'] + ")", book['book_score'], i[1])
        else:
            print('Неопознанная книга, id =', i[0])

    print()
    print('Calculating PageRank centrality...')
    top = sort_list(nx.pagerank(g))[-5:]
    for i in top:
        if len(books_dict) > i[0]:
            book = get_book_by_id(books_dict, int(i[0]))
            print(i[0], book['book_id'], '"' + book['book_title'] + '"', book['book_author'], "(" + book['book_release_year'] + ")", book['book_score'], i[1])
        else:
            print('Неопознанная книга, id =', i[0])
