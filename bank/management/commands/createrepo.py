from django.core.management.base import BaseCommand, CommandError
from bank.models import Repo


class Command(BaseCommand):
    help = 'python manage.py createrepo <repo_name>'

    def add_arguments(self, parser):
        parser.add_argument('repo_name',type=str)

    def handle(self, *args, **options):
        repo_name = options['repo_name']
        repo = Repo.objects.create(
            name=repo_name
        )
        self.stdout.write(self.style.SUCCESS('Repo create. Id is %d'%repo.id))



