import serial

import time

# ports = list(serial.tools.list_ports.grep("ttyACM0"))

# if len(ports) > 0:
#     serial_port = serial.Serial("/dev/ttyACM0", baudrate=115200, timeout=1)
#     print(serial_port)
# else:
#     print("Unable to find Arduino")

serial_port = serial.Serial('/dev/ttyACM0', baudrate=115200, timeout=1)

time.sleep(2)

# serial_port.write(b"medium\n")
serial_port.write(f"forward\n".encode())

time.sleep(2)

serial_port.write(b"stop\n")