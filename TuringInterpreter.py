#! /usr/bin/env python3
import sys
import fileinput


# Accept/Reject halts
class Decision(Exception):
    pass


class Accept (Decision):
    def __init__(self):
        super().__init__("ACCEPT")


class Reject (Decision):
    def __init__(self):
        super().__init__("REJECT")


class Tape:
    _empty_val = '_'

    def __init__(self):
        """Initialize an empty tape and initial position"""
        self._tape = [self._empty_val]
        self._position = 0
        self._first_write = True

    def get_empty_val(self):
        """Returns this tape's 'empty' value."""
        return self._empty_val

    def append(self, value):
        """Add an object to the end of the tape.

        :param value: The value to append to tape.
        :return: None
        """
        # Remove placeholder
        if self._first_write:
            self._first_write = False
            self._tape.pop()

        self._tape.append(value)

    def prepend(self, value):
        """Add an object to the beginning of the tape.

        :param value: The value to prepend to tape.
        :return: None
        """
        # Remove placeholder
        if self._first_write:
            self._first_write = False
            self._tape.pop()

        self._tape.insert(0, value)
        self._position += 1     # The list extended, so move position

    def move_left(self):
        """Move the head left, extend tape if needed"""
        if self._position == 0:
            self.prepend(self._empty_val)

        self._position -= 1

    def move_right(self):
        """Move the head right, extend tape if needed"""
        if self._position + 1 >= len(self._tape):
            self._tape.append(self._empty_val)

        self._position += 1

    def read(self):
        """Read the current contents of the tape.

        :return: The tape contents at that position
        """
        return self._tape[self._position]

    def write(self, value):
        """Write value to current location in tape.

        :param value:  The value to write.
        """
        self._tape[self._position] = value

    def __str__(self, *args, **kwargs):
        return ''.join(self._tape)


class State:
    """Turing Machine state, contains accept/reject status, and transitions."""

    def __init__(self, states, tape):
        """Initializes a state as a reject with no transitions.

        :param states: The object that contains the states (updated externally)
        """
        self.states = states
        self.accepts = False
        self._transitions = []
        self.tape = tape
        pass

    def add_transition(self, input_symbol, next_state, write_symbol, movement_direction):
        """Add a transition to the State to another state

        :param input_symbol:        An input symbol
        :param next_state:          State object key: the state to transition to
        :param write_symbol:        The symbol to write to the tape
        :param movement_direction:  The direction to move the head
        :return:
        """
        self._transitions.append((input_symbol, next_state, write_symbol, movement_direction))

    def process_transition(self):
        """Handles reading to the tape and moving to the next transition.

        This function throws Accept if the machine has ended on an accept state, or reject
             if the machine has ended OR is requesting a transition that does not exist.
        """
        tape_text = self.tape.read()

        for transition in self._transitions:
            try:
                if tape_text == transition[0]:
                    # Execute tape modification and movement
                    self.tape.write(transition[2])
                    if transition[3].upper() == 'R':
                        self.tape.move_right()
                    else:
                        self.tape.move_left()

                    # Process new state
                    self.states[transition[1]].process_transition()
            except Reject:
                # Mask rejections, as one of the transitions could accept still
                pass

        # If no transition was found, decide if must accept or reject
        if self.accepts:
            raise Accept()
        else:
            raise Reject()


def main(argc: int, argv: list):
    tape = Tape()               # Contains the input tape
    states = {}                 # Stores all the states
    states[0] = State(states, tape)   # Create initial state

    # Go through all input lines
    for line in fileinput.input():
        # If empty line, break
        line = line.strip('\n').strip('\r')
        if not len(line):
            break

        # Split a line into its individual pieces
        line = line.split(' ')

        # If line is a state
        if line[0] == 't':
            state_num = int(line[1])
            # Create state if not exist
            if state_num not in states.keys():
                states[state_num] = State(states, tape)

            # Add transition
            states[state_num].add_transition(line[2], int(line[3]), line[4], line[5])

            # Create destination state if not exists
            if int(line[3]) not in states.keys():
                states[int(line[3])] = State(states, tape)

        # If line specifies accept states
        elif line[0] == 'f':
            parts = line[1:]

            # Mark all accepting states
            for part in parts:
                states[int(part)].accepts = True

        # Tape contents
        elif line[0] == 'i':
            text = line[1]
            # Populate tape
            for character in text:
                tape.append(character)

            # Run machine
            try:
                states[0].process_transition()
            except Decision as err:
                print(tape)
                print(err)
            finally:
                # Restore initial state
                tape = Tape()                       # Contains the input tape
                states = {}                         # Stores all the states
                states[0] = State(states, tape)     # Create initial state


if __name__ == "__main__":
    main(len(sys.argv), sys.argv)
