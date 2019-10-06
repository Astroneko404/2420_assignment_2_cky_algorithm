from decimal import Decimal
from collections import defaultdict
import re


# terminal = ['Det', 'Noun', 'Verb', 'Pronoun']


def print_nested_dict(d):
    """
    :param d: The nested defaultdict to be printed
    :return: None
    """
    for item, keys in d.items():
        print(item, end='')
        print(': ')
        for subitem, prob in keys.items():
            print(subitem, prob)
        print()
    return


def print_table(t):
    for i in range(len(t)):
        print(t[i])
    return


class CKY:
    def __init__(self, grammar_txt):
        self.grammar_txt = grammar_txt
        self.grammar = defaultdict(lambda: defaultdict(lambda: Decimal(0.0)))
        self.lexicon = defaultdict(lambda: defaultdict(lambda: Decimal(0.0)))
        self.bin_map = defaultdict(lambda: '')  # X_n -> (t_1, t_2)
        self.bin_map_inverted = defaultdict(lambda: '')  # (t_1, t_2) -> X_n

        self.build_pcfg()
        self.binarize()
        self.check_prob()
        # print_nested_dict(self.grammar)

    def build_pcfg(self):
        """
        Build the probabilistic CFG
        """
        part = 0  # 0 for grammar, 1 for lexicon
        rule = r'(\d*\.\d*)\ (.*)->(.*)[\n]*'

        with open(self.grammar_txt) as file:
            for line in file:
                if line == 'Grammar\n':
                    continue
                elif line == 'Lexicon\n':
                    part = 1
                else:
                    line = [s for s in re.split(rule, line) if s]
                    prob, parent, child = line[0], line[1], line[2]
                    if part is 0:  # Grammar part
                        child = tuple(i for i in child.split())
                        self.grammar[parent][child] = Decimal(prob)
                    else:  # Lexicon part
                        self.lexicon[parent][child.lower()] = Decimal(prob)
            # print_nested_dict(self.grammar)
            # print_nested_dict(self.lexicon)
        file.close()

    def binarize(self):
        grammar_tmp = self.grammar.copy()
        bin_count = 1

        for parent in list(self.grammar):
            for child in list(self.grammar[parent]):
                if len(child) > 2:  # Since there's no child with terminals >=4, we don't need to use while loop
                    tag = child[:2]
                    rest = child[2:]
                    if tag not in self.bin_map_inverted:
                        label = 'X' + str(bin_count)

                        self.bin_map[label] = tag
                        self.bin_map_inverted[tag] = label
                        grammar_tmp[parent][tuple([label]) + rest] = grammar_tmp[parent].pop(child)
                        grammar_tmp[label][tag] = Decimal(1.0)

                        bin_count += 1

                    else:
                        label = self.bin_map_inverted[tag]
                        grammar_tmp[parent][tuple([label]) + rest] = grammar_tmp[parent].pop(child)

        self.grammar = grammar_tmp

        # Convert unit productions
        for parent in list(self.grammar):
            for child in list(self.grammar[parent]):
                if len(child) == 1 and child[0] not in self.lexicon:
                    base_prob = self.grammar[parent][child]
                    self.grammar[parent].pop(child)
                    # print(child[0], base_prob)
                    for rule, prob in self.grammar[child[0]].items():
                        # print(rule, prob)
                        self.grammar[parent][rule] = prob * base_prob

        # print_nested_dict(self.grammar)

    def check_prob(self):
        for parent in self.grammar:
            assert sum([self.grammar[parent][i] for i in self.grammar[parent]]) == Decimal(1.0)
        for parent in self.lexicon:
            assert sum([self.lexicon[parent][i] for i in self.lexicon[parent]]) == Decimal(1.0)

    def build_tree(self, back, table, n):
        print(back[1][n])
        return

    def prob_cky(self, words):
        n = len(words)
        table = [[dict() for i in range(n+1)] for j in range(n+1)]
        back = [[dict() for i in range(n+1)] for j in range(n+1)]

        for j in range(1, n+1):
            for A in self.lexicon:
                if words[j-1] in self.lexicon[A]:
                    table[j-1][j][A] = (self.lexicon[A][words[j-1]])
            for A in self.grammar:
                for rule, prob in self.grammar[A].items():
                    if len(rule) == 1:
                        B = rule[0]
                        # print(A, B)
                        if B in table[j-1][j]:
                            table[j-1][j][A] = table[j-1][j][B] * prob

            # print(table[1][2])

            for i in reversed(range(0, j - 1)):
                for k in range(i+1, j):
                    for A in self.grammar:
                        # print(self.grammar[A])
                        for rule, prob in self.grammar[A].items():
                            if len(rule) == 2:
                                B, C = rule[0], rule[1]

                                if B in table[i][k] and C in table[k][j]:
                                    # print(B, table[i][k])
                                    # print(C, table[k][j])
                                    # print()
                                    if A not in table[i][j]:
                                        table[i][j][A] = prob * table[i][k][B] * table[k][j][C]
                                    elif table[i][j][A] < prob * table[i][k][B] * table[k][j][C]:
                                        table[i][j][A] = prob * table[i][k][B] * table[k][j][C]
                                        back[i][j][A] = (k, B, C)

        # self.build_tree(back, table, n)
        for i in range(len(table)):
            for j in range(len(table[0])):
                print(i, j, table[i][j])
        return
