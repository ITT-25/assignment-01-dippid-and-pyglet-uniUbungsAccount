from DIPPID import SensorUDP

# use UPD (via WiFi) for communication
PORT = 5700
sensor = SensorUDP(PORT)

def handle_hearbeat(data):
    print("recieved data successfully: ")
    print(data)

def handle_button1(data):
    print("recieved click data: ")
    print(data)

def handle_accelerometer(data):
    print("recieved accelerometer data: ")
    print(data)

sensor.register_callback('heartbeat', handle_hearbeat)
sensor.register_callback('button_1', handle_button1)
sensor.register_callback('accelerometer', handle_accelerometer)
