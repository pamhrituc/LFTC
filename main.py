from grammar import *
import re

from state import State

'''
W is the list of codifications from the PIF

every production terminal needs to be replaced w/ it's code from the codification table
'''


def Col_stariLR0(G):
	NE = G.N + G.E  # terminals and non-terminals
	C = []  # canonical collections of  states
	productions_verified = []
	s0 = State(closure(("S'", '.S'), G))
	C.append(s0)
	ok = True
	while ok:
		for s in C:
			for X in NE:
				state, prod_verified = goto(s, X, G)
				if prod_verified and prod_verified in productions_verified:
					ok = False
					break
				if state.productions:
					C.append(state)
					productions_verified.append(prod_verified)
					# print(state.productions)
			if not ok:
				break
		if not ok:
			break
	return C

'''
We need a fuction to build the table
We need to add the input for the following function (page 75)
'''
def anal_syntLR0():
	j = 1
	state = 0
	stack = ['$']
	out = ""
	done = False
	while done != True:
		if state.action(g.P) == 'shift':
			stack.append(a[j])
			j += 1
		else:
			if state.action(g.P) == 'reduce':
				pass
			else:
				if state.action(g.P) == 'accept':
					print("Success")
					print(out)
					done = True
				if state.action(g.P) == 'error':
					print("Error")
					done = True

def nonTerminalIn(string, G):
	for nonterminal in G.N:
		if nonterminal in string:
			return nonterminal

def terminalIn(string, G):
	for nonterminal in G.E:
		if nonterminal in string:
			return nonterminal

def shiftDot(rhs, G):
	if "." not in rhs:
		return "." + rhs
	else:
		if rhs[-1] == '.':
			return rhs
		else:
			index = rhs.find(".")
			rhsList = list(rhs)
			rhsList[index], rhsList[index+1] = rhsList[index+1], rhsList[index]
			return "".join(rhsList)

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


g = Grammar.from_file("exemplu1.txt")
#for p in g.P:
#    print(p[0] + "->" + p[1])

# s0 = State([])
# s0.productions = closure(("S'", ".S"), g)
# print("\ns0:")
# print(s0.productions)
# print(s0.action(g.P))
#
# s1, el = goto(s0, 'S', g)
# print("\ns1:")
# print(s1.productions)
# print(s1.action(g.P))
#
#
# s2, el = goto(s0, 'a', g)
# print("\ns2:")
# print(s2.productions)
# print(s2.action(g.P))
#
# s3, el = goto(s2, 'A', g)
# print("\ns3:")
# print(s3.productions)
# print(s3.action(g.P))
#
#
# s4, el = goto(s2, 'b', g)
# print("\ns4:")
# print(s4.productions)
# print(s4.action(g.P))
#
#
# s5, el = goto(s2, 'c', g)
# print("\ns5:")
# print(s5.productions)
# print(s5.action(g.P))


C = Col_stariLR0(g)
print("C:")
for s in C:
	print(s.productions)


