from django.core.management.base import BaseCommand
# from django.contrib.auth.models import User
from app.models import *


class Command(BaseCommand):

    def handle(self, *args, **options):
        repos=Repo.objects.all()
        for repo in repos:
            for word in repo.words:
                entries=Entry.objects.filter(word=word)
                if len(entries)==1:
                    repo.entries.add(entries[0])
                elif len(entries)>1:
                    print('Error in ['+word+']')
                    break
            # newSentences=[]
            # # i=0
            # for sentence in entry.sentences:
            #     newSentences.append(sentence['text'])
            #     # i+=1
            # entry.sentences=newSentences
            # entry.save()
        self.stdout.write(self.style.SUCCESS('Done'))
