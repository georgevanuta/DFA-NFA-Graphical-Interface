# DFA

from src.misc import exit_if, \
                 INVALID_DESCRIPTION


class DFA:
    description = ""
    alphabet = set()
    initial = ""
    finals = set()
    delta = dict({})            # <- for testing if the dfa accepts a string
    interface_delta = dict({})  # <- for displaying the dfa
    states = set()

    def __init__(self, string):
        lines = string.split('\n')
        self.description = lines[0]
        exit_if(self.description[0:2] != "--", INVALID_DESCRIPTION)

        self.description = self.description[2:]

        self.initial = lines[1]
        self.finals = lines[-1].split(' ')

        for final in self.finals:
            self.states.add(final)

        self.states.add(self.initial)

        for i in range(2, len(lines) - 1):
            spl = lines[i].split(' ')

            current_state = spl[0]
            characters = spl[1].split(',')
            interface_characters = spl[1]
            next_state = spl[2]

            self.interface_delta[(current_state, interface_characters)] = next_state

            for character in characters:
                self.delta[(current_state, character)] = next_state
                self.states.add(current_state)
                self.states.add(next_state)
                self.alphabet.add(character)

    def __str__(self):
        return f'alphabet:\t{self.alphabet}\n\
delta:\t{self.delta}\n\
initial state:\t{self.initial}\n\
final states:\t{self.finals}\n'

    def next_configuration(self, configuration):
        current_state, word = configuration

        if len(word) == 0:
            return configuration

        character = word[0]
        rest_of_word = word[1:]
        next_state = self.delta[(current_state, character)]

        return next_state, rest_of_word

    def accepts(self, word):
        current_configuration = (self.initial, word)
        current_state = self.initial

        for i in range(0, len(word)):
            current_configuration = self.next_configuration(current_configuration)
            current_state = current_configuration[0]

        return self.finals.__contains__(current_state)


def is_dfa_invalid(dfa):
    return dfa.initial == "" or len(dfa.finals) == 0
