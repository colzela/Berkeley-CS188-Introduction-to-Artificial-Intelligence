# Project 1: Search

Introduction
In this project, your Pacman agent will find paths through his maze world, both to reach a particular location and to collect food efficiently. You will build general search algorithms and apply them to Pacman scenarios

As in Project 0, this project includes an autograder for you to grade your answers on your machine. This can be run with the command:
```
python autograder.py
```
See the autograder tutorial in Project 0 for more information about using the autograder.

The code for this project consists of several Python files, some of which you will need to read and understand in order to complete the assignment, and some of which you can ignore.
|Files you'll edit:| |
|:---|---|
```search.py```|	Where all of your search algorithms will reside.
```searchAgents.py```|	Where all of your search-based agents will reside.
**Files you might want to look at:**
```pacman.py```|	The main file that runs Pacman games. This file describes a Pacman GameState type, which you use in this project.
```game.py```|	The logic behind how the Pacman world works. This file describes several supporting types like AgentState, Agent, Direction, and Grid.
```util.py```|	Useful data structures for implementing search algorithms.
**Supporting files you can ignore:**
```graphicsDisplay.py```|	Graphics for Pacman
```graphicsUtils.py```|	Support for Pacman graphics
```textDisplay.py```|	ASCII graphics for Pacman
```ghostAgents.py```|	Agents to control ghosts
```keyboardAgents.py```|	Keyboard interfaces to control Pacman
```layout.py```|	Code for reading layout files and storing their contents
```autograder.py```|	Project autograder
```testParser.py```	|Parses autograder test and solution files
```testClasses.py```|	General autograding test classes
```test_cases/```	|Directory containing the test cases for each question
```searchTestClasses.py```|	Project 1 specific autograding test classes
