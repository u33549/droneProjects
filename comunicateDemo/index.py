from dronekit import connect, VehicleMode
import droneFuncs
# Drone'a bağlan
connection_string = "127.0.0.1:14550"
print(f"Connecting to drone on: {connection_string}")
vehicle = connect(connection_string, wait_ready=True)

droneFuncs.setVehicle(vehicle)
droneFuncs.arm_and_takeoff(5)
# droneFuncs.rotate_drone(90)
# droneFuncs.go_forvard(50)

# Drone'u araca güvenli bir şekilde kapatma
vehicle.close()