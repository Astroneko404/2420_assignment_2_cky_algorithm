from CKY import CKY
import sys


if __name__ == '__main__':
    if len(sys.argv) != 4:
        print('Need 3 arguments!')
        print('1) The grammar file; 2) The sentence; 3) Gold Standard')

    else:
        my_cky = CKY(sys.argv[1])
