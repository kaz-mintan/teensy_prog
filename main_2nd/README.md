# develop branch to debug!

## hardware components
- firmware/

	- sma_act/sma_act.ino

		- without serial communication, it actuate a sma.

	- read_ir/read_ir.ino

		- without serial communication, it read the value of ir sensor

	- serial_sma/serial_sma.ino

		- actuate sma based on a value of pwm which is sent by serial communication.
		- it may have time delay
