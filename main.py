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

def closure(I, G):
    C = [I]
    ok = True
    while ok:
        for c in C: #c is A->a.Bb
            #production is all the productions of B
            productions = []
            if c[1] in G.N:
                productions = G.get_productions_for(c[1])
            else:
                if any(nonterminal in c[1] for nonterminal in G.N):
                    productions = G.get_productions_for(nonTerminalIn(c[1], G))
            for production in productions:
                if production not in C:
                    C.append(production)
                    ok = True
                if production in C:
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

s0 = closure(("S'", "S"), g)
print(goto(s0, "X", g))