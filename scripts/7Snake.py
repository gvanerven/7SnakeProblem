import seven_snake as sn
import numpy as np
import sys

if __name__ == "__main__":
    matrix = np.loadtxt(sys.argv[1], delimiter=',', dtype='int')
    if matrix.shape[0] * matrix.shape[1] < 14:
        print('FAIL')
        print('Matrix Dimensions' + str(matrix.shape))
        sys.exit(-1)
    
    graph_board = sn.gen_graph(matrix)
    pair = sn.search_snakes(graph_board, 7)
    if pair is None:
        print('FAIL')
        print('Pair is None')
        sys.exit(-1)
    
    if sn.check_sum(graph_board, pair):
        print(sn.decode_coord_label(graph_board, matrix, pair))
        bd, bd_plot = sn.map_snakes_matrix(graph_board, matrix, pair)
        print(bd)
        print(bd_plot)
        sn.plot_snakes_board(bd_plot)
        
