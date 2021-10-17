***Project Neriak Overview***

**Project Goals**

The goal for this project is to provide the means to meaningfully streamline the control of a player character in *EverQuest,* from automating repetitive actions up to complete autonomous control in certain cases. 

**Overview**

Neriak implements a player agent in the form of a multi-threaded producer and consumer model with setup and shared resource initialization coordinated by a controller. Player agent behaviors are defined in a 
custom *Persona* which is implemented as a Python Module and Class. In this class are defined all member variables and functions that maintain state an perform actions on behalf of the agent. The name of the
Persona module you wish to load is passed into the program as an argument, otherwise the *Default* persona is used.


**A Simple Example**

TODO: Add examples

**DEPENDANCIES**

TODO: Add virtual environment support

pip3 install pyautogui
pip3 install pydirectinput
pip3 install requests
pip3 install pywin32

