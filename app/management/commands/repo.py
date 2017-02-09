from django.core.management.base import BaseCommand, CommandError
from app.models import *



class Command(BaseCommand):
    help = 'python manage.py repo'

    def add_arguments(self, parser):
        pass
        # parser.add_argument('index',type=int)
        # parser.add_argument('name',type=str)
        # parser.add_argument(
        #     '--delete',
        #     action='store_true',
        #     dest='delete',
        #     default=False,
        #     help='Delete poll instead of closing it',
        # )

    def handle(self, *args, **options):
        repo=Repo.objects.create()
        file = open("cet4.txt")
        words=[]
        while 1:
            line = file.readline().replace('\n','')
            if not line:
                break
            words.append(line)
        repo.set_words(words)
        repo.save()
        self.stdout.write(self.style.SUCCESS('Repo added'))



