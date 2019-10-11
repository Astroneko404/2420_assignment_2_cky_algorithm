### INFSCI 2420 Assignment 2 
#### Environment 
Python 3.6
#### Binarization for CNF conversion
For binarization, I followed the steps on the textbook.
In order to save some space, there is no new grammar created,
and all modifications are on the original grammar:
1. Rules with right-hand side longer than 2 are normalized. 
For example, S -> Aux NP VP is written as S-> X1 VP and X1 -> Aux NP.
The probabilities are re-calculated so that the sum of probabilities starting with
S (or other tags) is 1.
If there are more than 3 tags on the right-hand side, there is a while
loop to deal with this situation.
2. Rules with single non-terminal on the right (Unit productions) are
eliminated by connecting the original left-hand side with all the non-unit
production rules that the original right-hand side leads to. 
Besides, the probabilities are also re-calculated by multiplying the 
probability of the unit production to the probability of every child
rule.
#### Other issues
1. There is no stemming or lemmatizing on the vocabulary.
2. As a result, due to the limited vocabulary of the lexicon, 
if the input sentence contains unseen words, 
the tree won't be generated

