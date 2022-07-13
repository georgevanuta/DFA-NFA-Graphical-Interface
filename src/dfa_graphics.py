# GRAPHICAL INTERFACE

from src.misc import START_X, START_Y, MAX_X, \
                 SIZE_CIRCLE, HALF_SIZE_CIRCLE, SIZE_INNER, SIZE_DIFFERENCE, LINE_DIST_MULT, \
                 SELF_DIFF_X, SELF_DIFF_Y, SELF_Y_ADJUST, SELF_MIDDLE_ADJUST, \
                 STATE_ADJUST, START_ADJUST_Y, START_ADJUST_X, START_TEXT, \
                 SELF_ARROW_ADJUST_X, SELF_ARROW_ADJUST_Y, SELF_ARROW_ADJUST_X_RIGHT, SELF_ARROW_ADJUST_Y_RIGHT, \
                 SELF_CHARACTER_ADJUST,\
                 STATE_TEXT_ADJUST, STATES_ARROW_ADJUST_X, STATES_ARROW_ADJUST_Y, STATES_ARROW_TIME, STATES_TEXT_TIME, \
                 STATE_LOWER_MULTIPLIER, \
                 ROW_ADJUST, ROW_TEXT_ADJUST, \
                 STATE_DIFFERENT_LENGTH, \
                 LIGHT_MODE, DARK_MODE, \
                 INVALID_DFA, MAX_STATES, STATES_EXCEEDED, \
                 exit_if

from dfa import DFA, is_dfa_invalid

from bezier import point_on_bezier

from src.geometry import get_ctrl_points

from math import sqrt

from PyQt6.QtWidgets import QWidget
from PyQt6.QtGui import QPainter, QPainterPath, QFont
from PyQt6.QtCore import Qt


class GraphicInterface(QWidget):
    def __init__(self, path, dark):
        super().__init__()
        self.state_pos = None

        if dark:
            self.theme = DARK_MODE
        else:
            self.theme = LIGHT_MODE

        with open(path, 'r') as f:
            self.dfa = DFA(f.read())
            exit_if(is_dfa_invalid(self.dfa), INVALID_DFA)
            exit_if(len(self.dfa.states) > MAX_STATES, STATES_EXCEEDED)
            self.initUI()

    def initUI(self):
        if self.theme == DARK_MODE:
            self.setStyleSheet("background-color: black;")
        else:
            self.setStyleSheet("background-color: white;")
        self.setMinimumSize(100, 100)
        self.setGeometry(500, 100, 600, 600)
        self.setWindowTitle(f'Deterministic Finite Automata: {self.dfa.description}')
        self.showMaximized()

    def paintEvent(self, e):
        qp = QPainter()
        qp.begin(self)
        self.draw_states(qp)
        qp.end()

    def draw_states(self, qp):
        if self.theme == DARK_MODE:
            qp.setPen(Qt.GlobalColor.white)
        else:
            qp.setPen(Qt.GlobalColor.black)

        qp.setFont(QFont('Arial', 10))

        x = START_X
        y = START_Y

        self.state_pos = dict({})

        # draw states
        for state in self.dfa.states:
            if x > MAX_X:
                x = START_X
                # start drawing on next line
                y += int(LINE_DIST_MULT * SIZE_CIRCLE)

            self.state_pos[state] = (x, y)
            self.draw_state(qp, int(x), int(y),
                            self.dfa.finals.__contains__(state), self.dfa.initial == state)
            qp.drawText(x + HALF_SIZE_CIRCLE - STATE_ADJUST, y + HALF_SIZE_CIRCLE, state)
            x += int(2.2 * SIZE_CIRCLE)

        # draw arrows
        for (src_state, character), dest_state in self.dfa.interface_delta.items():
            self.draw_arrow(qp, src_state, character, dest_state)

    def draw_state(self, qp, x, y, is_final, is_start):
        qp.drawEllipse(x, y, SIZE_CIRCLE, SIZE_CIRCLE)

        if is_final:  # draw an inner circle
            qp.drawEllipse(x + int(SIZE_DIFFERENCE / 2), y + int(SIZE_DIFFERENCE / 2), SIZE_INNER, SIZE_INNER)
        if is_start:  # write that the respective state is the start of computation
            qp.drawText(x + HALF_SIZE_CIRCLE - STATE_ADJUST - START_ADJUST_X,
                        y + HALF_SIZE_CIRCLE + START_ADJUST_Y,
                        START_TEXT)

    def draw_arrow(self, qp, src_state, character, dest_state):
        if src_state == dest_state:
            self.draw_self_arrow(qp, src_state, character)
        else:
            self.draw_states_arrow(qp, src_state, character, dest_state)

    def draw_self_arrow(self, qp, state, character):
        # get the state positions
        pos_x = self.state_pos[state][0] + HALF_SIZE_CIRCLE
        pos_y = self.state_pos[state][1] + SELF_Y_ADJUST

        # draw the self arc
        path = QPainterPath()
        path.moveTo(pos_x - SELF_DIFF_X, pos_y)
        path.cubicTo(pos_x - SELF_DIFF_X, pos_y,
                     pos_x + int(SELF_DIFF_X / 2) - SELF_MIDDLE_ADJUST, pos_y - SELF_DIFF_Y,
                     pos_x + SELF_DIFF_X, pos_y)
        qp.drawPath(path)

        # complete the arrow
        qp.drawLine(pos_x + SELF_DIFF_X, pos_y,
                    pos_x + SELF_DIFF_X - SELF_ARROW_ADJUST_X, pos_y - SELF_ARROW_ADJUST_Y)

        qp.drawLine(pos_x + SELF_DIFF_X, pos_y,
                    pos_x + SELF_DIFF_X + SELF_ARROW_ADJUST_X - SELF_ARROW_ADJUST_X_RIGHT,
                    pos_y - SELF_ARROW_ADJUST_Y - SELF_ARROW_ADJUST_Y_RIGHT)

        # draw the read character
        qp.drawText(pos_x - SELF_CHARACTER_ADJUST, pos_y - int(SELF_DIFF_Y / 2), character)

    def draw_states_arrow(self, qp, src_state, character, dest_state):
        (src_x, src_y) = self.state_pos[src_state]
        (dest_x, dest_y) = self.state_pos[dest_state]

        if src_y == dest_y:  # same line

            if src_x > dest_x:
                curvature = -1  # upper arrow
            else:
                curvature = 1   # lower arrow

            y = src_y

            if curvature == -1:
                y += SIZE_CIRCLE

            x_start = src_x + HALF_SIZE_CIRCLE
            x_end = dest_x + HALF_SIZE_CIRCLE

            dist = abs(int(x_start - x_end))

            ctrl_p_x = abs(int((x_start + x_end)) / 2)
            ctrl_p_y = y - curvature * int(dist / 5)

            # draw arc
            path = QPainterPath()
            path.moveTo(x_start, y)
            path.cubicTo(ctrl_p_x - curvature * int(dist / 2.5), ctrl_p_y,
                         ctrl_p_x + curvature * int(dist / 2.5), ctrl_p_y,
                         x_end, y)
            qp.drawPath(path)

            multiplier = 1
            if curvature == -1:
                multiplier = STATE_LOWER_MULTIPLIER

            # draw the read character
            x_half, y_half = point_on_bezier(x_start, y,
                                             ctrl_p_x - curvature * int(dist / 2.5), ctrl_p_y,
                                             ctrl_p_x + curvature * int(dist / 2.5), ctrl_p_y,
                                             x_end, y, STATES_TEXT_TIME)

            qp.drawText(int(x_half), int(y_half - multiplier * curvature * STATE_TEXT_ADJUST), character)

            # draw arrow head

            x_arr, y_arr = point_on_bezier(x_start, y,
                                           ctrl_p_x - curvature * int(dist / 2.5), ctrl_p_y,
                                           ctrl_p_x + curvature * int(dist / 2.5), ctrl_p_y,
                                           x_end, y, STATES_ARROW_TIME)

            x_arr, y_arr = int(x_arr), int(y_arr)

            qp.drawLine(x_arr, y_arr, x_arr - curvature * STATES_ARROW_ADJUST_X, y_arr + STATES_ARROW_ADJUST_Y)
            qp.drawLine(x_arr, y_arr, x_arr - curvature * STATES_ARROW_ADJUST_X, y_arr - STATES_ARROW_ADJUST_Y)

        elif src_x == dest_x:   # same row
            if src_y > dest_y:
                curvature = -1
            else:
                curvature = 1

            if curvature == -1:
                x = src_x
            else:
                x = src_x + SIZE_CIRCLE

            start_y = src_y + HALF_SIZE_CIRCLE
            end_y = dest_y + HALF_SIZE_CIRCLE

            dist = int(abs(start_y - end_y))

            ctrl_p_x = x + curvature * int(dist / ROW_ADJUST)
            ctrl_p_y = int(abs((start_y + end_y) / 2))

            # draw arc
            path = QPainterPath()
            path.moveTo(x, start_y)
            path.cubicTo(ctrl_p_x, ctrl_p_y - curvature * int(dist / ROW_ADJUST),
                         ctrl_p_x, ctrl_p_y + curvature * int(dist / ROW_ADJUST),
                         x, end_y)
            qp.drawPath(path)

            # draw text
            multiplier = 1
            if curvature == -1:
                multiplier = 2

            half_x, half_y = point_on_bezier(x, start_y,
                                             ctrl_p_x, ctrl_p_y - curvature * int(dist / ROW_ADJUST),
                                             ctrl_p_x, ctrl_p_y + curvature * int(dist / ROW_ADJUST),
                                             x, end_y, STATES_TEXT_TIME)

            qp.drawText(int(half_x + multiplier * curvature * ROW_TEXT_ADJUST), int(half_y), character)

            # draw arrow
            x_arr, y_arr = point_on_bezier(x, start_y,
                                           ctrl_p_x, ctrl_p_y - curvature * int(dist / ROW_ADJUST),
                                           ctrl_p_x, ctrl_p_y + curvature * int(dist / ROW_ADJUST),
                                           x, end_y, STATES_ARROW_TIME)

            x_arr, y_arr = int(x_arr), int(y_arr)

            qp.drawLine(x_arr, y_arr, x_arr + STATES_ARROW_ADJUST_Y, y_arr - curvature * STATES_ARROW_ADJUST_X)
            qp.drawLine(x_arr, y_arr, x_arr - STATES_ARROW_ADJUST_Y, y_arr - curvature * STATES_ARROW_ADJUST_X)

        else:    # different line and different row
            if src_y < dest_y:
                curvature = 1

                upper_x, upper_y = src_x + HALF_SIZE_CIRCLE, src_y + SIZE_CIRCLE
                lower_x, lower_y = dest_x + HALF_SIZE_CIRCLE, dest_y
            else:
                curvature = -1

                upper_x, upper_y = dest_x + HALF_SIZE_CIRCLE, dest_y + SIZE_CIRCLE
                lower_x, lower_y = src_x + HALF_SIZE_CIRCLE, src_y

            dist = sqrt(pow(upper_x - lower_x, 2) + pow(upper_y - lower_y, 2)) / 7

            # draw arc
            ctrl_x_1, ctrl_y_1, ctrl_x_2, ctrl_y_2 = get_ctrl_points(upper_x, upper_y,
                                                                     lower_x, lower_y,
                                                                     curvature * dist)

            path = QPainterPath()
            path.moveTo(upper_x, upper_y)
            path.cubicTo(ctrl_x_1, ctrl_y_1,
                         ctrl_x_2, ctrl_y_2,
                         lower_x, lower_y)

            qp.drawPath(path)

            # draw text
            half_x, half_y = point_on_bezier(upper_x, upper_y,
                                             ctrl_x_1, ctrl_y_1,
                                             ctrl_x_2, ctrl_y_2,
                                             lower_x, lower_y,
                                             STATES_TEXT_TIME)

            half_x, half_y = int(half_x), int(half_y)

            if src_x > dest_x:
                curvature_x = 1
            else:
                curvature_x = -1
            if src_y > dest_y:
                curvature_y = -1
            else:
                curvature_y = 1

            # not doing this will lead to overlapping the text with the arc
            if src_y < dest_y and src_x < dest_x:
                curvature_x = -2
                curvature_y = 2

            qp.drawText(half_x + curvature_x * STATE_TEXT_ADJUST,
                        half_y + curvature_y * STATE_TEXT_ADJUST,
                        character)

            # draw arrow
            if curvature == 1:
                arrow_x, arrow_y = point_on_bezier(upper_x, upper_y,
                                                   ctrl_x_1, ctrl_y_1,
                                                   ctrl_x_2, ctrl_y_2,
                                                   lower_x, lower_y,
                                                   STATES_ARROW_TIME)
            else:
                arrow_x, arrow_y = point_on_bezier(lower_x, lower_y,
                                                   ctrl_x_2, ctrl_y_2,
                                                   ctrl_x_1, ctrl_y_1,
                                                   upper_x, upper_y,
                                                   STATES_ARROW_TIME)

            arrow_x, arrow_y = int(arrow_x), int(arrow_y)

            if curvature_x > 0 and curvature_y > 0:
                qp.drawLine(arrow_x, arrow_y,
                            arrow_x + STATE_DIFFERENT_LENGTH, int(arrow_y + STATE_DIFFERENT_LENGTH / 2))
                qp.drawLine(arrow_x, arrow_y,
                            int(arrow_x + STATE_DIFFERENT_LENGTH / 4), arrow_y - STATE_DIFFERENT_LENGTH)
            elif curvature_x > 0 and curvature_y < 0:
                qp.drawLine(arrow_x, arrow_y,
                            arrow_x + STATE_DIFFERENT_LENGTH, int(arrow_y - STATE_DIFFERENT_LENGTH / 2))
                qp.drawLine(arrow_x, arrow_y,
                            int(arrow_x + STATE_DIFFERENT_LENGTH / 4), arrow_y + STATE_DIFFERENT_LENGTH)
            elif curvature_x < 0 and curvature_y > 0:
                qp.drawLine(arrow_x, arrow_y,
                            arrow_x - STATE_DIFFERENT_LENGTH, int(arrow_y + STATE_DIFFERENT_LENGTH / 4))
                qp.drawLine(arrow_x, arrow_y,
                            int(arrow_x + STATE_DIFFERENT_LENGTH / 3), arrow_y - STATE_DIFFERENT_LENGTH)
            else:
                qp.drawLine(arrow_x, arrow_y,
                            arrow_x - STATE_DIFFERENT_LENGTH, int(arrow_y - STATE_DIFFERENT_LENGTH / 6))
                qp.drawLine(arrow_x, arrow_y,
                            int(arrow_x - STATE_DIFFERENT_LENGTH / 6), arrow_y + STATE_DIFFERENT_LENGTH)
