'''
W is the list of codifications from the PIF

every production terminal needs to be replaced w/ it's code from the codification table
'''

def closure(I, G):
    C = [I]
    ok = True
    while ok:
        for c in C: #c is A->a.Bb
            #production is all the productions of B
            for production in G.P:
                if production not in C:
                    C.append(production)
                    ok = True
                else:
                    ok = False
    return C

def goto(s, X):
    #all productions w/ X on rhs
    return closure(X, s)