from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from app.models import *


class Command(BaseCommand):

    # def add_arguments(self, parser):
        # parser.add_argument('phone',type=str)
        # parser.add_argument('name',type=str)
        # parser.add_argument(
        #     '--delete',
        #     action='store_true',
        #     dest='delete',
        #     default=False,
        #     help='Delete poll instead of closing it',
        # )

    def handle(self, *args, **options):
        entries=Entry.objects.all()
        for entry in entries:
            pass
            # newSentences=[]
            # # i=0
            # for sentence in entry.sentences:
            #     newSentences.append(sentence['text'])
            #     # i+=1
            # entry.sentences=newSentences
            # entry.save()
        self.stdout.write(self.style.SUCCESS('Done'))
