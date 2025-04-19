import socket
import sys
from time import sleep
import vgamepad as vg

gamepad = vg.VX360Gamepad()
steerPos = 0
forceFeedback = 0

server_address = ('', 3000)
sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
sock.bind(server_address)
sock.listen(1)

connection = None

def my_callback(client, target, large_motor, small_motor, led_number, user_data):
	forceFeedback = small_motor
	if connection != None:
		print(forceFeedback)
		connection.sendall(forceFeedback.to_bytes(4,byteorder='big',signed=True))

gamepad.register_notification(callback_function=my_callback)

while True:

	print('waiting for a connection')
	con, client_address = sock.accept()
	try:
		connection = con
		print('connection from', client_address)

		# Receive the data in small chunks and retransmit it
		while True:
			data = connection.recv(7)
			pos = int.from_bytes(data[:4], byteorder='big', signed=True)
			brake = int.from_bytes(data[4:][:1], byteorder='big', signed=False)
			throttle = int.from_bytes(data[5:][:1], byteorder='big', signed=False)
			shifter = int.from_bytes(data[6:][:1], byteorder='big', signed=False)

			#print("current pos: ", throttle)
			#print("current force: ", forceFeedback)
			steerPos = pos
			actualPos = max(-1, min(steerPos/900, 1))

			if shifter == 2:
				gamepad.press_button(button=vg.XUSB_BUTTON.XUSB_GAMEPAD_LEFT_SHOULDER)
				gamepad.release_button(button=vg.XUSB_BUTTON.XUSB_GAMEPAD_A)
				gamepad.press_button(button=vg.XUSB_BUTTON.XUSB_GAMEPAD_X)
			elif shifter == 0:
				gamepad.press_button(button=vg.XUSB_BUTTON.XUSB_GAMEPAD_LEFT_SHOULDER)
				gamepad.press_button(button=vg.XUSB_BUTTON.XUSB_GAMEPAD_A)
				gamepad.release_button(button=vg.XUSB_BUTTON.XUSB_GAMEPAD_X)
			else:
				gamepad.release_button(button=vg.XUSB_BUTTON.XUSB_GAMEPAD_LEFT_SHOULDER)
				gamepad.release_button(button=vg.XUSB_BUTTON.XUSB_GAMEPAD_A)
				gamepad.release_button(button=vg.XUSB_BUTTON.XUSB_GAMEPAD_X)

			gamepad.left_trigger_float(value_float=(brake/45))
			gamepad.right_trigger_float(value_float=(throttle/45))
			gamepad.left_joystick_float(x_value_float=actualPos, y_value_float=0)
			gamepad.update()
	#except:
	#	print("Error occurred, disconnecting")
	#	connection.close()
	except KeyboardInterrupt:
		break
	finally:
		print("disconnected")
		connection.close()

	sleep(0.01)