# Project 2: Multi-Agent Search

This project designed agents for the classic version of Pacman, including ghosts. 
Along the way, I implemented both minimax and expectimax search and the evaluation function design.

To grade answers on your machine. This can be run on all questions with the command:
```python
python autograder.py
```
The code for this project contains the following files:

| Files you'll edit: | |
|:---|---------|
|```multiAgents.py```	|Where all of your multi-agent search agents will reside.|
|**Files you might want to look at:**| |
|```pacman.py```	|The main file that runs Pacman games. This file also describes a Pacman GameState type, which you will use extensively in this project.|
|```game.py```	|The logic behind how the Pacman world works. This file describes several supporting types like AgentState, Agent, Direction, and Grid.|
|```util.py```	|Useful data structures for implementing search algorithms. You don't need to use these for this project, but may find other functions defined here to be useful.|
|**Supporting files you can ignore:**| |
```graphicsDisplay.py```|	Graphics for Pacman
```graphicsUtils.py```|	Support for Pacman graphics
```textDisplay.py```|	ASCII graphics for Pacman
```ghostAgents.py```|	Agents to control ghosts
```keyboardAgents.py```|	Keyboard interfaces to control Pacman
```layout.py```	|Code for reading layout files and storing their contents
```autograder.py```	|Project autograder
```testParser.py```	|Parses autograder test and solution files
```testClasses.py```|	General autograding test classes
```test_cases/```|Directory containing the test cases for each question
```multiagentTestClasses.py```|Project 3 specific autograding test classes
