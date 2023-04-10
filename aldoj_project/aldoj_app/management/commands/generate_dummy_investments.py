import random
from django.core.management.base import BaseCommand
from aldoj_app.models import Investment, Property, User
from django.contrib.auth.models import Group

class Command(BaseCommand):
    help = 'Generate dummy investments'

    def add_arguments(self, parser):
        parser.add_argument('num_investments', type=int, help='Number of dummy investments to generate')

    def handle(self, *args, **options):
        num_investments = options['num_investments']

        properties = Property.objects.all()
        investor_group = Group.objects.get(name='Investor')
        investors = User.objects.filter(groups=investor_group)

        if not properties.exists():
            self.stdout.write(self.style.ERROR('No properties found. Please add properties first.'))
            return

        if not investors.exists():
            self.stdout.write(self.style.ERROR('No investors found. Please add investors first.'))
            return

        for i in range(num_investments):
            property_obj = random.choice(properties)
            investor_obj = random.choice(investors)
            amount = round(random.uniform(100, 10000), 2)

            investment = Investment.objects.create(
                property=property_obj,
                investor=investor_obj,
                amount=amount
            )

            self.stdout.write(self.style.SUCCESS(f'Created investment: {investment.id}'))
