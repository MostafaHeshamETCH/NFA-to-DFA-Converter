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

# ----- HARDCODED INPUT # 1 ------

allStates = ['A', 'B', 'C', 'D']

qNode = 'A'

inputSymbols = ['0', '1']

transitionTable = [
   ['A', '0', 'A'],
   ['A', '1', 'B'],
   ['A', '1', 'A'],
   ['B', '0', 'C'],
   ['B', '1', 'C'],
   ['C', '0', 'D'],
   ['C', '1', 'D'],
]

qFinal = ['D']

################

# ----- HARDCODED INPUT # 2 ------

# allStates = [ 'A', 'B', 'C' ]
#
# qNode = 'A'
#
# inputSymbols = ['0', '1']
#
# transitionTable = [
#     ['A', '0', 'A'],
#     ['A', '1', 'A'],
#     ['A', '0', 'B'],
#     ['B', '1', 'C']
# ]

# A,0,A|A,1,A|A,0,B|B,1,C

# qFinal = ['C']

################

# preprocessing of input
dfaTransitionTable = {}  # used as the transition table for NFA; when given [State][Symbol] produces the next state

# print NFA
pprint(dfaTransitionTable)
print()

################

# function to convert an NFA to a DFA
def convert_nfa_to_dfa():
    # previously defined variables
    global statesString, startStateString, deltaString, alphabetString, finalStatesString, allStates, qNode, inputSymbols, transitionTable, qFinal, \
        globalOutput, var

    allStates = []
    qNode = ''
    inputSymbols = []
    transitionTable.clear()
    qFinal = ''

    # mapping the strings to the content of the input from the GUI
    statesString = setOfStatesInput.get()
    startStateString = startStateInput.get()
    alphabetString = alphabetInput.get()
    finalStatesString = finalStatesInput.get()
    deltaString = deltaInput.get()

    # transform strings into arrays
    allStates = statesString.split(',')
    qNode = startStateString
    inputSymbols = alphabetString.split(',')
    qFinal = finalStatesString.split(',')
    transitionTable = [list(line.split(',')) for line in deltaString.split('|')]

    # fill the transition table with states and symbols only
    for q in allStates:  # loop over all states
        dfaTransitionTable[q] = {}  # initialize the transition row for the state currently looping on
        for input in inputSymbols:  # loop over all symbols in the alphabet
            dfaTransitionTable[q][input] = []  # initialize state-symbol pairs

    # fill the dictionary with the transitioning states
    for t in transitionTable:  # loop over the transition function
        cs, a, ns = t  # extract the state in cs, the symbol in a, and the next state in ns
        dfaTransitionTable[cs][a].append(ns)  # fill the dictionary of state cs symbol a with the transitioned state ns

    ################

    # Algorithm NFA to DFA

    # new arrays for current state, new transition function and new dfa states
    dfaStates = [[qNode]]
    newDFATransitionTable = []
    tempDFAStates = [[qNode]]

    #                     tempDFAStates |    Symbol1 (0)   |    Symbol2 (1)   |  ...etc
    #                  -------------------------------------------------------------------
    #  currentDFAState ->       q0       |        ns1       |         ns2      |
    #                                   |                  |                  |
    #                                   |                  |                  |
    #                                   |                  |                  |
    #
    #  ns & y determined by the pre-defined dictionary as follows
    #      delta_dict[currentDFAState][input]   -> currentDFAState could be more than one state like {A,B}
    #      so it's iterated upon all its elements

    # loop over all new dfa states, row by row
    while len(tempDFAStates) > 0:
        currentDFAState = tempDFAStates[0]  # current state is the first dfa state
        tempDFAStates = tempDFAStates[1:]  # remove the first state from the temporary dfa state

        # concatenate the current state to the global output, to be displayed in GUI
        globalOutput += 'Current state: ' + '{' + ', '.join(f'{w}' for w in currentDFAState) + '}' + '\n'

        # loop over the symbols in the alphabet (for each state)
        for input in inputSymbols:
            followingState = []  # create a list of the next states (for union between multiple states)
            for singleState in currentDFAState:  # loop over each element of the current state (important if the current state is made up of more than 1)
                for ns in dfaTransitionTable[singleState][input]:  # loop over the transition table's next states
                    if ns not in followingState:  # check if ns is not already in the list of next states
                        followingState.append(ns)  # add the new next state to the list of next states
            newDFATransitionTable.append([currentDFAState, input, followingState])  # add (current state - input - following state) to the transition table
            # concatenate the next state corresponding to each input symbol to the global output, to be displayed in GUI
            globalOutput += 'When input = ' + ', '.join(f'{w}' for w in input) + ', Go to : {' + ', '.join(
                f'{w}' for w in followingState) + '}\n'

            # check if next state has not been previously handled, as
            if followingState not in dfaStates:
                dfaStates.append(followingState)  # add next state to dfa state
                tempDFAStates.append(followingState)  # add next state to new dfa state

        globalOutput += '\n'  # concatenate a new line, to be displayed in GUI

    # concatenate the DFA states to the global output, to be displayed in GUI
    globalOutput += 'DFA Q = { '
    globalOutput += ', '.join(f'{w}' for w in dfaStates)
    globalOutput += ' }\n\n'

    # concatenate the DFA transition table (delta) to the global output, to be displayed in GUI
    globalOutput += 'DFA Delta = \n'
    globalOutput += pformat(newDFATransitionTable)

    # print global output to ensure it is correct
    print(globalOutput)

    var.set(globalOutput)

################


# GUI code
root = Tk()
root.geometry(str(1000) + "x" + str(400))
root.title("NFA to DFA - ASU Final Automata Course Project")

Label(root, text="Enter NFA to convert", font=("Montserrat", 18), fg='#000000').grid(column=1, row=1, padx=2, sticky="w")

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

