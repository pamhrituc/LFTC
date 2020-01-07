import copy
from grammar import *

from state import State

def Col_stariLR0(G):
	NE = G.N + G.E  # terminals and non-terminals
	C = []  # canonical collections of  states
	productions_verified = []
	index = 0
	s0 = State(closure(("S'", "." + G.N[0]), G))
	C.append(s0)
	s0.set_index(index)
	ok = True
	isLR0 = True
	while ok:
		for s in C:
			for X in NE:
				state, prod_verified = goto(s, X, G)

				if prod_verified and prod_verified in productions_verified:
					s.add_goto_value((X, productions_verified.index(prod_verified) + 1))
					ok = False

				if state.action(G.P) == "ERROR1":
					print("We have an accept conflict, thus this grammar isn't of type LR0")
					isLR0 = False
					ok = False
				if state.action(G.P) == "ERROR2":
					print("We have shift - reduce conflict, thus this grammar isn't of type LR0")
					isLR0 = False
					ok = False
				if state.action(G.P) == "ERROR3":
					print("We have an reduce - reduce conflict, thus this grammar isn't of type LR0")
					isLR0 = False
					ok = False
				
				if not isLR0:
					return False

				if state.productions and ok:
					C.append(state)
					index = index + 1
					state.set_index(index)
					s.add_goto_value((X, state.index))
					productions_verified.append(prod_verified)
			if not ok:
				break
		if not ok:
			break
	return C

def count(rhs, G):
	tNT = G.N + G.E
	nonTerminal = nonTerminalIn(rhs, G)
	terminal = terminalIn(rhs, G)
	k = 0
	if terminal:
		if rhs[:len(terminal)] == terminal:
			k += 1
			rhs = rhs[len(terminal):]
	if nonTerminal:
		if rhs[:len(nonTerminal)] == nonTerminal:
			k += 1
			rhs = rhs[:len(nonTerminal)]
	return k

def nonTerminalIn(string, G):
	for nonterminal in G.N:
		if nonterminal in string:
			return nonterminal

def terminalIn(string, G):
	for nonterminal in G.E:
		if nonterminal in string:
			return nonterminal

def shiftDot(rhs, G):
	rhsCopy = copy.deepcopy(rhs)
	dotIndex = rhs.find('.')
	rhs = rhs.replace('.', '')
	currentWord = ""
	indexFound = -1
	tNT = G.N + G.E
	for index in range(dotIndex, len(rhs)):
		currentWord += rhs[index]
		if currentWord in tNT:
			indexFound = index
			break
	rhs = rhs[:indexFound + 1] + "." + rhs[indexFound + 1:]
	return rhs
				

def closure(I, G):
	C = [I]
	ok = True
	while ok:
		for c in C:
			#production is all the productions of B
			nt = nonTerminalIn(C[0][1], G)
			if not nt:
				return C
			productions = G.get_productions_for(nt)

			if productions != []:
				for production in productions:
					prod = (production[0], shiftDot(production[1], G))
					if prod not in C:
						C.append(prod)
						ok = True
					if prod in C:
						ok = False
			if productions == []:
				ok = False
	return C


'''
Input:
	s - state
	X - nonterminal/terminal
	G - grammar
Output:
	closureList - list of productions
'''
def goto(state, X, G):
	#all productions w/ X on rhs of s
	elems = [] # elems(productions) to do goto
	closureList = []
	for prod in state.productions:
		element = "." + X
		if element in prod[1]:
			elems.append((prod[0], shiftDot(prod[1], G)))

	for elem in elems:
		if elem[1][-1] == ".":
			closureList.append(elem)
		else:
			closureList = closure(elem, G)
	return [State(closureList), elems]

def anal_syntLR0(input_stack, C, G):
	work_stack = ['$', 0]
	output = []
	done = False
	P = G.P
	while not done:
		state = C[work_stack[-1]]
		action = state.action(P)

		if action == "SHIFT":
			print("entered shift")
			val = input_stack[0]
			found = False
			for goto_val in state.goto_values:
				if val == goto_val[0]:
					work_stack.append(val)
					work_stack.append(goto_val[1])
					input_stack.pop(0)
					found = True
					break
				else:
					found = False
			if not found:
				print("Error")
				break

		elif "REDUCE" in action:
			print("entered reduce")
			prod_index = action[6:]
			output.append(prod_index)

			production = P[int(prod_index)]

			nr = count(production[1], G) * 2
			for i in range(nr):
				work_stack.pop()

			val = production[0]
			state = C[work_stack[-1]]
			found = True
			for goto_val in state.goto_values:
				if val == goto_val[0]:
					work_stack.append(val)
					work_stack.append(goto_val[1])
					found = True
					break
				else:
					found = False
			if not found:
				print("Error: Couldn't find production")
				break

		elif action == "ACCEPT":
			print("Success")
			str = "".join(output)
			print("Output: " + str[::-1])
			break

		else:
			print("Error")
			break

def main():
	g = Grammar.from_file("exemplu2.txt")
	
	C = Col_stariLR0(g)
	if not C:
		print("Grammar is not of type LR0")
	else:
		print("C:")
		for s in C:
			print("s" + str(s.index))
			print(s.productions)
			print(s.action(g.P))
			print("goto values:")
			print(s.goto_values)
			print("\n")

		#input_stack = ["a", "b", "b", "c"]
		input_stack = ["31", "09", "01"]

		anal_syntLR0(input_stack, C, g)

main()