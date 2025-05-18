from django.shortcuts import render
from django.http import JsonResponse
from .models import City, KundaliRequest
from .utils import get_d1_chart, get_gochar_chart, get_planet_info, get_aspects
from datetime import datetime
import pytz
from geopy.geocoders import Nominatim
import json
from django.views.decorators.http import require_http_methods
from django.core.cache import cache
from geopy.exc import GeocoderTimedOut, GeocoderUnavailable
from django.shortcuts import render
from django.http import JsonResponse
from datetime import datetime
import pytz
from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse
from .models import City, KundaliRequest
from .utils import get_d1_chart, get_gochar_chart
from datetime import datetime
import pytz
from django.views.decorators.http import require_http_methods
from geopy.geocoders import Nominatim
from geopy.exc import GeocoderTimedOut, GeocoderUnavailable
import pytz
# kundali/views.py
from django.shortcuts import render
from django.http import JsonResponse
from django.views.decorators.http import require_http_methods
from django.views.decorators.csrf import csrf_exempt
from geopy.geocoders import Nominatim
from geopy.exc import GeocoderTimedOut, GeocoderUnavailable
from datetime import datetime
import pytz
import logging

logger = logging.getLogger(__name__)

def kundali_home(request):
    return render(request, 'kundali/home.html')

@csrf_exempt
def generate_kundali(request):
    if request.method == 'POST':
        try:
            # Parse date in DD.MM.YYYY format
            birth_date_str = request.POST.get('birth_date')
            day, month, year = map(int, birth_date_str.split('.'))
            birth_date = f"{year}-{month:02d}-{day:02d}"
            
            birth_time = request.POST.get('birth_time')
            latitude = request.POST.get('latitude')
            longitude = request.POST.get('longitude')
            timezone = request.POST.get('timezone')
            
            # Validate inputs
            if not all([birth_date, birth_time, latitude, longitude, timezone]):
                return JsonResponse({
                    'success': False,
                    'error': 'All fields are required'
                }, status=400)
            
            # Parse datetime
            birth_datetime = datetime.strptime(f"{birth_date} {birth_time}", "%Y-%m-%d %H:%M")
            
            # Generate charts using your existing utils
            from .utils import get_d1_chart, get_gochar_chart
            d1_chart = get_d1_chart(birth_datetime, float(latitude), float(longitude), timezone)
            current_datetime = datetime.now(pytz.timezone(timezone))
            gochar_chart = get_gochar_chart(current_datetime, float(latitude), float(longitude), timezone)
            
            # Prepare response
            return JsonResponse({
                'success': True,
                'd1_chart': {
                    'planets': {planet.id: get_planet_info(planet) for planet in d1_chart.planets},
                    'ascendant': const.LIST_SIGNS[d1_chart.get(const.ASC).sign],
                },
                'gochar_chart': {
                    'planets': {planet.id: get_planet_info(planet) for planet in gochar_chart.planets},
                    'current_time': current_datetime.strftime("%d.%m.%Y %H:%M %Z")
                }
            })
            
        except Exception as e:
            logger.error(f"Error generating kundali: {str(e)}")
            return JsonResponse({
                'success': False,
                'error': str(e)
            }, status=500)
    
    return JsonResponse({'error': 'Invalid method'}, status=405)

@require_http_methods(["GET"])
def search_location(request):
    query = request.GET.get('q', '').strip()
    if len(query) < 2:
        return JsonResponse([], safe=False)
    
    try:
        geolocator = Nominatim(user_agent="kundali_app")
        locations = geolocator.geocode(query, exactly_one=False, limit=5) or []
        
        results = []
        for loc in locations:
            try:
                timezone = pytz.timezone_at(lng=loc.longitude, lat=loc.latitude)
            except:
                timezone = 'Asia/Kolkata'  # Default to Indian timezone
                
            results.append({
                'name': loc.address,
                'latitude': loc.latitude,
                'longitude': loc.longitude,
                'timezone': timezone
            })
        
        return JsonResponse(results, safe=False)
    
    except (GeocoderTimedOut, GeocoderUnavailable) as e:
        logger.error(f"Geocoder error: {str(e)}")
        return JsonResponse([], safe=False)
    except Exception as e:
        logger.error(f"Location search error: {str(e)}")
        return JsonResponse({'error': str(e)}, status=500)

@csrf_exempt
def generate_kundali(request):
    if request.method == 'POST':
        try:
            # Get form data
            birth_date = request.POST.get('birth_date')
            birth_time = request.POST.get('birth_time')
            city_id = request.POST.get('city')
            
            if not all([birth_date, birth_time, city_id]):
                return JsonResponse({
                    'success': False,
                    'error': 'All fields are required'
                }, status=400)
            
            # Get city details
            try:
                city = City.objects.get(id=city_id)
            except City.DoesNotExist:
                return JsonResponse({
                    'success': False,
                    'error': 'Invalid city selected'
                }, status=400)
            
            # Parse date and time
            try:
                birth_datetime = datetime.strptime(f"{birth_date} {birth_time}", "%Y-%m-%d %H:%M")
            except ValueError:
                return JsonResponse({
                    'success': False,
                    'error': 'Invalid date or time format'
                }, status=400)
            
            # Get current time for Gochar
            current_datetime = datetime.now(pytz.timezone(city.timezone))
            
            # Generate charts
            try:
                d1_chart = get_d1_chart(birth_datetime, float(city.latitude), float(city.longitude), city.timezone)
                gochar_chart = get_gochar_chart(current_datetime, float(city.latitude), float(city.longitude), city.timezone)
            except Exception as e:
                return JsonResponse({
                    'success': False,
                    'error': f'Error generating charts: {str(e)}'
                }, status=500)
            
            # Prepare D1 chart data
            d1_data = {
                'planets': {planet.id: get_planet_info(planet) for planet in d1_chart.planets},
                'houses': [house.sign for house in d1_chart.houses],
                'ascendant': const.LIST_SIGNS[d1_chart.get(const.ASC).sign],
                'aspects': get_aspects(d1_chart),
                'birth_details': {
                    'date': birth_date,
                    'time': birth_time,
                    'place': city.name,
                    'coordinates': f"{city.latitude}, {city.longitude}",
                    'timezone': city.timezone
                }
            }
            
            # Prepare Gochar chart data
            gochar_data = {
                'planets': {planet.id: get_planet_info(planet) for planet in gochar_chart.planets},
                'houses': [house.sign for house in gochar_chart.houses],
                'ascendant': const.LIST_SIGNS[gochar_chart.get(const.ASC).sign],
                'aspects': get_aspects(gochar_chart),
                'current_time': current_datetime.strftime("%Y-%m-%d %H:%M:%S %Z")
            }
            
            # Save the request
            KundaliRequest.objects.create(
                birth_date=birth_date,
                birth_time=birth_time,
                latitude=city.latitude,
                longitude=city.longitude,
                timezone=city.timezone,
                city=city
            )
            
            return JsonResponse({
                'success': True,
                'd1_chart': d1_data,
                'gochar_chart': gochar_data
            })
            
        except Exception as e:
            return JsonResponse({
                'success': False,
                'error': str(e)
            }, status=500)
    
    return JsonResponse({
        'success': False,
        'error': 'Invalid request method'
    }, status=405)

def get_cities(request):
    query = request.GET.get('q', '')
    cities = City.objects.filter(name__icontains=query)[:10]
    data = [{
        'id': city.id,
        'name': f"{city.name}, {city.country}",
        'latitude': str(city.latitude),
        'longitude': str(city.longitude),
        'timezone': city.timezone
    } for city in cities]
    return JsonResponse(data, safe=False)

@require_http_methods(["GET"])
def search_location(request):
    query = request.GET.get('q', '').strip()
    if len(query) < 3:
        return JsonResponse([], safe=False)
    
    try:
        geolocator = Nominatim(user_agent="kundali_app")
        locations = geolocator.geocode(query, exactly_one=False, limit=5) or []
        
        results = []
        for loc in locations:
            try:
                timezone = pytz.timezone_at(lng=loc.longitude, lat=loc.latitude)
            except:
                timezone = 'UTC'
            
            results.append({
                'name': loc.address,
                'latitude': loc.latitude,
                'longitude': loc.longitude,
                'timezone': timezone
            })
        
        return JsonResponse(results, safe=False)
    
    except (GeocoderTimedOut, GeocoderUnavailable):
        return JsonResponse([], safe=False)
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=500)

# kundali/views.py


@require_http_methods(["GET"])
def search_location(request):
    query = request.GET.get('q', '').strip()
    if len(query) < 2:
        return JsonResponse({'error': 'Query too short'}, status=400)
    
    cache_key = f'location_search_{query.lower()}'
    locations = cache.get(cache_key)
    
    if locations is None:
        try:
            locations = geolocator.geocode(
                query,
                exactly_one=False,
                limit=5,
                timeout=10
            ) or []
            
            # Cache valid results
            if locations:
                cache.set(cache_key, locations, timeout=60*60*24)  # 24 hours
            
        except (GeocoderTimedOut, GeocoderUnavailable) as e:
            return JsonResponse({
                'error': 'Location service unavailable. Please try again later.'
            }, status=503)
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=500)
    
    results = []
    for loc in locations:
        results.append({
            'name': loc.address,
            'latitude': loc.latitude,
            'longitude': loc.longitude,
            'timezone': 'Asia/Kolkata'  # You'll need to implement timezone lookup
        })
    
    return JsonResponse(results, safe=False)



def kundali_home(request):
    # Static data to mimic Drikpanchang when database isn't available
    context = {
        'd1_chart': get_static_d1_chart(),
        'gochar_chart': get_static_gochar_chart(),
        'server_running': True,
        'kundali_available': False,
        'location_available': False
    }
    return render(request, 'kundali/home.html', context)

def get_static_d1_chart():
    """Return static D1 chart data"""
    return {
        'planets': {
            'Sun': {'sign': 'Aries', 'position': '12°34'},
            'Moon': {'sign': 'Taurus', 'position': '5°12'},
            # Add all planets...
        },
        'houses': ['Aries', 'Taurus', 'Gemini', 'Cancer', 'Leo', 'Virgo',
                  'Libra', 'Scorpio', 'Sagittarius', 'Capricorn', 'Aquarius', 'Pisces'],
        'ascendant': 'Leo'
    }

def get_static_gochar_chart():
    """Return static Gochar chart data"""
    return {
        'planets': {
            'Sun': {'sign': 'Gemini', 'position': '18°45'},
            'Moon': {'sign': 'Scorpio', 'position': '23°12'},
            # Add all planets...
        },
        'current_time': datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    }