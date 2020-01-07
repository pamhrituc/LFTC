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
			# print("nooooow")
			# print(self.productions)
			prod = (self.productions[0][0], self.productions[0][1].replace('.', ''))
			# print("prod")
			# print(prod)
			if prod == P[0]:
				return "ACCEPT"
			else:
				return "REDUCE" + str(P.index(prod))
		else:
			return "SHIFT"





