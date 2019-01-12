import analyze_books, analyze_authors
import csv as csv

books_dict = []
with open('fantlab_books_data.csv', 'r', encoding="utf8") as csv_old:
    reader = csv.DictReader(csv_old)
    books_dict = []
    for row in reader:
        books_dict.append(row)

print("================================")
print("=======  BOOKS ANALYSIS  =======")
print("================================")
print()
analyze_books.analyze_books(books_dict)
print("================================")
print("======  AUTHORS ANALYSIS  ======")
print("================================")
print()
analyze_authors.analyze_authors(books_dict)
