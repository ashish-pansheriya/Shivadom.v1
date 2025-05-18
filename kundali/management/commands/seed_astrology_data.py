from django.core.management.base import BaseCommand
from kundali.models import City
import pytz

class Command(BaseCommand):
    help = 'Seeds initial astrology data'
    
    def handle(self, *args, **options):
        # Major Indian cities
        cities = [
            {'name': 'Delhi', 'latitude': 28.6139, 'longitude': 77.2090, 
             'timezone': 'Asia/Kolkata', 'country': 'India'},
            {'name': 'Mumbai', 'latitude': 19.0760, 'longitude': 72.8777, 
             'timezone': 'Asia/Kolkata', 'country': 'India'},
            {'name': 'Chennai', 'latitude': 13.0827, 'longitude': 80.2707, 
             'timezone': 'Asia/Kolkata', 'country': 'India'},
            {'name': 'Kolkata', 'latitude': 22.5726, 'longitude': 88.3639, 
             'timezone': 'Asia/Kolkata', 'country': 'India'},
            {'name': 'Bangalore', 'latitude': 12.9716, 'longitude': 77.5946, 
             'timezone': 'Asia/Kolkata', 'country': 'India'},
            {'name': 'Hyderabad', 'latitude': 17.3850, 'longitude': 78.4867, 
             'timezone': 'Asia/Kolkata', 'country': 'India'},
            {'name': 'New York', 'latitude': 40.7128, 'longitude': -74.0060, 
             'timezone': 'America/New_York', 'country': 'USA'},
            {'name': 'London', 'latitude': 51.5074, 'longitude': -0.1278, 
             'timezone': 'Europe/London', 'country': 'UK'},
        ]
        
        for city_data in cities:
            City.objects.get_or_create(**city_data)
        
        self.stdout.write(self.style.SUCCESS('Successfully seeded astrology data'))