from misc import DETERMINISTIC, NONDETERMINISTIC

# DFA

from src.misc import exit_if, \
                 DETERMINISTIC, \
                 SYMBOLS, \
                 SPACES, \
                 INVALID_DESCRIPTION, INVALID_DETERMINISTIC, INVALID_SPACE


class FiniteAutomata:
    type = 0
    description = ""
    alphabet = set()
    initial = ""
    finals = set()
    delta = dict({})            # <- for testing if the dfa accepts a string
    interface_delta = dict({})  # <- for displaying the dfa
    states = set()

    def __init__(self, string, type):
        self.type = type
        lines = string.split('\n')
        descr_line = 0

        self.nameless = False
        self.accept = True
        self.dark = False

        # check for tags/spaces
        if lines[0][0] == '[':
            descr_line += 1
            tags = lines[0][1:len(lines[0]) - 1].split(', ')
            for tag in tags:
                exit_if(not SPACES.__contains__(tag), INVALID_SPACE(tag))
                if tag == 'NAMELESS':
                    self.nameless = True
                elif tag == 'NO_ACCEPT':
                    self.accept = False
                elif tag == 'DARK_MODE':
                    self.dark = True

        self.description = lines[descr_line]
        exit_if(self.description[0:2] != "--", INVALID_DESCRIPTION)

        self.description = self.description[2:]

        # search first non-empty / non-comment lines for start state
        start_index = descr_line + 1

        for i in range(1,len(lines)):
            if len(lines[i]) == 0 or lines[i][0:2] == '--':
                continue

            start_index = i + 1
            self.initial = lines[i]
            break

        # search last non-empty / non-comment lines for accepts states
        end_index = len(lines)

        if self.accept:
            for i in range(1, len(lines)):
                if len(lines[-i]) == 0 or lines[-1][0:2] == '--':
                    continue

                end_index = len(lines) - i
                self.finals = lines[-i].split(' ')
                break

        for final in self.finals:
            self.states.add(final)

        self.states.add(self.initial)

        for i in range(start_index, end_index):
            if len(lines[i]) == 0 or lines[i][0:2] == '--':
                continue

            spl = lines[i].split(' ')

            current_state = spl[0]
            characters = spl[1].split(',')
            next_state = spl[2]

            interface_characters = ''

            for character in characters:
                if SYMBOLS.keys().__contains__(character):
                    exit_if(self.type == DETERMINISTIC and character == '\eps', INVALID_DETERMINISTIC)
                    interface_characters = interface_characters + ',' + SYMBOLS[character]
                else:
                    interface_characters = interface_characters + ',' + character

            interface_characters = interface_characters[1:] # delete first comma

            if (current_state, interface_characters) not in self.interface_delta:
                self.interface_delta[current_state, interface_characters] = list()

            self.interface_delta[(current_state, interface_characters)].append(next_state)

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
