#!/usr/bin/env python3
import socket
import sys
from time import sleep
from ev3dev2.port import LegoPort
from ev3dev2.motor import OUTPUT_A, OUTPUT_B, OUTPUT_C, LargeMotor, MediumMotor

brake = LargeMotor(OUTPUT_B)
throttle = LargeMotor(OUTPUT_C)
wheel = MediumMotor(OUTPUT_A)

print("running calibration")
brakeCalib = brake.position
throttleCalib = throttle.position
wheelCalib = wheel.position

print("complete! printing calibration")
print("- brake pedal: ", brakeCalib)
print("- throttle pedal: ", throttleCalib)
print("- steering wheel: ", wheelCalib)

shifterForce = True
throttleForce = True
wheelForce = True

print("attempting server connection")

# The way I got the server IP address is by ssh-ing to the microcontroller twice and using that last login IP address
server_address = ('insert server ip address here', 3000)
server_mode = False

try:
	sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
	sock.connect(server_address)
	sock.setblocking(False)
	server_mode = True
	print("connection success")
except:
	server_mode = False
	print("connection failed")

feedbackLoad = 0
steerRange = 900

print("entering loop")

while True:
	currentBrakePosition = brake.position-brakeCalib
	currentThrottlePosition = throttle.position-throttleCalib
	currentWheelPosition = wheel.position-wheelCalib

	if server_mode == True:
		wheelBytes = currentWheelPosition.to_bytes(4,byteorder='big',signed=True)

		throttlee = -max(-45, min(currentThrottlePosition, 0))
		brakee = max(0, min(currentThrottlePosition, 45))

		shifterPos = 1
		if currentBrakePosition >= 15:
			shifterPos = 2
		elif currentBrakePosition <= -15:
			shifterPos = 0

		brakeBytes = brakee.to_bytes(1,byteorder='big',signed=False)
		throttleBytes = throttlee.to_bytes(1,byteorder='big',signed=False)

		shifterBytes = shifterPos.to_bytes(1,byteorder='big',signed=False)

		#brakeBytes = (-max(-60, min(currentBrakePosition, 0))).to_bytes(1,byteorder='big',signed=False)
		#throttleBytes = (-max(-60, min(currentThrottlePosition, 0))).to_bytes(1,byteorder='big',signed=False)

		sock.sendall(wheelBytes + brakeBytes + throttleBytes + shifterBytes)

		try:
			data = sock.recv(4)
			feedbackLoad = int.from_bytes(data[:4], byteorder='big', signed=True)
			print(feedbackLoad)
		except:
			feedbackLoad = feedbackLoad

	# handle force feedback
	# wheel
	if wheelForce == True:
		customLoad = 0
		if currentWheelPosition <= -steerRange/2:
			customLoad = -(currentWheelPosition+(steerRange/2))
		elif currentWheelPosition >= steerRange/2:
			customLoad = -(currentWheelPosition-(steerRange/2))

		wheelLoad = feedbackLoad + customLoad
		wheel.on(max(-100, min((wheelLoad/255)*100, 100)))

	# shifter
	if shifterForce == True:
		if currentBrakePosition >= 30:
			brake.on(-max(0, min(currentBrakePosition-30, 100))*0.1)
		elif currentBrakePosition <= -30:
			brake.on(max(0, min(-currentBrakePosition+30, 100))*0.1)
		else:
			brake.on(0)


	# throttle
	if throttleForce == True:
		if currentThrottlePosition >= 45:
			throttle.on(-max(0, min(currentThrottlePosition-45, 100))*0.1)
		elif currentThrottlePosition <= -45:
			throttle.on(max(0, min(-currentThrottlePosition+45, 100))*0.1)
		else:
			throttle.on(0)

	sleep(0.01)
