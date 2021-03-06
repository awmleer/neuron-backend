from django.core.management.base import BaseCommand, CommandError
from bank.models import Entry, Sentence, Repo
import  urllib.request,urllib.parse
from bs4 import BeautifulSoup
import time
from django.db import transaction
import traceback


class Command(BaseCommand):
    help = 'python manage.py crawl <repo_name> <index>'

    def add_arguments(self, parser):
        parser.add_argument('repo_name',type=str)
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
        def do_crawl(word):
            with transaction.atomic():
                result = urllib.request.urlopen("http://youdao.com/w/%s/" % urllib.request.quote(word)).read()
                soup = BeautifulSoup(result,'html.parser')
                content = soup.select('#results-contents')[0]

                phrs_list_tab = content.select('#phrsListTab')[0]
                word = phrs_list_tab.select('h2.wordbook-js span.keyword')[0].get_text(strip=True)
                if word != word:
                    self.stdout.write(self.style.ERROR('Word not identical [%d] %s & %s' % (count, word, word)))
                    return

                entry = Entry(word=word)

                # star_tags = content.select('#collinsResult span.star')
                # if len(star_tags)>0:
                #     star_class = star_tags[0]['class']
                #     if 'star5' in star_class:
                #         entry.rank = 5
                #     elif 'star4' in star_class:
                #         entry.rank = 4
                #     elif 'star3' in star_class:
                #         entry.rank = 3
                #     elif 'star2' in star_class:
                #         entry.rank = 2
                #     elif 'star1' in star_class:
                #         entry.rank = 1
                #     elif 'star0' in star_class:
                #         entry.rank = 0

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
                    if len(tag.select('span.phonetic'))>0:
                        phonetic = tag.select('span.phonetic')[0].get_text(strip=True)[1:-1]
                        if tag.get_text(strip=True)[0] == '英':
                            entry.pronounce['UK'] = phonetic
                        elif tag.get_text(strip=True)[0] == '美':
                            entry.pronounce['US'] = phonetic

                result = urllib.request.urlopen("http://dict.cn/%s" % urllib.request.quote(word)).read()
                soup = BeautifulSoup(result, 'html.parser')
                entry.rank = soup.select('.word-cont a')[1].get('class')[0].replace('level_', '', 1) if len(soup.select('.word-cont a'))>=2 else 0

                entry.save()

                # sentences
                result = urllib.request.urlopen("http://youdao.com/example/blng/eng/%s/" % urllib.request.quote(word)).read()
                soup = BeautifulSoup(result, 'html.parser')
                sentence_count = 0
                if len(soup.select('#results-contents ul.ol'))>0:
                    li_tags = soup.select('#results-contents ul.ol')[0].select('li')
                    sentence_count = len(li_tags)
                    for li_tag in li_tags:
                        p_tags = li_tag.select('p')
                        english = ''
                        for span_tag in p_tags[0].select('span'):
                            for content in span_tag.contents:
                                english += str(content)
                        chinese = p_tags[1].get_text(strip=True)
                        reference = p_tags[2].get_text(strip=True) if len(p_tags)>2 else ''
                        if entry.sentences.filter(english__exact=english).exists():
                            continue
                        Sentence.objects.create(
                            entry=entry,
                            english=english,
                            chinese=chinese,
                            reference=reference
                        )
                    repo.entries.add(entry)
            self.stdout.write(self.style.SUCCESS('Add word [%d] %s with %d sentences.' % (count, word, sentence_count)))
            if sentence_count==0:
                self.stdout.write(self.style.WARNING('No sentence found.'))


        file = open('%s.txt'%options['repo_name'])
        repo = Repo.objects.get(name=options['repo_name'])

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
            time.sleep(5)
            success = False
            for i in range(0,5):
                try:
                    do_crawl(line)
                    success = True
                    break
                except Exception as e:
                    traceback.print_exc()
                    time.sleep(5)
                    continue
            if not success:
                self.stdout.write(self.style.ERROR('Failed [%s]'%line))
                return




