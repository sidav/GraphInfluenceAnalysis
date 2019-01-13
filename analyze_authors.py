import networkx as nx

COUNT_MISSING_DATES = False
PRINT_TOP_N = 10
total_cites = cites_accounted = 0

def progressBar(title, value, endvalue, bar_length=20):
    import sys
    percent = float(value) / endvalue
    arrow = '-' * int(round(percent * bar_length) - 1) + '>'
    spaces = ' ' * (bar_length - len(arrow))

    sys.stdout.write("\r" + title + " [{0}] {1}% ({2} out of {3})".format(arrow + spaces, int(round(percent * 100)), value, endvalue))
    if value == endvalue:
        sys.stdout.write("\n")
    sys.stdout.flush()


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


########### MEAN CENTRALITY #########
def calculate_mean_of_values_for_keys(d1, d2, d3, d4):
    final_dict = {}
    for key in d1.keys():
        final_dict[key] = (d1[key]+d2[key]+d3[key]+d4[key]) / 4
    return final_dict


#######################################


def get_book_by_id(books_dict, requested_id):
    requested_id = int(requested_id)
    if len(books_dict) > requested_id:
        # TODO: dichotomia usage for faster search
        for actual_index in range(1, len(books_dict)):
            if len(books_dict[actual_index]['book_id']) > 0 and int(books_dict[actual_index]['book_id']) == requested_id:
                return books_dict[actual_index]


def get_list_of_similar_books_regarding_year(books_dict, book):
    global total_cites, cites_accounted
    sim_ids_list = ''
    for sim_id in book['book_similar'].split(';'):
        total_cites += 1
        sim_book = get_book_by_id(books_dict, sim_id)
        if COUNT_MISSING_DATES:
            if sim_book is not None and (
                    sim_book["book_release_year"] == '' or book["book_release_year"] == '' or int(
                    sim_book["book_release_year"]) < int(book["book_release_year"])):
                sim_ids_list += str(sim_id) + ';'
                cites_accounted += 1
        else:
            if sim_book is not None and (
                    sim_book["book_release_year"] != '' and book["book_release_year"] != '' and int(
                    sim_book["book_release_year"]) < int(book["book_release_year"])):
                sim_ids_list += str(sim_id) + ';'
                cites_accounted += 1
    return sim_ids_list


def get_author_index_by_name(adict, name):
    for i in range(len(adict)):
        author = adict[i]
        if author["name"] == name:
            return i
    return -1


def form_authors_dict(books_dict):
    authors = []
    for book_index in range(len(books_dict)):
        progressBar('Forming authors dict...', book_index, len(books_dict)-1, 20)
        book = books_dict[book_index]
        if book['book_id_exists'] == 'True' and len(book['book_similar']) > 0:
            author_not_exists = True
            for author in authors:
                if author['name'] == book['book_author']:
                    author['similar_to'] += get_list_of_similar_books_regarding_year(books_dict, book)
                    author['books'].append(book['book_id'])
                    author_not_exists = False
            if author_not_exists:
                authors.append({"name": book['book_author'], "similar_to": get_list_of_similar_books_regarding_year(books_dict, book), "books": [book["book_id"]]})
    return authors


def form_authors_graph(books_dict, authors_dict):
    g = nx.DiGraph()
    for index in range(0, len(authors_dict)):
        progressBar('Forming the authors graph... ', index, len(authors_dict)-1, 20)
        author = authors_dict[index]
        if len(author['similar_to']) > 0:
            splitted_list = author['similar_to'].split(';')
            if splitted_list[-1] == '':
                splitted_list = splitted_list[:-1]
            similar_list = list(map(lambda x: int(x), splitted_list))
            for i in similar_list:
                book = get_book_by_id(books_dict, i)
                if book is not None and book["book_author"] != author["name"]:
                    influentor = get_author_index_by_name(authors_dict, book["book_author"])
                    if influentor != -1:
                        # print("Added the influence of", authors_dict[influentor]["name"], "on", author["name"], "because of the book", book["book_title"])
                        g.add_edge(index, influentor)
                # else:
                #     print("No book found!")
    return g

##################################################


def print_top_n(adict, all_list):
    top = all_list[-PRINT_TOP_N:]
    for ind in reversed(range(PRINT_TOP_N)):
        i = top[ind]
        if len(adict) > i[0]:
            author = adict[i[0]]
            print(author["name"], i[1])
        else:
            print('Неопознанный автор')


def analyze_authors(books_dict):
    adict = form_authors_dict(books_dict)
    g = form_authors_graph(books_dict, adict)

    # MEASUREMENTS
    print()
    print('------- AUTHORS INFLUENCE ANALYSIS -------')
    print('Graph is built. Calculating in-degree centrality...')
    idg = normalize_dict(nx.in_degree_centrality(g))
    print_top_n(adict, sort_list(idg))

    print()
    print('Calculating closeness centrality...')
    cls = normalize_dict(nx.closeness_centrality(g))
    print_top_n(adict, sort_list(cls))

    print()
    print('Calculating harmonic centrality...')
    hrm = normalize_dict(nx.harmonic_centrality(g))
    print_top_n(adict, sort_list(hrm))

    print()
    print('Calculating PageRank centrality...')
    pgr = normalize_dict(nx.pagerank(g))
    print_top_n(adict, sort_list(pgr))

    print()
    print('Calculating mean centrality...')
    mean_centrality = normalize_dict(calculate_mean_of_values_for_keys(idg, cls, hrm, pgr))
    print_top_n(adict, sort_list(mean_centrality))

    print()
    print("TOTAL:", total_cites, "cites;", "ACCOUNTED:", cites_accounted, "cites.")
