import csv
import os
from django.core.management.base import BaseCommand
from django.conf import settings
from reviews.models import Category, Genre, Title, Review
from django.contrib.auth import get_user_model

User = get_user_model()

class Command(BaseCommand):
    help = 'Import data from CSV files'

    def handle(self, *args, **options):
        base_path = os.path.join(settings.BASE_DIR, 'static', 'data')
        
        # 1. Импорт пользователей (если доступен)
        users_path = os.path.join(base_path, 'users.csv')
        if os.path.exists(users_path):
            with open(users_path, encoding='utf-8') as f:
                reader = csv.DictReader(f)
                for row in reader:
                    User.objects.get_or_create(
                        id=row['id'],
                        username=row['username'],
                        email=row['email'],
                    )
        else:
            self.stdout.write(self.style.WARNING('users.csv not found, skipping user import'))

        # 2. Импорт категорий
        with open(os.path.join(base_path, 'category.csv'), encoding='utf-8') as f:
            reader = csv.DictReader(f)
            for row in reader:
                Category.objects.get_or_create(
                    id=row['id'],
                    name=row['name'],
                    slug=row['slug']
                )

        # 3. Импорт жанров
        with open(os.path.join(base_path, 'genre.csv'), encoding='utf-8') as f:
            reader = csv.DictReader(f)
            for row in reader:
                Genre.objects.get_or_create(
                    id=row['id'],
                    name=row['name'],
                    slug=row['slug']
                )

        # 4. Импорт произведений
        with open(os.path.join(base_path, 'titles.csv'), encoding='utf-8') as f:
            reader = csv.DictReader(f)
            for row in reader:
                # Используем get_or_create для категории на случай отсутствия
                category, _ = Category.objects.get_or_create(id=row['category'])
                Title.objects.get_or_create(
                    id=row['id'],
                    name=row['name'],
                    year=row['year'],
                    category=category
                )

        # 5. Импорт связей произведений и жанров
        with open(os.path.join(base_path, 'genre_title.csv'), encoding='utf-8') as f:
            reader = csv.DictReader(f)
            for row in reader:
                title = Title.objects.get(id=row['title_id'])
                genre = Genre.objects.get(id=row['genre_id'])
                title.genre.add(genre)

        # 6. Импорт отзывов (с проверкой существования пользователей и произведений)
        with open(os.path.join(base_path, 'review.csv'), encoding='utf-8') as f:
            reader = csv.DictReader(f)
            for row in reader:
                try:
                    # Проверяем существование пользователя
                    user = User.objects.get(id=row['author'])
                    
                    # Проверяем существование произведения
                    title = Title.objects.get(id=row['title_id'])
                    
                    Review.objects.get_or_create(
                        id=row['id'],
                        title=title,
                        text=row['text'],
                        author=user,
                        score=row['score'],
                        pub_date=row['pub_date']
                    )
                except User.DoesNotExist:
                    self.stdout.write(self.style.ERROR(f"User {row['author']} not found for review {row['id']}"))
                except Title.DoesNotExist:
                    self.stdout.write(self.style.ERROR(f"Title {row['title_id']} not found for review {row['id']}"))

        self.stdout.write(self.style.SUCCESS('Data imported successfully'))