import random
import string
from django.core.management.base import BaseCommand
from django.contrib.auth.models import User, Group

class Command(BaseCommand):
    help = 'Generate dummy users'

    def add_arguments(self, parser):
        parser.add_argument('num_users', type=int, help='Number of dummy users to generate')

    def handle(self, *args, **options):
        num_users = options['num_users']

        def random_username():
            prefix = ''.join(random.choices(string.ascii_lowercase, k=3))
            suffix = ''.join(random.choices(string.digits, k=3))
            return f'{prefix}{suffix}'

        def random_email(username):
            domains = ['example.com', 'mail.com', 'test.org']
            domain = random.choice(domains)
            return f'{username}@{domain}'

        def random_password():
            length = 8
            characters = string.ascii_letters + string.digits + string.punctuation
            return ''.join(random.choices(characters, k=length))

        investor_group, _ = Group.objects.get_or_create(name='Investor')

        for i in range(num_users):
            username = random_username()
            email = random_email(username)
            password = random_password()
            first_name = f'First{i+1}'
            last_name = f'Last{i+1}'

            user = User.objects.create_user(
                username=username,
                password=password,
                email=email,
                first_name=first_name,
                last_name=last_name
            )
            user.groups.add(investor_group)
            user.save()

            self.stdout.write(self.style.SUCCESS(f'Created user: {user.username}'))
