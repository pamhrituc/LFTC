class State:
	def __init__(self, productions):
		self.productions = productions
		self.goto_values = []
		self.index = -1

	def add_goto_value(self, values):
		self.goto_values.append(values)

	def set_index(self, index):
		self.index = index

	def action(self, P):
		if len(self.productions) == 1:
			prod = (self.productions[0][0], self.productions[0][1].replace('.', ''))
			if prod == P[0]:
				return "ACCEPT"
			else:
				return "REDUCE" + str(P.index(prod))
		else:
			ok = -1
			sr = -1
			for production in self.productions:
				prod = (production[0], production[1].replace('.', ''))
				if production[1].find('.') == len(production[1]) - 1:
					if prod == P[0]:
						return "ERROR1"
					if ok != -1 and P.index(prod) != ok:
						return "ERROR3"
					if ok == -1:
						ok = P.index(prod)
					if sr == -1:
						sr = 1
					if sr == 0:
						return "ERROR2"
				else:
					if sr == 1:
						return "ERROR2"
					if sr == -1:
						sr = 0
			return "SHIFT"

'''
P = [("S'", 'S'), ('S', 'aA'), ('A', 'a')]
s0 = State([("S'", 'S.'), ('S', '.a')])
s1 = State([('S', 'a.A'), ('A', 'a.')])
s2 = State([('A', 'a.'), ('S', 'aA.')])
print(s0.action(P))
print(s1.action(P))
print(s2.action(P))
'''