# rainforce learning program

## main program
- motion_dqn.py

	- is main program.
	- output possible appropriate parameters of motion.
	- uses some modules as below,

		- neural_network.py
			- as a Q function
			- and to predict the next facial expression based on the information of state.

		- reward_function.py
			- to calculate reward based on the gained facial expression and other information( ex. error of prediction facial expression)

		- sequence.py
			- to calculate the features of time sequence data of facial expression and ir sensor.

## simulation mode
- in a simlation mode, motion_dqn.py uses the modules which are shown below.

	- dummy_evaluator.py
		- to get dummy facial expression as an evaluator.
	- hand_motion.py
		- to get dummy information of ir sensor.
