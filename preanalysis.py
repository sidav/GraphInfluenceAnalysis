PRINT_TOP_N = 10


def sort_list(in_list):
    return sorted(in_list.items(), key=lambda x: x[1])


def do_analysis(books_list):
    years = {}
    decades = {}
    centuries = {}
    for book in books_list:
        book_year = book["book_release_year"]
        book_decade = book["book_release_year"][:3] + "x"
        book_century = book["book_release_year"][:2] + "xx"
        # print(book_decade, book_year)
        if book["book_id_exists"] != "True":
            continue
        if book_year in years.keys():
            years[book_year] += 1
        else:
            years[book_year] = 1

        if book_decade in decades.keys():
            decades[book_decade] += 1
        else:
            decades[book_decade] = 1

        if book_century in centuries.keys():
            centuries[book_century] += 1
        else:
            centuries[book_century] = 1
            
    print(sort_list(years))
    print_top_n(sort_list(years), "books_by_years", True)
    print(sort_list(decades))
    print_top_n(sort_list(decades), "books_by_decades", True)
    print(sort_list(centuries))
    print_top_n(sort_list(centuries), "books_by_centuries", True)



def print_top_n(all_list, name, print_graph=False):
    top = all_list[-PRINT_TOP_N:]

    top_names = []
    top_vals = []

    for ind in reversed(range(PRINT_TOP_N)):
        if ind >= len(top):
            continue
        i = top[ind]
        top_names.append(i[0])
        top_vals.append(i[1])
        print(i[0], ":", i[1])

    if print_graph:
        import matplotlib.pyplot as plt
        import numpy as np
        plt.rcdefaults()
        fig, ax = plt.subplots()

        y_pos = [i - 0.5 for i in np.arange(PRINT_TOP_N)]
        # print(y_pos)
        ax.barh(y_pos, top_vals, align='center',
                color='green', ecolor='black')
        ax.set_yticks(y_pos)
        ax.set_yticklabels(top_names)
        ax.invert_yaxis()  # labels read top-to-bottom
        ax.set_xlabel('Количество')
        ax.xaxis.grid()

        fig.tight_layout()
        fig.savefig(name + '.png')
        # fig.savefig('total_books_mean.jpg')
        # plt.tight_layout()
        # plt.show()
