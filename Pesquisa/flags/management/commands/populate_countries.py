from django.core.management.base import BaseCommand
from django.db import transaction
from flags.models import Country


class Command(BaseCommand):
    help = 'Populate the database with common countries and their flag codes'

    def add_arguments(self, parser):
        parser.add_argument(
            '--clear',
            action='store_true',
            help='Clear existing countries before populating',
        )

    def handle(self, *args, **options):
        # List of common countries with their ISO codes and names
        countries_data = [
            ('BR', 'Brazil'),
            ('US', 'United States'),
            ('CA', 'Canada'),
            ('MX', 'Mexico'),
            ('AR', 'Argentina'),
            ('CL', 'Chile'),
            ('CO', 'Colombia'),
            ('PE', 'Peru'),
            ('VE', 'Venezuela'),
            ('UY', 'Uruguay'),
            ('GB', 'United Kingdom'),
            ('DE', 'Germany'),
            ('FR', 'France'),
            ('ES', 'Spain'),
            ('IT', 'Italy'),
            ('PT', 'Portugal'),
            ('NL', 'Netherlands'),
            ('BE', 'Belgium'),
            ('CH', 'Switzerland'),
            ('AT', 'Austria'),
            ('SE', 'Sweden'),
            ('NO', 'Norway'),
            ('DK', 'Denmark'),
            ('FI', 'Finland'),
            ('IS', 'Iceland'),
            ('IE', 'Ireland'),
            ('PL', 'Poland'),
            ('CZ', 'Czech Republic'),
            ('SK', 'Slovakia'),
            ('HU', 'Hungary'),
            ('RO', 'Romania'),
            ('BG', 'Bulgaria'),
            ('HR', 'Croatia'),
            ('SI', 'Slovenia'),
            ('GR', 'Greece'),
            ('TR', 'Turkey'),
            ('RU', 'Russia'),
            ('UA', 'Ukraine'),
            ('CN', 'China'),
            ('JP', 'Japan'),
            ('KR', 'South Korea'),
            ('IN', 'India'),
            ('TH', 'Thailand'),
            ('VN', 'Vietnam'),
            ('ID', 'Indonesia'),
            ('MY', 'Malaysia'),
            ('SG', 'Singapore'),
            ('PH', 'Philippines'),
            ('AU', 'Australia'),
            ('NZ', 'New Zealand'),
            ('ZA', 'South Africa'),
            ('NG', 'Nigeria'),
            ('EG', 'Egypt'),
            ('MA', 'Morocco'),
            ('KE', 'Kenya'),
            ('GH', 'Ghana'),
            ('ET', 'Ethiopia'),
            ('IL', 'Israel'),
            ('SA', 'Saudi Arabia'),
            ('AE', 'United Arab Emirates'),
            ('QA', 'Qatar'),
            ('KW', 'Kuwait'),
            ('JO', 'Jordan'),
            ('LB', 'Lebanon'),
            ('IQ', 'Iraq'),
            ('IR', 'Iran'),
            ('AF', 'Afghanistan'),
            ('PK', 'Pakistan'),
            ('BD', 'Bangladesh'),
            ('LK', 'Sri Lanka'),
            ('MM', 'Myanmar'),
            ('NP', 'Nepal'),
        ]

        if options['clear']:
            self.stdout.write('Clearing existing countries...')
            Country.objects.all().delete()

        created_count = 0
        updated_count = 0

        with transaction.atomic():
            for code, name in countries_data:
                country, created = Country.objects.get_or_create(
                    code=code,
                    defaults={
                        'name': name,
                        'flag_code': code.lower(),
                        'is_active': True,
                    }
                )
                
                if created:
                    created_count += 1
                    self.stdout.write(
                        self.style.SUCCESS(f'Created: {country.name} ({country.code})')
                    )
                else:
                    # Update name if it's different
                    if country.name != name:
                        country.name = name
                        country.save()
                        updated_count += 1
                        self.stdout.write(
                            self.style.WARNING(f'Updated: {country.name} ({country.code})')
                        )

        self.stdout.write(
            self.style.SUCCESS(
                f'\nPopulation complete!\n'
                f'Created: {created_count} countries\n'
                f'Updated: {updated_count} countries\n'
                f'Total: {Country.objects.count()} countries in database'
            )
        )