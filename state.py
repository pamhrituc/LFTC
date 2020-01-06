class State:
	def __init__(self, productions):
		self.productions = productions

	def action(self, P):
		if len(self.productions) == 1:
			prod = (self.productions[0][0], self.productions[0][1][:-1])
			if prod == P[0]:
				return "ACCEPT"
			else:
				return "REDUCE" + str(P.index(prod))
		else:
			return "SHIFT"





