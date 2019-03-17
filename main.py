import analyze_books, analyze_authors, preanalysis
import csv as csv

books_dict = []
total_books = 0
print("================================")
print("==== READING THE DATA SET... ===")
with open('fantlab_books_data.csv', 'r', encoding="utf8") as csv_old:
    reader = csv.DictReader(csv_old)
    books_dict = []
    for row in reader:
        if row["book_id_exists"] == "True":
            total_books += 1
        books_dict.append(row)

print(total_books, "books total.")
print("================================")
print("===   DATASET PRE-ANALYSIS   ===")
print("================================")
print()
preanalysis.do_analysis(books_dict)
#
# print("================================")
# print("=======  BOOKS ANALYSIS  =======")
# print("================================")
# print()
# analyze_books.analyze_books(books_dict)
# print("================================")
# print("======  AUTHORS ANALYSIS  ======")
# print("================================")
# print()
# analyze_authors.analyze_authors(books_dict)
