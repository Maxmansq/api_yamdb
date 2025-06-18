import csv
import os

from django.core.management.base import BaseCommand

from reviews.models import Category, Genre, Title, Review
from users.models import CastomUser


class Command(BaseCommand):
    help = "Import data from CSV files"

    def import_users(self, base_path):
        users_path = os.path.join(base_path, "users.csv")
        if not os.path.exists(users_path):
            self.stdout.write(self.style.WARNING(
                "users.csv not found, skipping user import"))
            return

        with open(users_path, encoding="utf-8") as f:
            for row in csv.DictReader(f):
                CastomUser.objects.get_or_create(
                    id=row["id"],
                    username=row["username"],
                    email=row["email"],
                )

    def import_categories(self, base_path):
        with open(os.path.join(base_path, "category.csv"),
                  encoding="utf-8") as f:
            for row in csv.DictReader(f):
                Category.objects.get_or_create(
                    id=row["id"],
                    name=row["name"],
                    slug=row["slug"]
                )

    def import_genres(self, base_path):
        with open(os.path.join(base_path, "genre.csv"),
                  encoding="utf-8") as f:
            for row in csv.DictReader(f):
                Genre.objects.get_or_create(
                    id=row["id"],
                    name=row["name"],
                    slug=row["slug"]
                )

    def import_titles(self, base_path):
        with open(os.path.join(base_path, "titles.csv"),
                  encoding="utf-8") as f:
            for row in csv.DictReader(f):
                category, _ = Category.objects.get_or_create(
                    id=row["category"])
                Title.objects.get_or_create(
                    id=row["id"],
                    name=row["name"],
                    year=row["year"],
                    category=category
                )

    def import_genre_title_links(self, base_path):
        with open(os.path.join(base_path, "genre_title.csv"),
                  encoding="utf-8") as f:
            for row in csv.DictReader(f):
                title = Title.objects.get(id=row["title_id"])
                genre = Genre.objects.get(id=row["genre_id"])
                title.genre.add(genre)

    def import_reviews(self, base_path):
        with open(os.path.join(base_path, "review.csv"),
                  encoding="utf-8") as f:
            for row in csv.DictReader(f):
                try:
                    user = CastomUser.objects.get(id=row["author"])
                    title = Title.objects.get(id=row["title_id"])
                    Review.objects.get_or_create(
                        id=row["id"],
                        title=title,
                        text=row["text"],
                        author=user,
                        score=row["score"],
                        pub_date=row["pub_date"]
                    )
                except CastomUser.DoesNotExist:
                    self.stdout.write(self.style.ERROR(
                        f"User {row['author']}"
                        f"not found for review {row['id']}"
                    ))
                except Title.DoesNotExist:
                    self.stdout.write(self.style.ERROR(
                        (f"Title {row['title_id']}"
                         f"not found for review {row['id']}")
                    ))
