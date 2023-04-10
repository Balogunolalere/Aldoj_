import json
from django.core.management.base import BaseCommand, CommandError
from aldoj_app.models import Property

class Command(BaseCommand):
    help = 'Load properties from a JSON file'

    def add_arguments(self, parser):
        parser.add_argument('json_file', type=str, help='The JSON file containing property data')

    def handle(self, *args, **options):
        json_file = options['json_file']

        try:
            with open(json_file, 'r') as f:
                data = json.load(f)

            for property_data in data:
                property_instance = Property(**property_data)
                property_instance.save()

            self.stdout.write(self.style.SUCCESS(f'Successfully loaded properties from {json_file}'))

        except FileNotFoundError:
            raise CommandError(f'File {json_file} not found')

        except Exception as e:
            raise CommandError(f'Error loading properties from {json_file}: {str(e)}')
