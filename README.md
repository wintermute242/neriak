***Project Neriak Overview***

**Project Goals**

The goal for this project is to provide the means to meaningfully streamline the control of a player character in *EverQuest,* from automating repetitive actions up to complete autonomous control in certain cases. 

**Overview**

Neriak implements a player agent in the form of a multi-threaded producer and consumer model with setup and shared resource initialization coordinated by a controller. Player agent behaviors are defined in a 
custom *Persona* which is implemented as a Python Module and Class. In this class are defined all member variables and functions that maintain state an perform actions on behalf of the agent. The name of the
Persona module you wish to load is passed into the program as an argument, otherwise the *Default* persona is used.

This design follows the pattern of dependency injection such that all behavior is defined in the module that is passed into the Controller, and control of execution is periodically returned to the persona when
either an event is triggered or after a certain amount of time has passed. This not only allows the persona to react immediately to events as they occur, but also because control is periodically returned, even if no events 
are triggered the persona is given opportunity to update internal state and do other things like check timers that have been started, and act if necessary. 


**A Simple Example**

TODO: Add examples

**DEPENDENCIES**

TODO: Add virtual environment support

pip3 install pyautogui
pip3 install pydirectinput
pip3 install requests
pip3 install pywin32

