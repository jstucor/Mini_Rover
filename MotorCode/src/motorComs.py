import serial
#import keyboard
import time

# This is code for testing the serial writing in python and the steering

#115200
ser = serial.Serial('/dev/ttyACM0', baudrate=115200, timeout=1)


while True:
	for i in range(40):
		ser.write(b"right\n")
		time.sleep(0.05)

	for i in range(40):
		ser.write(b"left\n")
		time.sleep(0.05)

	for i in range(40):
		ser.write(b"forward\n")
		time.sleep(0.05)


"""
def on_key_release(key):
	if key == Key.right:
		print("Right key clicked")
	elif key == Key.left:
		print("Left key clicked")
	elif key == Key.up:
		print("Up key clicked")
	elif key == Key.down:
		print("Down key clicked")
	elif key == Key.esc:
		return False  # Stop listener

with keyboard.Listener(on_release=on_key_release) as listener:
	listener.join()
"""

"""
while True:
	if keyboard.is_pressed('left'):
		print('You Pressed left!')
	elif keyboard.is_pressed('right'):
		print('You Pressed right!')
	elif keyboard.is_pressed('down'):
		print('You Pressed down!')
	elif keyboard.is_pressed('up'):
		print('You Pressed up!')
	elif keyboard.is_pressed('esc'):
		break
	time.sleep(0.1)  # Prevent multiple detections"
"""