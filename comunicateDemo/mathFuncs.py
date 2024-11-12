import math
from geopy.distance import geodesic
from geopy import Point


def dist_lat_lon_to_meters(lat1, lon1, lat2, lon2):
    """
    İki enlem ve boylam noktası arasındaki mesafeyi metre cinsinden hesaplar.
    - lat1, lon1: Başlangıç enlem ve boylamı
    - lat2, lon2: Hedef enlem ve boylamı
    """
    # Dünya yarıçapı (metre cinsinden)
    R = 6378137.0

    # Radyan cinsinden enlem ve boylam farkı
    d_lat = math.radians(lat2 - lat1)
    d_lon = math.radians(lon2 - lon1)

    # Haversine formülü
    a = math.sin(d_lat / 2) ** 2 + math.cos(math.radians(lat1)) * math.cos(math.radians(lat2)) * math.sin(d_lon / 2) ** 2
    c = 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a))

    # İki nokta arasındaki mesafe
    distance = R * c
    return distance

def error_margin_check(number, target, error_margin):
    """
    Checks if the given number is within the error margin of the target value.

    :param number: The number to check
    :param target: The target value
    :param error_margin: The error margin percentage (e.g., for 5% use 5)
    :return: A tuple with a boolean indicating if it's in range, and the lower and upper limits
    """
    lower_limit = target * (1 - error_margin / 100)
    upper_limit = target * (1 + error_margin / 100)

    return lower_limit <= number <= upper_limit

def lower_error_margin_check(number, target, error_margin):
    """
    Checks if the given number is within the error margin of the target value.

    :param number: The number to check
    :param target: The target value
    :param error_margin: The error margin percentage (e.g., for 5% use 5)
    """
    lower_limit = target * (1 - error_margin / 100)

    return lower_limit <= number 

def upper_error_margin_check(number, target, error_margin):
    """
    Checks if the given number is within the error margin of the target value.

    :param number: The number to check
    :param target: The target value
    :param error_margin: The error margin percentage (e.g., for 5% use 5)
    """
    upper_limit = target * (1 + error_margin / 100)

    return  number <= upper_limit

def normalize_angle(angle):
    """
    Açıyı 0 ile 360 derece arasına normalleştirir.
    """
    normalized_angle = angle % 360
    return normalized_angle




def calculate_destination(lat, lon, azimuth, distance_m):
    distance_km=distance_m/1000
    # Başlangıç noktası (drone'un mevcut koordinatları)
    start_point = Point(lat, lon)
    
    # Enlem ve boylam farkını hesaplayalım
    # Azimut, drone'un bakış açısını (derece cinsinden) temsil eder
    azimuth_rad = math.radians(azimuth)  # Dereceyi radiana çevir

    # Dünya'nın yarıçapını (km cinsinden) kabul ediyoruz
    radius = 6371.0  # km

    # Azimut doğrultusunda mesafeyi hareket ettiriyoruz
    delta_lat = (distance_km / radius) * math.cos(azimuth_rad)
    delta_lon = (distance_km / radius) * math.sin(azimuth_rad) / math.cos(math.radians(lat))

    # Hedef noktayı hesapla
    destination_lat = lat + math.degrees(delta_lat)
    destination_lon = lon + math.degrees(delta_lon)

    return destination_lat, destination_lon