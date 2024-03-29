# DFA / NFA Graphical Visualization Tool

Visualize FA's by imputing their code in a .dfa / .nfa file and compiling it using this program.


[DFA / NFA Graphic Visualization Tool](#dfa-/-nfa-graphic-visualization-tool)
  - [Example](#example)
  - [DFA format](#dfa-format)
  - [Restrictions](#restrictions)
  - [Notes](#notes)
  - [What's in plan?](#whats-in-plan)

## Example
<img src="https://user-images.githubusercontent.com/74255152/178478526-d4817b2f-5986-41d2-ab37-e21e28027c71.png">

## FA format

*First line:* "--" Followed by a short description of your DFA. \
*Second line:* The start state. \
*Following lines:* The FA instructions, being of the format: \
<CURRENT_STATE> \[<CHARACTERS\>] <NEXT_STATE> \
*Last line:* The accepts states, separated by spaces.

_Example of dfa code_:

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

- The name of the states to be at most 6 characters.
- Each member of the alphabet to be at most 3 characters (Mostly applies when having 7+ states).
- The number of states to be at most 14.

## Notes

You can play around with different FA's locatated in the **tests** folder and see how they are going to be rendered.

## What's in plan?

 - [ ] an animation showing the different states the DFA goes through processing a string. 
 - [x] add dark mode.
 - [ ] increase the limit of states by making the window slidable.
 - [x] add support for NFA's.

