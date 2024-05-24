import csv
from django.core.management.base import BaseCommand, CommandError
from books.models import Book, Genre, Author


class Command(BaseCommand):
    help = "Imports books from a CSV file"

    def add_arguments(self, parser):
        parser.add_argument("filename", nargs=1, type=str)

    def handle(self, *args, **options):
        filename = options["filename"][0]
        self.stdout.write(f"Importing books from {filename}")

        with open(filename) as csv_file:
            csv_reader = csv.reader(csv_file, delimiter=',')
            line_count = 0
            for row in csv_reader:
                if line_count == 0:
                    line_count += 1
                    continue
                else:
                    author_names = row[0]
                    authors = []
                    for author_name in author_names.split("|"):
                        author_name = author_name.strip()
                        author, _ = Author.objects.get_or_create(full_name=author_name)
                        authors.append(author)

                    try:
                        pages = int(float(row[4].replace(" pages", "")))
                    except ValueError:
                        pages = 0

                    genre_names = row[9]
                    genres = []
                    for genre_name in genre_names.split("|"):
                        genre_name = genre_name.strip()
                        genre, _ = Genre.objects.get_or_create(name=genre_name)
                        genres.append(genre)

                    book = Book.objects.create(
                        desc=row[1],
                        edition=row[2],
                        format=row[3],
                        pages=pages,
                        rating=row[5],
                        rating_count=row[6],
                        review_count=row[7],
                        title=row[8],
                    )

                    book.authors.set(authors)
                    book.genres.set(genres)

                    self.stdout.write(f"Created {book}")

                    line_count += 1
            self.stdout.write(f"Imported {line_count} books.")