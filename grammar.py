class Grammar:
    def __init__(self, N, E, P, S):
        self.N = N
        self.E = E
        self.P = P
        self.S = S

    def is_non_terminal(self, value):
        return value in self.N
        
    def is_terminal(self, value):
        return value in self.E

    def is_regular(self):
        used_in_rhs = dict()
        not_allowed_in_rhs = list()

        for prod in self.P:
            lhs, rhs = prod
            has_terminal = False
            has_non_terminal = False
            if len(rhs) > 2:
                return False
            for char in rhs:
                if self.is_non_terminal(char):
                    used_in_rhs[char] = True
                    has_non_terminal = True
                elif self.is_terminal(char):
                    if has_non_terminal:
                        return False
                    has_terminal = True
                if char == 'E':
                    not_allowed_in_rhs.append(lhs)

            if has_non_terminal and not has_terminal:
                return False

        for char in not_allowed_in_rhs:
            if char in used_in_rhs:
                return False

        return True

    def get_productions_for(self, non_terminal):
        if not self.is_non_terminal(non_terminal):
            raise Exception('Can only show productions for non-terminals')
        return [prod for prod in self.P if prod[0] == non_terminal]

    def show_productions_for(self, non_terminal):
        productions = self.get_productions_for(non_terminal)
        print(', '.join([' -> '.join(prod) for prod in productions]))

    def get_right_hand_side_for(self, non_terminal):
        pass
    def __str__(self):
        return 'Set of nonterminal symbols: N = { ' + ', '.join(self.N) + ' }\n' \
                + 'Set of terminal symbols:  E = { ' + ', '.join(self.E) + ' }\n' \
                + 'Finite set of productions: P = { ' + ', '.join([' -> '.join(prod) for prod in self.P]) + ' }\n' \
                + 'Start symbol: S = ' + str(self.S) + '\n'

    @staticmethod
    def parse_line(line):
        return [value.strip() for value in line.strip().split('=')[1].strip()[1:-1].strip().split(',')]

    @staticmethod
    def parse_console(line):
        return [value.strip() for value in line.strip()[1:-1].strip().split(',')]

    @staticmethod
    def from_file(file_name):
        with open(file_name) as file:
            N = Grammar.parse_line(file.readline())
            E = Grammar.parse_line(file.readline())
            S = file.readline().split('=')[1].strip()
            P = Grammar.parsing(Grammar.parse_line(''.join([line for line in file])))

            return Grammar(N, E, P, S)

    @staticmethod
    def parsing(productions):
        result = []
        for prod in productions:
            lhs, rhs = prod.split('->')
            lhs = lhs.strip()
            rhs = [value.strip() for value in rhs.split('|')]
            for value in rhs:
                result.append((lhs, value))

        return result
