# Turing Machine Simulator
This project simulates the operation of a Turing Machine in Python.

# Input
Input can be either supplied in the program terminal or via a file name supplied
on the command line. It's format:

### Transitions
The format of the transitions to be input into your Turing machine emulator will be as follows:
```
t current_state input_symbol next_state write_symbol head_movement_direction
```
So for example, the transition above would be written as follows:
```
t 0 0 1 1 R
```

### Final/accept states
The start state is numbered 0. Final (accept) states are indicated using a line formatted as follows:
```
f final_state_1 final_state_2 ... final_state_n
```
So for example, if states 4 and 7 of were accept states of this particular Turing machine, you would write:
```
f 4 7
```
### Input tape
Input to the Turing machine (i.e., the initial tape contents) is a line beginning with ‘i’ followed by a string of symbols. You can assume that an infinite sequence of blank symbols (i.e., ␣) extend in both directions. For example, the following input:
```
i 1 0 1 0 1
```
would be used to specify the contents of the tape.

### Output
Once your computation is complete (an accept or reject state was encountered), output the final contents and the accept/reject status. For example:
```
10101
ACCEPT
```

The supplied file must end with a blank line to exit the program.