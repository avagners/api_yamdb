from django.core.management.base import BaseCommand
from reviews.models import Title, Category, Genre, Review, Comment
from users.models import User
import pandas as pd
import csv



class Command(BaseCommand):



    def add_arguments(self, parser):
        parser.add_argument('file_path', type=str)

    def handle(self, *args, **options):
        file_path = f'static/data/{options["file_path"]}'
        
        with open(file_path, newline='', encoding='utf-8') as f:
            reader = csv.DictReader(f)
            for row in reader:
                path = file_path.split('/')
                if path[-1] == 'genre.csv':
                    status, created = Genre.objects.update_or_create(
                        id=row['id'],
                        name=row['name'],
                        slug=row['slug']
                    )

                elif path[-1] == 'category.csv':
                    status, created = Category.objects.update_or_create(
                        id=row['id'],
                        name=row['name'],
                        slug=row['slug']
                        )

                elif path[-1] == 'comments.csv':
                    status, created = Comment.objects.update_or_create(
                        id=row['id'],
                        review_id=row['review_id'],
                        text=row['text'],
                        author=row['author'],
                        pub_date=row['pub_date']
                        )

                elif path[-1] == 'title.csv':
                    status, created = Title.objects.update_or_create(
                        id=row['id'],
                        name=row['name'],
                        year=row['year'],
                        category=row['category']
                        )

                elif path[-1] == 'review.csv':
                    status, created = Review.objects.update_or_create(
                        id=row['id'],
                        title_id=row['title_id'],
                        text=row['text'],
                        author=row['author'],
                        score=row['score'],
                        pub_date=row['pub_date']
                        )

                elif path[-1] == 'users.csv':
                    status, created = User.objects.update_or_create(
                        id=row['id'],
                        username=row['username'],
                        email=row['username'],
                        role=row['role'],
                        bio=row['bio'],
                        first_name=row['first_name'],
                        last_name=row['last_name']
                        )

