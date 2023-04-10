import json
from django.core.management.base import BaseCommand
from aldoj_app.models import Investment, Property, User
from django.contrib.auth.models import User

class Command(BaseCommand):
    help = 'Load investments from a JSON file'

    def add_arguments(self, parser):
        parser.add_argument('json_file', type=str, help='Path to the JSON file')

    def handle(self, *args, **options):
        json_file = options['json_file']

        with open(json_file, 'r') as file:
            investments_data = json.load(file)

        for investment_data in investments_data:
            property_id = investment_data['property_id']
            investor_id = investment_data['investor_id']
            amount = investment_data['amount']

            try:
                property_obj = Property.objects.get(id=property_id)
                investor_obj = User.objects.get(id=investor_id)

                investment = Investment.objects.create(
                    property=property_obj,
                    investor=investor_obj,
                    amount=amount
                )

                self.stdout.write(self.style.SUCCESS(f'Created investment: {investment.id}'))
            except Property.DoesNotExist:
                self.stdout.write(self.style.ERROR(f'Property with id {property_id} does not exist'))
            except User.DoesNotExist:
                self.stdout.write(self.style.ERROR(f'User with id {investor_id} does not exist'))
