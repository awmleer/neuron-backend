from django.core.management.base import BaseCommand, CommandError
from datetime import datetime, timedelta
from app.models import *
import  urllib.request,urllib.parse
from bs4 import BeautifulSoup
import time



class Command(BaseCommand):
    help = 'python manage.py pa'

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
        # user = User.objects.create_user(username=options['phone'],password=options['phone'])
        # user.save()
        # UserInfo.objects.create(user=user,name=options['name'],type='高级用户',expiration=timezone.now()+timedelta(days=30))
        # self.stdout.write(self.style.SUCCESS('Successfully create user [%s]' % (options['phone'])))

        file = open("ielts.txt")

        count=0
        while 1:
            line = file.readline().replace('\n','')
            if not line:
                break
            count+=1
            if(count<options['index']):
                continue
            if len(Entry.objects.filter(word=str(line)))>0:
                self.stdout.write(self.style.SUCCESS('Already exist [%s]' %line))
                continue
            time.sleep(1)
            result = urllib.request.urlopen("http://dict.cn/%s" % urllib.request.quote(line)).read()
            soup = BeautifulSoup(result,'html.parser')

            chart = soup.select('#dict-chart-basic')
            rates='{}'
            if len(chart)>0:
                rates=urllib.parse.unquote(chart[0].get('data'))

            definitions = soup.select('.word .basic ul li')
            phonetics = soup.select('.word .phonetic span')
            res = {
                'word': soup.select('.word-cont .keyword')[0].get_text(strip=True),
                'level': soup.select('.word-cont a')[1].get('class')[0].replace('level_', '', 1) if len(soup.select('.word-cont a'))>=2 else 0,
                'phonetic': {
                    'UK': {
                        'symbol': (phonetics[0].select('bdo')[0].get_text() if len(phonetics[0].select('bdo'))>0 else '') if len(phonetics)>0 else '',
                        'sound': {
                            'female': phonetics[0].select('i.sound')[0].get('naudio') if len(phonetics)>0 else '',
                            'male': phonetics[0].select('i.sound')[1].get('naudio') if len(phonetics)>0 else ''
                        }
                    },
                    'US': {
                        'symbol': (phonetics[1].select('bdo')[0].get_text() if len(phonetics[1].select('bdo'))>0 else '') if len(phonetics)>0 else '',
                        'sound': {
                            'female': phonetics[1].select('i.sound')[0].get('naudio') if len(phonetics)>0 else '',
                            'male': phonetics[1].select('i.sound')[1].get('naudio') if len(phonetics)>0 else ''
                        }
                    }
                },
                # 'syllable':soup.select('.word-cont .keyword')[0].get('tip').replace('音节划分：','',1),
                'definitions': [],
                'sentences': []
            }
            for definition in definitions:
                if definition.get('style') is not None: continue
                # print(definition.get('style'))
                res['definitions'].append({
                    'type': definition.select('span')[0].get_text() if len(definition.select('span'))>0 else '',
                    'text': definition.select('strong')[0].get_text()
                })
            if len(soup.select('.section.sent .layout.sort'))>0:
                sentences = soup.select('.section.sent .layout.sort li')
                for sentence in sentences:
                    i_tags = sentence.select('i')
                    for i_tag in i_tags:
                        i_tag.decompose()
                    res['sentences'].append(
                        sentence.prettify()
                            .replace('\n ', '')
                            .replace('</em>', '</em> ')
                            .replace('<em class=\"hot\"> ',' <em class=\"hot\">')
                            .replace('\n', '')
                            .replace('<li>', '')
                            .replace('</li>', '')
                    )
            if res['word']!= line:
                self.stdout.write(self.style.ERROR('Word not identical [%d] %s & %s' % (count,line,res['word'])))
                return
            entry=Entry(word=res['word'],level=int(res['level']))
            entry.definitions=res['definitions']
            entry.sentences=res['sentences']
            entry.phonetic=res['phonetic']
            entry.definition_rates = rates
            entry.save()
            self.stdout.write(self.style.SUCCESS('Add word [%d] %s' % (count,res['word'])))



