# CONSTANTS, MESSAGES, AND HELPERS

# Coordinates
START_X = 100
START_Y = 160

MAX_X = 1170


# Circles
SIZE_CIRCLE = 80
HALF_SIZE_CIRCLE = int(SIZE_CIRCLE / 2)
SIZE_DIFFERENCE = 10
SIZE_INNER = SIZE_CIRCLE - 10

# States
LINE_DIST_MULT = 5

STATE_ADJUST = 12
START_ADJUST_Y = 15
START_ADJUST_X = 13
START_TEXT = "<START>"
STATE_TEXT_ADJUST = 5
STATE_LOWER_MULTIPLIER = 2.6

ROW_ADJUST = 11
ROW_TEXT_ADJUST = 8

# Arcs
SELF_DIFF_X = 24
SELF_DIFF_Y = 70
SELF_Y_ADJUST = 5
SELF_MIDDLE_ADJUST = 10

SELF_ARROW_ADJUST_X = 12
SELF_ARROW_ADJUST_Y = 10
SELF_ARROW_ADJUST_X_RIGHT = 5
SELF_ARROW_ADJUST_Y_RIGHT = 5

SELF_CHARACTER_ADJUST = 3


STATES_TEXT_ADJUST_Y = 9
STATES_ARROW_ADJUST_X = 10
STATES_ARROW_ADJUST_Y = 6
STATES_ARROW_TIME = 2 / 3
STATES_TEXT_TIME = 1 / 2

DIFFERENT_STATES_DIST = 5

# Arrows
STATE_DIFFERENT_LENGTH = 8

# Helpers
def exit_if(condition, msg):
    if condition:
        print(msg)
        exit(2)


def TODO(title):
    print(f"[TODO]: {title}")


# Usage
ARG_USAGE = "[USAGE]: dfa path/to/dfa/file."

# Error
MAX_STATES = 14

INVALID_DFA = "[ERROR]: dfa has no initial state or no final state."
INVALID_DESCRIPTION = "[ERROR]: your .dfa file needs to contain a description as the first line\n\t\t\
 that starts with \"--\""
STATES_EXCEEDED = f"[ERROR]: Can't load more than {MAX_STATES} states."
NEGATIVE_DISCRIMINANT = "[ERROR]: Negative discriminant."