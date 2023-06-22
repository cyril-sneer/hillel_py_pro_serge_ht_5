from django.contrib.auth import get_user_model
from django.contrib.auth.hashers import make_password
from django.core.management.base import BaseCommand, CommandError

from faker import Faker


class Command(BaseCommand):
    help = """Creates several new random users. Quantity of user is a obligatory argument"""

    def add_arguments(self, parser):
        parser.add_argument("user_qty", type=int, choices=range(1, 11))

    def handle(self, *args, **options):
        fake = Faker()
        User = get_user_model()
        User.objects.bulk_create(
            [
                User(
                    username=fake.user_name(),
                    email=fake.email(),
                    first_name=fake.first_name(),
                    last_name=fake.last_name(),
                    password=make_password(password=fake.password()),
                )
                for _ in range(options["user_qty"])
            ]
        )
        self.stdout.write(self.style.SUCCESS("Пользователи успешно созданы!"))
