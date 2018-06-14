from django.core.management.base import BaseCommand
# from django.contrib.auth.models import User
from app.models import *


class Command(BaseCommand):

    def handle(self, *args, **options):
        for sentence in Sentence.objects.all():
            texts=sentence.english.split('<br/>')
            sentence.english=texts[0]
            sentence.chinese=texts[1]
            sentence.save()
        self.stdout.write(self.style.SUCCESS('Done'))
