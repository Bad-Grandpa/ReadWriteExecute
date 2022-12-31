import json

from django.core.management.base import BaseCommand, CommandError
from django.shortcuts import get_object_or_404
from django.http import Http404

from learnjapanese.models import FlashCard, Category

class Command(BaseCommand):
    help = '''Create FlashCards base from json file.

    Data expected from the single entry in json:
     gloss - english word/phrase, 
     reb - japanese translation written in hiragana/katakana,
     keb - (optional) japanese translation written with kanji.

    Data format is based on JMDict project (https://www.edrdg.org/jmdict/j_jmdict.html)
    since subset of this dictionary is used internally.
    '''

    def add_arguments(self, parser):
        parser.add_argument('dict_path',
            help='Path to json file containing the dictionary with project folder as the working directory')

        category_group = parser.add_mutually_exclusive_group()
        category_group.add_argument('-cpk', '--category_pk', type=int, default=1,
            help='All entries will be added to category with pk provided.')
        category_group.add_argument('-cc', '--create_category', action='store_true',
            help='Adding this option will create new category all entries will be added to.')

    def handle(self, *args, **options):
        category_pk = options['category_pk']
        dict_path = options['dict_path']

        if options['create_category']:
            target_category = Category(category_name='dictionary_default')
            target_category.save()
        else:
            try:
                target_category = get_object_or_404(Category, pk=category_pk)
            except Http404:
                raise CommandError(f'Category with pk={category_pk} does not exist')

        try:
            with open(dict_path, 'r') as f:
                data = json.load(f)

                for entry in data:
                    fc = FlashCard(
                        english_text=entry["gloss"],
                        japanese_text=entry["reb"],
                        japanese_text_kanji = entry.get("keb"),
                        category=target_category
                        )
                    
                    fc.save()
        except FileNotFoundError:
            raise CommandError(f'File {dict_path} was not found')

        self.stdout.write(self.style.SUCCESS(f'Dictionary {dict_path} imported succesfully'))