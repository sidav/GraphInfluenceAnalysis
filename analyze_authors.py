import networkx as nx


def sort_list(in_list):
    return sorted(in_list.items(), key=lambda x: x[1])


def get_book_by_id(books_dict, requested_id):
    requested_id = int(requested_id)
    if len(books_dict) > requested_id:
        # TODO: dichotomia usage for faster search
        for actual_index in range(1, len(books_dict)):
            if len(books_dict[actual_index]['book_id']) > 0 and int(books_dict[actual_index]['book_id']) == requested_id:
                return books_dict[actual_index]


def get_author_index_by_name(adict, name):
    for i in range(len(adict)):
        author = adict[i]
        if author["name"] == name:
            return i
    return -1


def form_authors_dict(books_dict):
    authors = []
    for book in books_dict:
        if book['book_id_exists'] == 'True' and len(book['book_similar']) > 0:
            author_not_exists = True
            for author in authors:
                if author['name'] == book['book_author']:
                    author['similar_to'] += book['book_similar']
                    author['books'].append(book['book_id'])
                    author_not_exists = False
            if author_not_exists:
                authors.append({"name": book['book_author'], "similar_to": book['book_similar'], "books": [book["book_id"]]})
    return authors


def form_authors_graph(books_dict, authors_dict):
    g = nx.DiGraph()
    for index in range(0, len(authors_dict)):
        author = authors_dict[index]
        if len(author['similar_to']) > 0:
            similar_list = list(map(lambda x: int(x), author['similar_to'].split(';')))
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


def analyze_authors(books_dict):
    adict = form_authors_dict(books_dict)
    g = form_authors_graph(books_dict, adict)

    # MEASUREMENTS
    print('------- AUTHORS INFLUENCE ANALYSIS -------')
    print('Graph is built. Calculating in-degree centrality...')
    top = sort_list(nx.in_degree_centrality(g))[-5:]
    for i in top:
        if len(adict) > i[0]:
            author = adict[i[0]]
            print(author["name"], i[1])
        else:
            print('Неопознанный автор')

    print()
    print('Calculating closeness centrality...')
    top = sort_list(nx.closeness_centrality(g))[-5:]
    for i in top:
        if len(adict) > i[0]:
            author = adict[i[0]]
            print(author["name"], i[1])
        else:
            print('Неопознанный автор')

    print()
    print('Calculating harmonic centrality...')
    top = sort_list(nx.harmonic_centrality(g))[-5:]
    for i in top:
        if len(adict) > i[0]:
            author = adict[i[0]]
            print(author["name"], i[1])
        else:
            print('Неопознанный автор')

    print()
    print('Calculating PageRank centrality...')
    top = sort_list(nx.pagerank(g))[-5:]
    for i in top:
        if len(adict) > i[0]:
            author = adict[i[0]]
            print(author["name"], i[1])
        else:
            print('Неопознанный автор')
