from django.core.management.base import BaseCommand, CommandError
from datetime import datetime, timedelta
from bank.models import Entry, Sentence
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

        file = open("cet4.txt")

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

            result = urllib.request.urlopen("http://youdao.com/w/%s/" % urllib.request.quote(line)).read()
            soup = BeautifulSoup(result,'html.parser')
            content = soup.select('#results-contents')[0]

            phrs_list_tab = content.select('#phrsListTab')[0]
            word = phrs_list_tab.select('h2.wordbook-js span.keyword')[0].get_text(strip=True)
            if word != line:
                self.stdout.write(self.style.ERROR('Word not identical [%d] %s & %s' % (count, line, word)))
                return

            entry = Entry(word=word)

            star_tags = content.select('#collinsResult span.star')
            if len(star_tags)>0:
                star_class = star_tags[0]['class']
                if 'star5' in star_class:
                    entry.rank = 5
                elif 'star4' in star_class:
                    entry.rank = 4
                elif 'star3' in star_class:
                    entry.rank = 3
                elif 'star2' in star_class:
                    entry.rank = 2
                elif 'star1' in star_class:
                    entry.rank = 1
                elif 'star0' in star_class:
                    entry.rank = 0

            definition_tags = phrs_list_tab.select('div.trans-container ul')[0].select('li')
            definitions = []
            for tag in definition_tags:
                t = tag.get_text(strip=True).split('. ', 1)
                definitions.append({
                    'part': t[0] if len(t)==2 else None,
                    'text': t[-1]
                })
            entry.definitions = definitions

            pronounce_tags = content.select('div.baav span.pronounce')
            for tag in pronounce_tags:
                phonetic = tag.select('span.phonetic')[0].get_text(strip=True)
                if tag.get_text(strip=True)[0] == '英':
                    entry.pronounce['UK'] = phonetic
                elif tag.get_text(strip=True)[0] == '美':
                    entry.pronounce['US'] = phonetic

            entry.save()

            # sentences
            result = urllib.request.urlopen("http://youdao.com/example/blng/eng/%s/" % urllib.request.quote(line)).read()
            soup = BeautifulSoup(result, 'html.parser')
            li_tags = soup.select('#results-contents ul.ol')[0].select('li')
            for li_tag in li_tags:
                p_tags = li_tag.select('p')
                english = ''
                for span_tag in p_tags[0].select('span'):
                    english += str(span_tag.unwrap())
                chinese = p_tags[1].get_text(strip=True)
                reference = p_tags[2].get_text(strip=True) if len(p_tags)>2 else ''
                Sentence.objects.create(
                    entry=entry,
                    english=english,
                    chinese=chinese,
                    reference=reference
                )

            self.stdout.write(self.style.SUCCESS('Add word [%d] %s with %d sentences.' % (count,word,len(li_tags))))



