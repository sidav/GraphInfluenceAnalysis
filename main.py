import analyze_books, analyze_authors
import csv as csv

books_dict = []
with open('fantlab_books_data.csv', 'r') as csv_old:
    reader = csv.DictReader(csv_old)
    books_dict = []
    for row in reader:
        books_dict.append(row)

analyze_books.analyze_books(books_dict)
print("--------------------------------")
print()
analyze_authors.analyze_authors(books_dict)
