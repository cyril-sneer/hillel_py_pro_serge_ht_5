from django.contrib.auth import get_user_model
from django.core.management.base import BaseCommand, CommandError


class Command(BaseCommand):
    help = """Deletes several users by its ids."""

    def add_arguments(self, parser):
        parser.add_argument("user_ids", nargs="+", type=int)

    def handle(self, *args, **options):
        User = get_user_model()

        users_queryset = User.objects.filter(id__in=options["user_ids"])
        if users_queryset.filter(is_superuser=True).exists():
            raise CommandError("Вы не можете удалить суперпользователя!")
        else:
            users_queryset.delete()

        # user_id_set = set(options['user_ids'])
        #
        # all_user_id_set = set(User.objects.all().values_list('id', flat=True))
        # superuser_id_set = set(User.objects.filter(is_superuser=True).values_list('id', flat=True))
        #
        # if user_id_set & superuser_id_set:
        #     raise CommandError("Вы не можете удалить суперпользователя!")
        # elif not user_id_set & all_user_id_set:
        #     raise CommandError("В базе нет пользователей с такими ID!")
        # else:
        #     User.objects.filter(id__in=user_id_set).delete()

        self.stdout.write(self.style.SUCCESS("Пользователи успешно удалены!"))
