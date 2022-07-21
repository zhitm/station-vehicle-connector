import math

import dronekit
import sys

from dronekit.mavlink import MAVConnection

# В config файле первая строка - px или sitl
# Вторая - адрес устройства (например, /dev/ttyUSB0 или tcp:192.168.1.105:5780 соответственно)
# Третья - адрес станции (например, udpout:192.168.1.67:2390)
# Четвертая - baudrate, если px
from pymavlink import mavutil

try:
    config_filename = sys.argv[1]
except IndexError:
    print("You should input filename in command line")
    exit()


def read_config():
    baudrate = 115200

    file = open(config_filename, 'r')
    lines = file.readlines()

    vehicle_type = lines[0].strip()
    vehicle_connection_str = lines[1].strip()
    station_connection_str = lines[2].strip()
    if vehicle_type == "px":
        baudrate = lines[3].strip()

    return vehicle_connection_str, station_connection_str, int(baudrate)


def connect_vehicle():
    print("Connecting to vehicle...")
    vehicle = dronekit.connect(vehicle_connection_str, wait_ready=True, baud=baudrate)
    print("Vehicle connected")
    return vehicle


def connect_station():
    print("Connecting to station...")
    connection = MAVConnection(station_connection_str, source_system=1, use_native=True)

    vehicle._handler.pipe(connection)
    connection.forward_message(listener2)
    connection.master.mav.srcComponent = 1
    connection.start()
    print("Station connected")
    return connection


def listener2(self, msg):
    print('TO PX: %s' % msg)
    # pass


def readmission(filename):
    """
    Load a mission from a file into a list. The mission definition is in the Waypoint file
    format (http://qgroundcontrol.org/mavlink/waypoint_protocol#waypoint_file_format).

    This function is used by upload_mission().
    """
    print("Reading mission from file: %s" % filename)
    mission_list = []
    with open(filename) as f:
        for i, line in enumerate(f):
            if i == 0:
                if not line.startswith('QGC WPL 110'):
                    raise Exception('File is not supported WP version')
            else:
                line_array = line.split('\t')
                ln_index = int(line_array[0])
                ln_current_wp = int(line_array[1])
                ln_frame = int(line_array[2])
                ln_command = int(line_array[3])
                ln_param1 = float(line_array[4])
                ln_param2 = float(line_array[5])
                ln_param3 = float(line_array[6])
                ln_param4 = float(line_array[7])
                ln_param5 = float(line_array[8])
                ln_param6 = float(line_array[9])
                ln_param7 = float(line_array[10])
                ln_autocontinue = int(line_array[11].strip())
                cmd = dronekit.Command(0, 0, 0, ln_frame, ln_command, ln_current_wp, ln_autocontinue, ln_param1,
                                       ln_param2, ln_param3, ln_param4, ln_param5, ln_param6, ln_param7)
                mission_list.append(cmd)
    return mission_list


def upload_mission(filename):
    """
    Upload a mission from a file.
    """
    # Read mission from file
    missionlist = readmission(filename)

    print("Upload mission from a file: %s" % filename)
    # Clear existing mission from vehicle
    print("Clear mission")
    cmds = vehicle.commands
    cmds.clear()
    # Add new mission to vehicle
    for command in missionlist:
        cmds.add(command)
    print("Upload mission")
    vehicle.commands.upload()


vehicle_connection_str, station_connection_str, baudrate = read_config()
vehicle = connect_vehicle()
conn = connect_station()

if len(sys.argv) == 3:
    upload_mission(sys.argv[2])


@vehicle.on_message('*')
def listener(self, name, msg):
    print('message FROM PX: %s' % msg)
    pass


while True:
    pass
