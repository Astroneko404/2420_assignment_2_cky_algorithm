from decimal import Decimal
from collections import defaultdict, deque
import numbers
import re


def evaluation(pred, true):
    """
    :param pred: Tree span for prediction
    :param true: Tree span for reference
    :return: recall and precision
    """
    pred_correct = [x for x in pred if x in true]
    recall = len(pred_correct) / len(true)
    precision = len(pred_correct) / len(pred)
    return recall, precision


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
        for j in range(1, len(t[0])):
            if j > i:
                print(i, j, t[i][j])
    return


def parse_tree_span(s, words):
    i = 0  # pointer for words
    idx = 0  # pointer for s
    word = ''
    queue = deque()
    result = []

    while idx < len(s):
        if s[idx] != '[' and s[idx] != ']':
            word += s[idx]
        else:
            if s[idx] == '[' and word:
                queue.append((word, i))
                word = ''
            elif s[idx] == ']':
                word = word.split()
                if len(word) == 2:
                    # assert word[1] == words[i]
                    while idx + 1 < len(s) and s[idx + 1] == ']':
                        tag, start = queue.pop()
                        result.append((tag, start, i))
                        idx += 1
                word = ''
                i += 1
        idx += 1

    result = sorted(result, key=lambda y: (y[1], -y[2]))
    return result


class CKY:
    def __init__(self, grammar_txt):
        self.grammar_txt = grammar_txt
        self.grammar = defaultdict(lambda: defaultdict(lambda: Decimal(0.0)))
        self.lexicon = defaultdict(lambda: defaultdict(lambda: Decimal(0.0)))
        self.bin_map = defaultdict(lambda: '')  # X_n -> (t_1, t_2)
        self.bin_map_inverted = defaultdict(lambda: '')  # (t_1, t_2) -> X_n
        self.back = None
        self.table = None

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

    def print_tree_level(self, tup, words):
        res = ''

        if len(tup) == 7:
            B, C, B_tag, C_tag, prob_B, prob_C, prob_A = tup
            B_i, B_j = B
            C_i, C_j = C
            next_B = None
            next_C = None

            for sub_tup in self.back[B_i][B_j][B_tag]:
                if isinstance(sub_tup, numbers.Number):
                    prob_next = sub_tup
                    if prob_next == prob_B:
                        next_B = ((B_i, B_j), B_tag, sub_tup)
                        break
                else:
                    prob_next = sub_tup[-1]
                    if prob_next == prob_B:
                        next_B = sub_tup
                        break

            for sub_tup in self.back[C_i][C_j][C_tag]:
                if isinstance(sub_tup, numbers.Number):
                    prob_next = sub_tup
                    if prob_next == prob_C:
                        next_C = ((C_i, C_j), C_tag, sub_tup)
                        break
                else:
                    prob_next = sub_tup[-1]
                    if prob_next == prob_C:
                        next_C = sub_tup
                        break

            # print(next_B)
            # print(next_C)

            if B_tag not in self.bin_map:
                res += '['
                if len(next_B) != 3:
                    res += B_tag
            res += self.print_tree_level(next_B, words)
            if B_tag not in self.bin_map: res += ']'

            if C_tag not in self.bin_map:
                res += '['
                if len(next_C) != 3:
                    res += C_tag
            res += self.print_tree_level(next_C, words)
            if C_tag not in self.bin_map: res += ']'

        elif len(tup) == 3:
            i, j = tup[0]
            tag = tup[1]
            res += tag + ' ' + words[j - 1]
        return res

    def build_tree(self, words):
        start = self.back[0][len(words)]
        if 'S' in start:
            result_list = []
            for tup in start['S']:
                res = '[S' + self.print_tree_level(tup, words) + ']'
                score = tup[-1]
                result_list.append((res, score))

            print('Sentence accepted:')
            return result_list
        else:
            print('Sentence rejected')
            return None

    def prob_cky(self, words):
        n = len(words)
        table = [[dict() for i in range(n + 1)] for j in range(n + 1)]
        back = [[dict() for i in range(n + 1)] for j in range(n + 1)]

        def is_terminal(tag):
            return tag in self.lexicon

        for j in range(1, n + 1):
            exist = False
            for A in self.lexicon:
                if words[j - 1] in self.lexicon[A]:
                    # table[j-1][j][A] = (self.lexicon[A][words[j-1]])
                    back[j - 1][j][A] = [(self.lexicon[A][words[j - 1]])]
                    exist = True
            if not exist:  # Edge cases
                print('The word "' + words[j - 1] + '" does not exist in the lexicon!')
                return ''
            # print_table(back)
            for A in self.grammar:
                for rule, prob in self.grammar[A].items():
                    if len(rule) == 1:
                        B = rule[0]
                        # print(A, B)
                        # if B in table[j-1][j]:
                        if B in back[j - 1][j]:
                            # table[j-1][j][A] = table[j-1][j][B] * prob
                            # print(back[j - 1][j])
                            if A in back[j - 1][j]:
                                back[j - 1][j][A].append(((j - 1, j), B, back[j - 1][j][B][0] * prob))
                            else:
                                back[j - 1][j][A] = [((j - 1, j), B, back[j - 1][j][B][0] * prob)]

            # print(table[1][2])
            # print_table(back)
            # print()

            for i in reversed(range(0, j - 1)):
                for k in range(i + 1, j):
                    for A in self.grammar:
                        # print(self.grammar[A])
                        for rule, prob in self.grammar[A].items():
                            if len(rule) == 2:
                                B, C = rule[0], rule[1]

                                if B in back[i][k] and C in back[k][j]:
                                    for B_sub in back[i][k][B]:
                                        for C_sub in back[k][j][C]:
                                            # print(B, B_sub)
                                            # print(C, C_sub)
                                            prob_B = Decimal(0.0)
                                            prob_C = Decimal(0.0)
                                            # print()
                                            if isinstance(B_sub, numbers.Number):
                                                prob_B = B_sub
                                            else:
                                                prob_B = B_sub[-1]

                                            if isinstance(C_sub, numbers.Number):
                                                prob_C = C_sub
                                            else:
                                                prob_C = C_sub[-1]
                                            prob_A = prob * prob_B * prob_C
                                            # if A not in table[i][j]:
                                            #     table[i][j][A] = prob * table[i][k][B] * table[k][j][C]
                                            # elif table[i][j][A] < prob * table[i][k][B] * table[k][j][C]:
                                            #     table[i][j][A] = prob * table[i][k][B] * table[k][j][C]
                                            if A not in back[i][j]:
                                                back[i][j][A] = [((i, k), (k, j), B, C, prob_B, prob_C, prob_A)]
                                            else:
                                                back[i][j][A].append(((i, k), (k, j), B, C, prob_B, prob_C, prob_A))

        self.back = back
        self.table = table
        # print_table(table)
        # print_table(back)
        result = self.build_tree(words)
        return result
