import random
from django.core.management.base import BaseCommand
from aldoj_app.models import Crop, Property

class Command(BaseCommand):
    help = 'Generate dummy crops'

    def add_arguments(self, parser):
        parser.add_argument('num_crops', type=int, help='Number of dummy crops to generate')

    def handle(self, *args, **options):
        num_crops = options['num_crops']

        crop_types = ['Fruits', 'Vegetables', 'Grains', 'Legumes']
        properties = Property.objects.all()

        if not properties.exists():
            self.stdout.write(self.style.ERROR('No properties found. Please add properties first.'))
            return

        for i in range(num_crops):
            crop_type = random.choice(crop_types)
            crop_name = f'{crop_type} Crop {i+1}'
            crop_yield = random.randint(50, 300)
            property_obj = random.choice(properties)

            crop = Crop.objects.create(
                property=property_obj,
                name=crop_name,
                yield_per_hectare=crop_yield
            )

            self.stdout.write(self.style.SUCCESS(f'Created crop: {crop.name}'))
