# CAN-bus_Diagnostics
This system is responsible for monitoring a given CAN bus line and detecting errors in the bus.

It consists of a Raspberry Pi 3 with touch screen and a PCB that converts the CANbus messages to SPI so as to be read from the RPi

The main_app.py has to be executed to run the code after the following line has been written to the terminal:
* sudo ip link set can0 up type can bitrate 1000000
                  ,to establish a CAN bus communication at a bitrate of 1Mbps (or the bitrate of the specific application).

Further documentation is uploaded in the repository (CAN_Diagnostics Documentation)
