#7SnakeProblem
Project to explore the 7 Snake Problem

##Problem description
In a matritial board, two snakes built from seven cells must to be allocated. Each cell in the matrix have a value and each snake's weight is the sum of the values in the cells that build the snake. The constraints to allocate them are:

* Both snakes must have the same weight.

* They must be built only from adjacent cell in the top, bottom, right or left. No diagonal path in the board is allowed.

* They can't have cells intersections.

* If the allocation is not possible, a FAIL message must to be shown.

##Proposal

From the board, a graph are built where each vertice is created from a cell and they will be connected only if the hop from one cell to other is allowed. Therefore, a path in the graph from a vertice v to u represents a snake with head in v and tail in u, following the building constraints (from on vertices, connections only to vertices in T, B, R, L positions in the board).

Thus, starting in any vertices, a backtrack dfs like algorithm can search find all paths with the maximum depth defined by the snake size. In the end of each snake, the sum is calculated and the group of cell is check against the other snakes with the same size to verify if any intersection exists. The first snake without intersection is returned together the last computed if no intersection exists. In the end, if no pair is found, a FAIL message is returned.

##Info
* notebooks directory - Solution Exploration and Analysis.

* script directory - Script to run over an input csv matrix file.
