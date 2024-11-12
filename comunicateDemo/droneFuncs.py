from dronekit import VehicleMode,LocationGlobalRelative
import time
import mathFuncs
import math
from pymavlink import mavutil
import matplotlib.pyplot as plt

vehicle=None

def setVehicle(drone):
    global vehicle
    vehicle=drone

def set_drone_velocity(forward_velocity, sideways_velocity):
    """
    Drone'un yerel NED koordinat sisteminde (İleri-Geri, Sağ-Sol) hızını ayarlamak için kullanılır.
    - forward_velocity: İleri (pozitif) veya geri (negatif) hız (m/s)
    - sideways_velocity: Sağ (pozitif) veya sol (negatif) hız (m/s)
    """
    
    msg = vehicle.message_factory.set_position_target_local_ned_encode(
        0,       # time_boot_ms (not used)
        0, 0,    # target system, target component
        mavutil.mavlink.MAV_FRAME_BODY_NED, # frame Needs to be MAV_FRAME_BODY_NED for forward/back left/right control.
        0b0000111111000111, # type_mask
        0, 0, 0, # x, y, z positions (not used)
        forward_velocity, sideways_velocity, 0, # m/s
        0, 0, 0, # x, y, z acceleration
        0, 0)
    vehicle.send_mavlink(msg)
    vehicle.flush()

def go_forward(distance):
    """
    Dronu belirtilen mesafeye kadar ileri götürür.
    - distance: Gitmek istediğin mesafe (metre cinsinden)
    - speed: Hedef hız (m/s)
    """
    
    lat1 = vehicle.location.global_relative_frame.lat
    lon1 = vehicle.location.global_relative_frame.lon
    onlineDist = 0
    lat2,lon2=mathFuncs.calculate_destination(lat1,lon1,get_current_yaw(),distance)

    vehicle.simple_goto(LocationGlobalRelative(lat2, lon2, vehicle.location.global_relative_frame.alt))
    
    while not mathFuncs.upper_error_margin_check(mathFuncs.dist_lat_lon_to_meters(lat2,lon2,vehicle.location.global_relative_frame.lat,vehicle.location.global_relative_frame.lon),0.1,10):
        time.sleep(0.1)
    # print("Gerçek Mesafe (GPS):", mathFuncs.dist_lat_lon_to_meters(vehicle.location.global_relative_frame.lat,vehicle.location.global_relative_frame.lon, lat1, lon1), "m")
    print("Yol TamamLandı")
    
def rotate_drone(angle_degrees):
    """
    Drone'u verilen derece açısına göre en kısa yoldan döndürür.
    - angle_degrees: Döndürmek istediğin açı (derece cinsinden)
    """
    
    yaw1 = mathFuncs.normalize_angle(get_current_yaw())
    target_yaw = mathFuncs.normalize_angle(angle_degrees + yaw1)
    
    # En kısa yoldan dönebilmek için açıyı ayarla
    delta_angle = target_yaw - yaw1
    if delta_angle > 180:
        delta_angle -= 360
    elif delta_angle < -180:
        delta_angle += 360

    # MAV_CMD_CONDITION_YAW komutunu en kısa yolu belirleyerek gönder
    msg = vehicle.message_factory.command_long_encode(
        0, 0,  # hedef sistem ve bileşen kimliği
        mavutil.mavlink.MAV_CMD_CONDITION_YAW,  # komut
        0,  # onaylanmayacak
        yaw1 + delta_angle,  # hedef açıyı en kısa yoldan belirle
        0,  # hız (opsiyonel)
        0,  # relative veya mutlak
        0, 0, 0, 0  # gerekmeyen parametreler
    )
    vehicle.send_mavlink(msg)
    
    onlineDist = 0
    while not mathFuncs.error_margin_check(onlineDist, mathFuncs.normalize_angle(angle_degrees), 3):
        currentYaw = mathFuncs.normalize_angle(get_current_yaw())
        onlineDist = mathFuncs.normalize_angle(currentYaw - yaw1)
        print(yaw1, currentYaw, onlineDist, mathFuncs.normalize_angle(angle_degrees))
        
    vehicle.flush()
    print("Dönüş tamamlandı.")
 
def get_current_yaw():
    """
    Drone'un mevcut yaw (baş) açısını derece cinsinden döndürür.
    """
    # vehicle.attitude.yaw değeri radyan cinsindedir, dereceye çevirmek için kullanıyoruz
    yaw_radians = vehicle.attitude.yaw
    yaw_degrees = math.degrees(yaw_radians)
    return yaw_degrees

def arm_and_takeoff(target_altitude):
    print("Arming motors")
    vehicle.mode = VehicleMode("GUIDED")
    vehicle.armed = True

    while not vehicle.armed:
        print("Waiting for arming...")
        time.sleep(1)

    print("Taking off!")
    vehicle.simple_takeoff(target_altitude)

    while True:
        print("Altitude:", vehicle.location.global_relative_frame.alt)
        if vehicle.location.global_relative_frame.alt >= target_altitude * 0.95:
            print("Target altitude reached")
            break
        time.sleep(0.1)