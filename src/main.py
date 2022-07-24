#!/usr/bin/python

# DRIVER FILE

from src.misc import exit_if, \
                     FLAGS, \
                     ARG_USAGE, INVALID_FLAG

from sys import argv

from PyQt6.QtWidgets import QApplication

from automata_graphics import GraphicInterface


def main():
    exit_if(len(argv) < 2, ARG_USAGE)
    path = argv[1]

    app = QApplication([])
    gi = GraphicInterface(path)
    app.exec()


if __name__ == '__main__':
    main()
