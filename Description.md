## Homework 2 (CS 2731)
#### Assigned: September 26, 2019
#### Due: October 10, 2019 (midnight)

### 2.1 HMM Decoding (Viterbi) (20 points)

A partial Viterbi calculation is pictured 
[here](https://gawron.sdsu.edu/compling/course_core/comp_ling_assignments/_images/viterbi_computation.jpg). 
This calculation takes us up through t=2 where v2(1) and v2(2) are computed. 
In the picture, the index 1 is used for the state labeled C and the index 2 is used for the 
state labeled H. Compute v3(1) and v3(2). 
You will need the transition and observation probabilities given 
[here](http://people.cs.pitt.edu/~litman/courses/cs2731/hw/hw2/hmm.pdf).

Think of this as filling in a table where the columns are moments in time and the rows are states in the HMM. 
Filling in the table with the numbers computed in the diagram above, and adding a column 
for time t = 0, and showing all the probability cells, it looks like this:<br/>

|  t =  |  0  |   1  |    2   | 3 |
|:-----:|:---:|:----:|:------:|:-:|
|   H   |  0  | 0.32 | 0.0448 |   |
|   C   |  0  |  0.2 |  0.048 |   |
| Start | 1.0 |   0  |    0   |   |
|  End  |  0  |   0  |    0   |   |

Each cell in the Viterbi table is filled with one of the Viterbi values computed in the diagram. 
Like the diagram, the table is complete through t=2. 
The values in the cells represent Viterbi probabilities. 
The Viterbi probability written as v2(2) repesents the probability of the highest probability path that ends at state 2 at time 2.

* (10 points) Submit a completed version of the table above, together with the calculations you used to compute the Viterbi probabilities v3(1) and v3(2).
  * The calculations should show the products producing the path probabilities and the maximization that gives the final Viterbi value.
  * In addition, show how you would do all calculations in log (ln) space as well as directly as products of probabilities (recall Chapter 3). 

* (10 points) 
  * Report the best path through the HMM that fits the data.
  * Justify your answer by adding backtraces to your table, including the backtraces for column 3. This [figure](https://gawron.sdsu.edu/compling/course_core/comp_ling_assignments/_images/viterbi_with_backtrace_computation.jpg) illustrates the idea. The dashed lines represent the best path associated with each Viterbi value. In your submission you can just explain textually how you would modify the figure, e.g., "Add a backtrace link (dashed line) to the backtrace figure going from STATE? at time t = 3 to STATE? at time t = 2." 
