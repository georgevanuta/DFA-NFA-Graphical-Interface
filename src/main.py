#!/usr/bin/python

# DRIVER FILE

from src.misc import exit_if, \
                     FLAGS, \
                     ARG_USAGE, INVALID_FLAG

from sys import argv

from PyQt6.QtWidgets import QApplication

from dfa_graphics import GraphicInterface


def main():
    exit_if(len(argv) < 2, ARG_USAGE)
    path = argv[1]

    dark = False
    flags = argv[2:]
    for flag in flags:
        exit_if(not FLAGS.__contains__(flag), INVALID_FLAG(flag))

        if flag == '-d' or flag == '--dark':
            dark = True

    app = QApplication([])
    gi = GraphicInterface(path, dark)
    app.exec()


if __name__ == '__main__':
    main()
