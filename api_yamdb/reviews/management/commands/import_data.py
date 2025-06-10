import csv
import os
from django.core.management.base import BaseCommand
from django.conf import settings
from reviews.models import Category, Genre, Title

class Command(BaseCommand):
    help = 'Import data from CSV files'

    def handle(self, *args, **options):
        base_path = os.path.join(settings.BASE_DIR, 'static', 'data')
        
        with open(os.path.join(base_path, 'category.csv'), encoding='utf-8') as f:
            reader = csv.DictReader(f)
            for row in reader:
                Category.objects.get_or_create(
                    id=row['id'],
                    name=row['name'],
                    slug=row['slug']
                )

        with open(os.path.join(base_path, 'genre.csv'), encoding='utf-8') as f:
            reader = csv.DictReader(f)
            for row in reader:
                Genre.objects.get_or_create(
                    id=row['id'],
                    name=row['name'],
                    slug=row['slug']
                )

        with open(os.path.join(base_path, 'titles.csv'), encoding='utf-8') as f:
            reader = csv.DictReader(f)
            for row in reader:
                category = Category.objects.get(id=row['category'])
                Title.objects.get_or_create(
                    id=row['id'],
                    name=row['name'],
                    year=row['year'],
                    category=category
                )

        with open(os.path.join(base_path, 'genre_title.csv'), encoding='utf-8') as f:
            reader = csv.DictReader(f)
            for row in reader:
                title = Title.objects.get(id=row['title_id'])
                genre = Genre.objects.get(id=row['genre_id'])
                title.genre.add(genre)

        with open(os.path.join(base_path, 'review.csv'), encoding='utf-8') as f:
            reader = csv.DictReader(f)
            for row in reader:
                Review.objects.get_or_create(
                    id=row['id'],
                    title_id=row['title_id'],
                    text=row['text'],
                    author_id=row['author'],
                    score=row['score'],
                    pub_date=row['pub_date']
                )
        self.stdout.write(self.style.SUCCESS('Data imported successfully'))
