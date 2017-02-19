from django.core.management.base import BaseCommand, CommandError
from datetime import datetime, timedelta
from app.models import *
import  urllib.request,urllib.parse
from bs4 import BeautifulSoup
import time



class Command(BaseCommand):
    help = 'python manage.py hhh'

    def add_arguments(self, parser):
        pass
        parser.add_argument('index',type=int)
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
        count = 0
        for entry in entries:
            count += 1
            if (count < options['index']):
                continue
            time.sleep(1)
            result = urllib.request.urlopen("http://dict.cn/%s" % urllib.request.quote(entry.word)).read()
            soup = BeautifulSoup(result,'html.parser')

            chart = soup.select('#dict-chart-basic')
            if len(chart)>0:
                rates=urllib.parse.unquote(chart[0].get('data'))
                entry.definition_rates=rates

            # dls=soup.select('.layout.phrase dl')
            # phrases=[]
            # for dl in dls:
            #     phrase={
            #         'phrase':dl.select('dt')[0].get_text(),
            #         'explanations':[]
            #     }
            #     for li in dl.select('dd li'):
            #         explanation=''
            #         for string in phrase['explanations'].stripped_strings:
            #             if explanation=='':
            #                 explanation += string
            #             else:
            #                 explanation=explanation+'\n'+string
            #         phrase['explanations'].append(explanation)
            #         print(phrase)
            #     phrases.append(phrase)
            # print(phrases)
            # entry.set_phrases(phrases)

            entry.save()
            self.stdout.write(self.style.SUCCESS('Update word [%d] %s' % (count,entry.word)))



