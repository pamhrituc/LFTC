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
	index = 0
	s0 = State(closure(("S'", "." + G.N[0]), G))
	C.append(s0)
	s0.set_index(index)
	ok = True
	while ok:
		for s in C:
			for X in NE:
				state, prod_verified = goto(s, X, G)

				if prod_verified and prod_verified in productions_verified:
					s.add_goto_value((X, productions_verified.index(prod_verified) + 1))
					ok = False

				if state.productions and ok:
					C.append(state)
					index = index + 1
					state.set_index(index)
					s.add_goto_value((X, state.index))
					productions_verified.append(prod_verified)
					# print(state.productions)
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
	if "." not in rhs:
		return "." + rhs
	else:
		if rhs[len(rhs) - 1] == '.':
			return rhs
		else:
			rhs_list = list(rhs)

			non_terminal = nonTerminalIn(rhs[rhs.find("."):], G)
			terminal = terminalIn(rhs[rhs.find("."):], G)

			dot_pos = rhs.find('.')
			# print("\nrhs = " + rhs)
			if non_terminal and rhs[dot_pos:].find(non_terminal) == 1:
					k = non_terminal
					# print("k = " + k)
			else:
				if terminal and rhs[dot_pos:].find(terminal) == 1:
					k = terminal
					# print("k = " + k)

			i = rhs_list.index(".")
			# print("k = " + str(k))
			for j in range(i, i + len(k)):
				rhs_list[j] = rhs_list[j+1]

			rhs_list[i + len(k)] = "."

			rhs = ""
			for elem in rhs_list:
				rhs += elem
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

'''
We need a fuction to build the table
We need to add the input for the following function (page 75)
'''
def anal_syntLR0(input_stack, C, G):
	work_stack = ['$', 0]
	output = []
	done = False
	P = G.P
	while not done:
		# print("\nwork stack: ")
		# print(work_stack)
		# print("output: ")
		# print(output)
		state = C[work_stack[-1]]
		action = state.action(P)

		if action == "SHIFT":
			# print("entered shift")
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
			# print("entered reduce")
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
				print("Error")
				break

		elif action == "ACCEPT":
			print("Success")
			str = "".join(output)
			print(str[::-1])
			break

		else:
			print("Error")
			break


	# while done != True:
	# 	action = state.action(P)
	# 	if action == 'SHIFT':
	# 		stack.append(a[j])
	# 		j += 1
	# 	else:
	# 		if 'REDUCE' in action:
	# 			index = action[6:]
	#
	# 			pass
	# 		else:
	# 			if action == 'ACCEPT':
	# 				print("Success")
	# 				print(out)
	# 				done = True
	# 			else:
	# 				print("Error")
	# 				done = True

# g = Grammar.from_file("exemplu1.txt")

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
g = Grammar.from_file("example2.txt")


C = Col_stariLR0(g)
print("C:")
for s in C:
    print("s" + str(s.index))
    print(s.productions)
    print(s.action(g.P))
    print("goto values:")
    print(s.goto_values)
    print("\n")

# input_stack = ["a", "b", "b", "c"]
input_stack = ["a", "a"]

anal_syntLR0(input_stack, C, g)





