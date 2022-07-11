#!/usr/bin/python

# DRIVER FILE

from src.misc import exit_if, \
                 ARG_USAGE

from sys import argv

from PyQt6.QtWidgets import QApplication

from dfa_graphics import GraphicInterface


def main():
    exit_if(len(argv) < 2, ARG_USAGE)
    path = argv[1]

    app = QApplication([])
    gi = GraphicInterface(path)
    app.exec()


if __name__ == '__main__':
    main()
