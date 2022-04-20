#
# Automata Final Project
# NFA to DFA
#
# Initial Comment TBC
#

# imports
from graphviz import Digraph
from pprint import pprint, pformat
from tkinter import *
import io

# global variables to be read from GUI (states, initial state, alphabet, final state, transition function)
statesString = ''
startStateString = ''
alphabetString = ''
finalStatesString = ''
deltaString = ''

# global variable to hold the final output to be displayed in GUI
globalOutput = ''

################

# def print_to_string(*args, **kwargs) -> str:
#    output = io.StringIO()
#    print(*args, file=output, **kwargs)
#    contents = output.getvalue()
#    output.close()
#    return contents

################

# ----- HARDCODED INPUT # 1 ------

# Q = [ 'A', 'B', 'C']

# q0 = 'A'

# alphabet = ['0', '1']

# delta = [
#     ['A', '0', 'A'],
#     ['A', '1', 'A'],
#     ['A', '0', 'B'],
#     ['B', '1', 'C']
# ]

# F = ['C']

################

# ----- HARDCODED INPUT # 2 ------

# Q = ['A', 'B', 'C', 'D']

# q0 = 'A'

# alphabet = ['0', '1']

# delta = [
#    ['A', '0', 'A'],
#    ['A', '1', 'B'],
#    ['A', '1', 'A'],
#    ['B', '0', 'C'],
#    ['B', '1', 'C'],
#    ['C', '0', 'D'],
#    ['C', '1', 'D'],
#]

# F = ['D']

################

# preprocessing of input
delta_dict = {}  # used as the transition table for NFA; when given [State][Symbol] produces the next state

# fill the dictionary with states and symbols only
for state in Q: # loop over all states
    delta_dict[state] = {} # initialize the transition row for the state currently looping on
    for symbol in alphabet: # loop over all symbols in the alphabet
        delta_dict[state][symbol] = [] # initialize state-symbol pairs

# fill the dictionary with the transitioning states
for transition in delta:  # loop over the transition function
    x, s, y = transition # extract the state in x, the symbol in s, and the next state in y
    delta_dict[x][s].append(y) # fill the dictionary of state x symbol s with the transitioned state y

# print NFA
pprint(delta_dict)
print()

# final graph format settings, to be displayed seperate of the GUI
dot = Digraph()
dot.graph_attr['rankdir'] = 'LR'
dot.node_attr['shape'] = 'circle'


################

# ----- HARDCODED INPUT # 1 ------


# Q = [ 'A', 'B', 'C']

# q0 = 'A'

# alphabet = ['0', '1']

# delta = [
#     ['A', '0', 'A'],
#     ['A', '1', 'A'],
#     ['A', '0', 'B'],
#     ['B', '1', 'C']
# ]

# A,0,A|A,1,A|A,0,B|B,1,C

# F = ['C']

################


# 
def convert_nfa_to_dfa():
    global statesString, startStateString, deltaString, alphabetString, finalStatesString, Q, q0, alphabet, delta, F, \
        globalOutput, var

    statesString = setOfStatesInput.get()
    startStateString = startStateInput.get()
    alphabetString = alphabetInput.get()
    finalStatesString = finalStatesInput.get()
    deltaString = deltaInput.get()

    Q = statesString.split(',')
    q0 = startStateString
    alphabet = alphabetString.split(',')
    F = finalStatesString.split(',')
    delta = [list(line.split(',')) for line in deltaString.split('|')]
    # Algorithm NFA to DFA
    dfa_states = [[q0]]
    dfa_delta = []
    new_dfa_states = [[q0]]

    #                    new_dfa_states |    Symbol1 (0)   |    Symbol2 (1)   |  ...etc
    #                  -------------------------------------------------------------------
    #   current_state ->       q0       |         x        |         y        |
    #                                   |                  |                  |
    #                                   |                  |                  |
    #                                   |                  |                  |
    #
    #  x & y determined by the pre-defined dictionary as following
    #      delta_dict[current_state][symbol]   -> current_state could be more than one state like {A,B} so it's iterated
    #      upon all its elements

    while len(new_dfa_states) > 0:
        current_state = new_dfa_states[0]  #
        new_dfa_states = new_dfa_states[1:]

        # globalOutput += print_to_string('Current state: ', current_state)
        globalOutput += 'Current state: ' + '{' + ', '.join(f'{w}' for w in current_state) + '}' + '\n'

        for symbol in alphabet:
            next_states = []
            for nfa_state in current_state:
                for x in delta_dict[nfa_state][symbol]:
                    if x not in next_states:
                        next_states.append(x)
            next_states = sorted(next_states)
            dfa_delta.append([current_state, symbol, next_states])
            # globalOutput += print_to_string('Symbol: ', symbol, ' States: ', next_states)
            globalOutput += 'When input = ' + ', '.join(f'{w}' for w in symbol) + ', Go to : {' + ', '.join(
                f'{w}' for w in next_states) + '}\n'

            if next_states not in dfa_states:
                dfa_states.append(next_states)
                new_dfa_states.append(next_states)
        globalOutput += '\n'

    globalOutput += 'DFA Q = { '
    globalOutput += ', '.join(f'{w}' for w in dfa_states)
    globalOutput += ' }\n\n'
    # globalOutput += print_to_string('\n')
    output2 = []
    for temp in dfa_delta:
        for elem in temp:
            output2.append(elem)

    globalOutput += 'DFA Delta = \n'
    globalOutput += pformat(dfa_delta)

    # print('dfa_delta')
    # globalOutput += 'DFA Delta = \n'
    # globalOutput += ', '.join(f'{w}' for w in ('[' + str(item) + ']' for innerlist in output2 for item in innerlist))

    print(globalOutput)

    # construct graph by dot (Graphviz)
    def stringify(state: list):
        return '{' + ','.join(state) + '}'

    for state in dfa_states:
        name = stringify(state)
        dot.node(name, name)

    for transition in dfa_delta:
        x, s, y = transition
        nameX = stringify(x)
        nameY = stringify(y)
        dot.edge(nameX, nameY, label=s)

    dot.node('BEGIN', '', shape='none')
    dot.edge('BEGIN', stringify([q0]), label='start')

    for dfa_state in dfa_states:
        for final_state in F:
            if final_state in dfa_state:
                name = stringify(dfa_state)
                dot.node(name, name, shape='doublecircle')

    var.set(globalOutput)
    # dot.render(filename='gv_dfa.gv', view=True)


# GUI
root = Tk()
root.geometry(str(1000) + "x" + str(400))
root.title("NFA to DFA - ASU Final Automata Course Project")

Label(root, text="Enter NFA to covert", font=("Montserrat", 18), fg='#000000').grid(column=1, row=1, padx=2, sticky="w")

Label(root, text="States", font=("Montserrat", 12), fg='#666666').grid(column=1, row=2, padx=2, sticky="w")
setOfStatesInput = Entry(root, width=15, justify="left", bg='#f0f0f0')
setOfStatesInput.grid(column=2, row=2, padx=2, sticky="w")

Label(root, text="Start State", font=("Montserrat", 12), fg='#666666').grid(column=1, row=4, padx=2, sticky="w")
startStateInput = Entry(root, width=5, justify="left", bg='#f0f0f0')
startStateInput.grid(column=2, row=4, padx=2, sticky="w")

Label(root, text="Final State", font=("Montserrat", 12), fg='#666666').grid(column=1, row=6, padx=2, sticky="w")
finalStatesInput = Entry(root, width=5, justify="left", bg='#f0f0f0')
finalStatesInput.grid(column=2, row=6, padx=2, sticky="w")

Label(root, text="Alphabet", font=("Montserrat", 12), fg='#666666').grid(column=1, row=8, padx=2, sticky="w")
alphabetInput = Entry(root, width=5, justify="left", bg='#f0f0f0')
alphabetInput.grid(column=2, row=8, padx=2, sticky="w")

Label(root, text="Delta", font=("Montserrat", 12), fg='#666666').grid(column=1, row=10, padx=2, sticky="w")
deltaInput = Entry(root, width=15, justify="left", bg='#f0f0f0')
deltaInput.grid(column=2, row=10, padx=2, sticky="w")

convertBtn = Button(root, text="Convert", width=30, height=2, font=("Montserrat", 10),
                    command=lambda: convert_nfa_to_dfa())
convertBtn.grid(column=1, row=12, columnspan=3, sticky="w", padx=10, pady=10)

# divider1 = Label(root, text="")
var = StringVar()
var.set('-\n-\n-\n-\n-\n-\n-\n-\n-\n-\n-\n-\n-\n-\n-\n-\n-\n-\n-\n-\n-\n-\n-\n-\n-\n-\n-\n-\n-\n-\n-\n-\n-\n-\n')
Label(root,
      textvariable=var,
      font=("Montserrat", 8),
      bg="#f0f0f0",
      fg='#666666',
      width=100,
      anchor="w",
      justify=LEFT).grid(column=5,
                         row=1,
                         padx=25,
                         rowspan=75,
                         sticky="w",
                         )

root.mainloop()
