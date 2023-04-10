import random
import string
from django.core.management.base import BaseCommand
from aldoj_app.models import Property

class Command(BaseCommand):
    help = 'Generate dummy data for properties'

    def add_arguments(self, parser):
        parser.add_argument('num_properties', type=int, help='Number of dummy properties to generate')

    def handle(self, *args, **options):
        num_properties = options['num_properties']

        def random_property_type():
            property_types = ['AG', 'RE']
            return random.choice(property_types)

        def random_title(i):
            return f'Property {i+1}'

        def random_description(i):
            return f'Property {i+1} description'

        def random_location(i):
            return f'Location {i+1}'

        def random_area():
            return round(random.uniform(100, 10000), 2)

        def random_price():
            return round(random.uniform(10000, 1000000), 2)

        for i in range(num_properties):
            property_type = random_property_type()
            title = random_title(i)
            description = random_description(i)
            location = random_location(i)
            area = random_area()
            price = random_price()

            property = Property.objects.create(
                property_type=property_type,
                title=title,
                description=description,
                location=location,
                area=area,
                price=price
            )
            self.stdout.write(self.style.SUCCESS(f'Created property: {property.title}'))
