from collections import defaultdict
import re


def build_cnf(grammar_txt):
    grammar = defaultdict(lambda: defaultdict(lambda: 0.0))
    lexicon = defaultdict(lambda: defaultdict(lambda: 0.0))
    part = 0  # 0 for grammar, 1 for lexicon
    rule = r'(\d*\.\d*)\ (.*)->(.*)[\n]*'

    with open(grammar_txt) as file:
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
                    grammar[parent][child] = float(prob)
                else:  # Lexicon part
                    lexicon[parent][child] = float(prob)

        # print_nested_dict(grammar)
        # print_nested_dict(lexicon)
    file.close()

    return grammar, lexicon


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


class CKY:
    def __init__(self, grammar_txt):
        self.grammar, self.lexicon = build_cnf(grammar_txt)

