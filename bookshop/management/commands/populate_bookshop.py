import random
import time

import faker
from django.core.management.base import BaseCommand, CommandError

from bookshop.models import Author, Book, Publisher, Store


class Command(BaseCommand):
    help = """Populate Book DB with 5 000 items"""

    def add_arguments(self, parser):
        parser.add_argument("-book_qty", type=int, required=False, default=5000)

    def handle(self, *args, **options):
        # 1000 res = 20 sec!!!

        if options['book_qty'] < 5000:
            raise CommandError("Books quantity should be more then 5 000 !")

        start = time.time()
        fake = faker.Faker()
        PUBLISHER_QTY = 100
        AUTHOR_QTY = 500

        self.stdout.write(self.style.NOTICE(f"Populating Publishers DB with {PUBLISHER_QTY} new records.."))
        Publisher.objects.bulk_create((
            Publisher(name=fake.company()) for _ in range(PUBLISHER_QTY)
        ))
        self.stdout.write(self.style.SUCCESS(f"Publishers DB +{PUBLISHER_QTY} done!"))

        self.stdout.write(self.style.NOTICE(f"Populating Authors DB with {AUTHOR_QTY} new records.."))
        Author.objects.bulk_create((
            Author(
                name=fake.name(),
                age=random.randint(20, 70)
            ) for _ in range(AUTHOR_QTY)
        ))
        self.stdout.write(self.style.SUCCESS(f"Authors DB +{AUTHOR_QTY} done!"))

        self.stdout.write(self.style.NOTICE(f"Populating Books DB with {options['book_qty']} new records.."))
        for book_counter in range(options['book_qty']):
            book = Book.objects.create(
                name=fake.sentence(),
                pages=random.randint(10, 1000),
                price=round(random.random() * 100, 2),
                rating=random.randint(1, 10),
                # authors=random.choice(Author.objects.all()),
                publisher=random.choice(Publisher.objects.all()),
                pubdate=fake.date_object()
            )

            num_of_authors = random.randint(1, 2)
            for author_counter in range(num_of_authors):
                book.authors.add(random.choice(Author.objects.all()))
        self.stdout.write(self.style.SUCCESS(f"Books DB +{options['book_qty']} done!"))

        self.stdout.write(
            self.style.NOTICE(f"Populating 3 Bookshops with {round(options['book_qty'] / 2)} books each.."))
        stores = [Store.objects.create(name='Best books'),
                  Store.objects.create(name='Interesting books'),
                  Store.objects.create(name='Exciting books')
                  ]
        for store in stores:
            for book in random.sample(tuple(Book.objects.all()), k=round(options['book_qty'] / 2)):
                store.books.add(book)
        self.stdout.write(self.style.SUCCESS(f"Store DB done!"))
        self.stdout.write(self.style.SUCCESS(f"ALL done in {time.time() - start:.2f} sec!"))

