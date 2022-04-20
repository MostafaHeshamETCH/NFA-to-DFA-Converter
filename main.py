#
# Automata Final Project
# NFA to DFA
#
# Initial Comment TBC
#

from graphviz import Digraph
from pprint import pprint
from tkinter import *

# ----- INPUT ------

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

Q = ['A', 'B', 'C', 'D']

q0 = 'A'

alphabet = ['0', '1']

delta = [
    ['A', '0', 'A'],
    ['A', '1', 'B'],
    ['A', '1', 'A'],
    ['B', '0', 'C'],
    ['B', '1', 'C'],
    ['C', '0', 'D'],
    ['C', '1', 'D'],
]

F = ['D']

# preprocessing of input
delta_dict = {}  # used as transition table for NFA where when given [State][Symbol] produces the next State

for state in Q:  # fills the dictionary with States and Symbols only
    delta_dict[state] = {}
    for symbol in alphabet:
        delta_dict[state][symbol] = []

for transition in delta:  # fills each State and Symbol with its transitioned States
    x, s, y = transition
    delta_dict[x][s].append(y)

# Print NFA
pprint(delta_dict)
print()


# Final Graph Format Settings
dot = Digraph()
dot.graph_attr['rankdir'] = 'LR'
dot.node_attr['shape'] = 'circle'


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

    print('Current state: ', current_state)

    for symbol in alphabet:
        next_states = []
        for nfa_state in current_state:
            for x in delta_dict[nfa_state][symbol]:
                if x not in next_states:
                    next_states.append(x)
        next_states = sorted(next_states)
        dfa_delta.append([current_state, symbol, next_states])
        print('Symbol: ', symbol, ' States: ', next_states)

        if next_states not in dfa_states:
            dfa_states.append(next_states)
            new_dfa_states.append(next_states)
    print()

print('dfa_states', dfa_states)
print()

print('dfa_delta')
pprint(dfa_delta)


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

# dot.render(filename='gv_dfa.gv', view=True)

# GUI
root = Tk()
root.geometry(str(1000) + "x" + str(1000))
root.title("NFA to DFA - ASU Final Automata Course Project")

Label(root, text="States", font=("Montserrat", 12), fg='#666666').grid(column=1, row=0, padx=2)
Label(root, text="Start State", font=("Montserrat", 12), fg='#666666').grid(column=2, row=0, padx=2)
Label(root, text="Alphabet", font=("Montserrat", 12), fg='#666666').grid(column=3, row=0, padx=2)

root.mainloop()
