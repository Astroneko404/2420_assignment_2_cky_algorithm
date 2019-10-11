from CKY import CKY, evaluation, parse_tree_span
import sys
import re


if __name__ == '__main__':
    if len(sys.argv) != 4:
        print('Need 3 arguments!')
        print('1) The grammar file; 2) The sentence; 3) Gold Standard')

    else:
        my_cky = CKY(sys.argv[1])
        words = sys.argv[2].lower().split()
        new_words = []

        for c in words:  # Special cases
            if c == 'includes':
                c = 'include'
            new_words.append(c)

        pred_list = my_cky.prob_cky(new_words)
        true = re.sub(r'\ \[', r'[', sys.argv[3])
        true_span = parse_tree_span(true, words)

        for pred, score in pred_list:
            print(pred)
            pred_span = parse_tree_span(pred, words)
            recall, precision = evaluation(pred_span, true_span)
            print('Recall: ' + str(recall) + '\t' + 'Precision: ' + str(precision))
            print('Score: ' + str(score) + '\n')
