import json
import sys
from django.core.management.base import BaseCommand
from aldoj_app.models import Crop, Property

class Command(BaseCommand):
    help = 'Load crops from a JSON file'

    def add_arguments(self, parser):
        parser.add_argument('file_path', type=str, help='Path to the JSON file containing crops')

    def handle(self, *args, **options):
        file_path = options['file_path']

        try:
            with open(file_path, 'r') as file:
                crops_data = json.load(file)

            for crop_data in crops_data:
                property_id = crop_data['property_id']
                property_obj = Property.objects.get(id=property_id)

                crop = Crop.objects.create(
                    property=property_obj,
                    name=crop_data['name'],
                    yield_per_hectare=crop_data['yield_per_hectare']
                )

                self.stdout.write(self.style.SUCCESS(f'Created crop: {crop.name}'))

        except FileNotFoundError:
            self.stdout.write(self.style.ERROR(f'File not found: {file_path}'))
            sys.exit(1)
        except Property.DoesNotExist:
            self.stdout.write(self.style.ERROR(f'Property with id {property_id} does not exist'))
