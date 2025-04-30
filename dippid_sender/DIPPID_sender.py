import json
import random
import socket
import time
import math

IP = '127.0.0.1'
PORT = 5700

sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

counter = 0
accelerometer_counter = 0
while True:
    message = '{"heartbeat" : ' + str(counter) + '}'
    print("in while true loop in dippid_sender.py: "+message)
    sock.sendto(message.encode(), (IP, PORT))

    if(random.randint(0, 10) > 8):
        print("clicked randomly")
        message = {
            "button_1": "clicked at random at tick"+str(counter)
        }
        sock.sendto(json.dumps(message).encode(), (IP, PORT))
    
    accelerometer_counter+=1
    x = math.sin(0.1*accelerometer_counter)
    y = math.sin(0.12*accelerometer_counter)
    z = math.sin(0.14*accelerometer_counter)
    message = {
        "accelerometer": {
            "x": x,
            "y": y,
            "z": z
        }
    }
    sock.sendto(json.dumps(message).encode(), (IP, PORT))

    counter += 1
    time.sleep(1)
