Hello there

The report detailing the methods and analysis of the Sokoban solver agent can be found in the pdf report. 

path_visualiser.py
This file takes an input file as a map (such as a text file from testcases), and an output file given list of moves to solve the game (Output file from solver.py). It will give a visual representation of the player following the output solution

sokoban_map.py 
Takes an input file as a map and allows the game to be visualised and played using the arrow keys.

tester.py
Takes an input file as a map and an output file as a solution of moves and determines whether the solution is correct.

solver.py
Given an input file as a map, and an output file, it will write the solution to solve the map to the output file, and if the output file does not exist it will create it. It uses an A* search algorithm with deadlock detection to find the optimal solution to a game of sokoban.


e.g 
To create a solution file:
solver.py testcases/1box_m1.txt output.txt

Display solution file:
path_visualiser.py testcases/1box_m1.txt output.txt

Example output of path_visualiser.py:

![](old_versions/gif.gif)
