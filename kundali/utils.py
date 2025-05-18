# kundali/utils.py
from flatlib import const
from flatlib.datetime import Datetime
from flatlib.geopos import GeoPos
from flatlib.chart import Chart

def get_d1_chart(birth_datetime, lat, lon, tz):
    date = birth_datetime.strftime('%Y/%m/%d')
    time = birth_datetime.strftime('%H:%M:%S')
    flatlib_datetime = Datetime(date, time, tz)
    pos = GeoPos(lat, lon)
    return Chart(flatlib_datetime, pos, IDs=const.LIST_OBJECTS, hsys=const.HOUSES_PLACIDUS)

def get_gochar_chart(current_datetime, lat, lon, tz):
    date = current_datetime.strftime('%Y/%m/%d')
    time = current_datetime.strftime('%H:%M:%S')
    flatlib_datetime = Datetime(date, time, tz)
    pos = GeoPos(lat, lon)
    return Chart(flatlib_datetime, pos, IDs=const.LIST_OBJECTS, hsys=const.HOUSES_PLACIDUS)

def get_planet_info(planet):
    return {
        'id': planet.id,
        'name': planet.id.lower().capitalize(),
        'sign': const.LIST_SIGNS[planet.sign],
        'signPos': planet.signPos,
        'lon': planet.lon,
        'lat': planet.lat,
    }