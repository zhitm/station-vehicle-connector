# В config файле первая строка - px или sitl
# Вторая - адрес устройства (например, /dev/ttyUSB0 или tcp:192.168.1.105:5780 соответственно)
# Третья - адрес станции (например, udpout:192.168.1.67:2390)
# Четвертая - baudrate, если px

Примеры запуска: 

python3 station_vehicle_connector.py config_sitl.txt mission.waypoints

python3 station_vehicle_connector.py config_sitl.txt

Первый аргумент обязателен и содержит путь к файлу с конфигурациями.
Второй - опционален и содержит путь к waypoints.