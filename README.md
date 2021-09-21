***Project Neriak Overview***

**Summary**

The goal for this project is to provide the means to meaningfully streamline the control of a player character in *EverQuest,* from automating repetitive actions up to complete autonomous control in certain cases. 

**Components**

At the highest level is something called the *Agent*, which is the top level construct which sends keyboard and mouse input to the game client based on input from the game logs. This could be activated by saying a trigger word to the agent in game, or by responding to events as read from the log files. 

An agent operates by performing *actions*. An *action* is composed of a *task* and one or more *triggers*. A task defines the actual output sent by the agent to the game client which accomplishes the desired action. This can be any combination of button presses or mouse clicks. A trigger defines exactly what circumstances will cause an agent to perform the associated task. This could be as simple as seeing an expected trigger word in the log text, or as complex as keeping track of damage received over a particular interval to trigger casting a heal spell. One or more triggers may be associated with a single task. 

**A Simple Example**
