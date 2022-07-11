# DFA Graphic Visualization Tool

Visualize DFA's by imputing their code in a .dfa file and compiling it using this program.

[DFA Graphic Visualization Tool](#dfa-graphic-visualization-tool) \
    [DFA format](#dfa-format) \
    [Restrictions](#restrictions)

## DFA format

First line: "--" Followed by a short description of your DFA. \
Second line: The start state. \
Following lines: The DFA instructions, being of the format: \
<CURRENT_STATE> \<CHARACTER\> <NEXT_STATE> \
Last line: The accepts states, separated by spaces.

_Example_:

```
--Even Binary Number Tester
init
init 0 even
init 1 odd
even 0 even
even 1 odd
odd 0 even
odd 1 even
even
```

## Restrictions

The name of the states to be at most 6 characters. \
Each member of the alphabet to be at most 3 characters (Mostly applies when having 7+ states)  \
The number of states to be at most 14.
