from grammar import *
import re
'''
W is the list of codifications from the PIF

every production terminal needs to be replaced w/ it's code from the codification table
'''
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
            rhsList = list(rhs)
            if rhs.find(nonTerminalIn(rhs[rhs.find("."):], G)) == rhs.find(".") + 1:
                k = nonTerminalIn(rhs[rhs.find("."):], G)
            elif rhs.find(terminalIn(rhs[rhs.find("."):], G)) == rhs.find(".") + 1:
                k = terminalIn(rhs[rhs.find("."):], G)
            i = rhsList.index(".")
            rhsList[i] = rhsList[i + len(k)]
            rhsList[i + len(k)] = "."
            rhs = ""
            for elem in rhsList:
                rhs += elem
            return rhs

def closure(I, G):
    C = [I]
    ok = True
    while ok:
        for c in C: 
            #production is all the productions of B
            productions = G.get_productions_for(nonTerminalIn(C[0][1], G))
            
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

def goto(s, X, G):
    #all productions w/ X on rhs of s
    elems = []
    closureList = []
    for prod in s:
        if X in prod[1]:
            elems.append(prod)
    for elem in elems:
        if elem[1][len(elem) - 1] == ".":
            closureList.append(elem)
        else:
            closureList.append(closure(elem, G))
    return closureList

def Col_stariLR0(G):
    C = []
    s0 = closure(G.get_productions_for("S'"), G)
    C.append(s0)
    ok = True
    while ok:
        for s in C:
            for X in G.N:
                if goto(s, X, G) and goto(s, X, G) not in C:
                    C.append(goto(s, X, G))
                    ok = True
                else:
                    ok = False
    return C

#We need a fuction to build the table
#We need to add the input for the following function (page 75)
def anal_syntLR0():
    j = 1
    state = 0
    stack = ['$']
    out = ""
    done = False
    while done != True:
        if action(state) == 'shift':
            stack.append(a[j])
            j += 1
        else:
            if action(state) == 'reduce':
                pass
            else:
                if action(state) == 'accept':
                    print("Success")
                    print(out)
                    done = True
                if action(state) == 'error':
                    print("Error")
                    done = True

g = Grammar.from_file("exemplu1.txt")
#for p in g.P:
#    print(p[0] + "->" + p[1])

s = []
s.append(closure(("S'", ".S"), g))
print(s)
print(goto(s[0], "c", g))

print(shiftDot(shiftDot(shiftDot(shiftDot("abS", g), g), g), g))