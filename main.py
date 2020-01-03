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

def Col_stariLR0(G):
    C = []
    s0 = closure()
    C.append(s0)
    ok = True
    while ok:
        for s in C:
            for X in N:
                if goto(s, X) and goto(s, X) not in C:
                    C.append(goto(s, X))
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