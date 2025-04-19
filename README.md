# ev3dev-steering-wheel
A (bad) sim steering wheel using LEGO EV3 parts with horrible force feedback.

I am open sourcing it now because I can't really use it long-term due to batteries. The motors use a significant amount of battery energy, and it also DROPS the voltage down. At times I've had it drop down wayy below 5 volts, which automatically triggered a power off in the OS. On top of that, I am not gonna be using this all the time. i just want to do more stupid stuff with lego

# Disclaimer
EV3 motors HAVE torque. It is actually difficult to turn while they're being powered. This creates a risk of breaking components and draining your battery, or something worse could also happen. If any of those happen, the responsibility is yours. This is entirely a prototype, I am releasing the source code for anyone who wants to build on top of it.
This also assumes you know what you're doing in terms of Linux and Python. I am not going to provide support for this project.

# Setup
The way I have set this up is a bit different from traditional steering wheels and pedals. One large motor is used for the gear shifter, which also acts as the clutch at the same time. Another large motor is used for the throttle and brake. I only have one microcontroller. This is all I had to play with.

# Hardware
This all is LEGO EV3 Mindstorms stuff
- Microcontroller (the brain of the operation)
- 1 medium motor (handles the steering)
- 2 large motors (one handles gear shifting & clutch, one handles throttle & brake)

# Software
The microcontroller must run [ev3dev](https://www.ev3dev.org/) for this to work. Regular BrickOS wont work.
All the code is in Python. The ``server.py`` file runs on the computer you want to play a game like BeamNG.Drive on. The ``client.py`` file runs on the microcontroller itself.

The server setups a virtual gamepad using ``vgamepad``, so you must have that library and the ViGEM driver installed (installing that library will also install the driver automatically). Then it starts a TCP server at the port 3000, at which it'll wait for a connection. You then run ``client.py`` on the microcontroller via SSH or PuTTY. If the server shows connection from a IP address, verify that its the microcontroller address. The microcontroller should also show if it successfully connected or not. Once it all is functional, you can start a game like BeamNG and play around!

The code may be horrible, but it wasn't made for production either.

# BeamNG
This was made to be used in BeamNG specifically. You must change some stuff in the Force Feedback section in Controls. Here are my settings:
![image](https://i.imgur.com/Otcmlxi.png)
![image](https://i.imgur.com/rV4cXB5.png)