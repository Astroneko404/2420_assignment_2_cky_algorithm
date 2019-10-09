from CKY import CKY, parse_tree_span
import sys


if __name__ == '__main__':
    if len(sys.argv) != 4:
        print('Need 3 arguments!')
        print('1) The grammar file; 2) The sentence; 3) Gold Standard')

    else:
        my_cky = CKY(sys.argv[1])
        words = sys.argv[2].lower().split()
        pred = my_cky.prob_cky(words)
        print(pred)
        pred_span = parse_tree_span(pred, words)
        print(pred_span)
