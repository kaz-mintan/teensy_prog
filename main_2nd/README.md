## hardware components
- firmware/

	- sma_act/sma_act.ino

		- without serial communication, it actuate a sma.

	- read_ir/read_ir.ino

		- without serial communication, it read the value of ir sensor

	- serial_sma/serial_sma.ino

		- actuate sma based on a value of pwm which is sent by serial communication.
		- it may have time delay

	- serial_read/serial_ir.ino

		- output the value of ir sensor by serial communication.

## communication components in PC

- serial_com/

	- serial_sma.py

		- after running the serial_sma/serial_sma.ino, it can actuate the motion of the sma to input the value of pwm into your console.

		- command: python serial_sma.py

	- serial_read.py

		- after runnning the serial_read/serial_ir.ino, it can get the value of the ir sensor which are sent by serial communication.

		- command: python serial_read.py

	- serial_double.py

		- connect sma to '/dev/ttyACMO'

		- connect ir to '/dev/ttyACM1'

		- output the value of ir sensor continuously,

		- when you input the value of pwm into bash, sma starts to move

- socket_com/

	- socket_face.py

		- receive the value of facial expressions by socket communication
