from django.core.management.base import BaseCommand
# from django.contrib.auth.models import User
from app.models import *


class Command(BaseCommand):

    def handle(self, *args, **options):
        entries=Entry.objects.all()
        for entry in entries:
            for sentence in entry.sentencesTemp:
                Sentence.objects.create(text=sentence,entry=entry)
            # newSentences=[]
            # # i=0
            # for sentence in entry.sentences:
            #     newSentences.append(sentence['text'])
            #     # i+=1
            # entry.sentences=newSentences
            # entry.save()
        self.stdout.write(self.style.SUCCESS('Done'))
