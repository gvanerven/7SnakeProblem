import networkx as nx
import numpy as np
import matplotlib
import matplotlib.pyplot as plt


def gen_graph(board):
    """
    Converts a matrix to graph when the vertices only can be conected to 
    cells on TOP, BOTTOM, LEFT or RIGHT
    """
    G = nx.Graph()
    x, y = board.shape
    G.add_nodes_from(list(range(1,(x*y)+1)))
    for i in range(x):
        for j in range(y):
            vertice_id = ((i*y) + j) + 1
            ix = i+1
            jy = j+1
            G.nodes[vertice_id]['ignore'] = False
            G.nodes[vertice_id]['label'] = "{},{}".format(ix,jy)
            G.nodes[vertice_id]['index'] = "{},{}".format(i,j)
            G.nodes[vertice_id]['value'] = board[i,j]
            if i-1 > -1:
                pos_top = (((i-1)*y) + j) + 1
                G.add_edge(vertice_id, pos_top, position='T')
            if i+1 < x:
                pos_bottom = (((i+1)*y) + j) + 1
                G.add_edge(vertice_id, pos_bottom, position='B')
            if j-1 > -1:
                pos_left = ((i*y) + (j-1)) + 1
                G.add_edge(vertice_id, pos_left, position='L')
            if j+1 < y:
                pos_right = ((i*y) + (j+1)) + 1
                G.add_edge(vertice_id, pos_right, position='R')
    return G


def find_distinct_set(list_sets, new_set):
    """
    Verify if an element in the new set is in any other set os the list_sets
    """    
    for elem_set in list_sets:
        #Set & operator Suggested by Wagner Alberto
        if not elem_set & new_set:
            return elem_set
    return None


def search_snakes(graph, snake_size):
    """
    Enumerate and search for the two snakes using a modified DFS algorithm.
    """
    summ = {}
    
    def dfs_7snakes(graph, new_snake, vertice_id, val_sum, num_snake_piece, max_snake_size, dict_sum):
        found = None
        if num_snake_piece == max_snake_size:
            #this_snake = new_snake | set([vertice_id])
            if val_sum in dict_sum:
                # Checks if exists other snake without overposition
                other_snake = find_distinct_set(dict_sum[val_sum], new_snake)
                if other_snake is not None:
                    dict_sum[val_sum].append(new_snake)
                    return other_snake, new_snake, val_sum
                else:
                    dict_sum[val_sum].append(new_snake)
            else:                
                dict_sum[val_sum] = [new_snake]
            return None
        
        # Only no visited nodes to avoid snake loops itself
        neighbors_to_go = set(list(graph.neighbors(vertice_id))) - new_snake

        if len(neighbors_to_go) > 0:
            for vertice in neighbors_to_go:
                if not graph.nodes[vertice]['ignore']:
                    found = dfs_7snakes(graph, (new_snake | set([vertice])), vertice, (val_sum + graph.nodes[vertice]['value']), num_snake_piece + 1, max_snake_size, dict_sum)
                    if found is not None:
                        return found
        return found
    # End of internal function dfs_7snakes
    
    for vertice in graph.nodes:
        pair = dfs_7snakes(graph, set([vertice]), vertice, graph.nodes[vertice]['value'], 1, snake_size, summ)
        if pair is not None:
            return pair
        else:
            graph.nodes[vertice]['ignore'] = True
    return pair


def decode_coord_label(graph, board, pair):
    """
    Converts the pair ids in graph to pairs of coordinates in matrix from the key label.
    """
    snake1, snake2, summation = pair
    coord_snake1 = []
    coord_snake2 = []    
    for vertice_id in snake1:
        coord = graph.nodes[vertice_id]['label'].split(",")
        coord_snake1.append((int(coord[0]),int(coord[1])))

    for vertice_id in snake2:
        coord = graph.nodes[vertice_id]['label'].split(",")
        coord_snake2.append((int(coord[0]),int(coord[1])))

    return coord_snake1, coord_snake2, summation


def map_snakes_matrix(graph, board, pair):
    bd = np.zeros(board.shape)
    bd_plot = np.zeros(board.shape)
    snake1, snake2, summ = pair
    for vertice_id in snake1:
        coord = graph.nodes[vertice_id]['index'].split(",")
        bd[int(coord[0]),int(coord[1])] = board[int(coord[0]),int(coord[1])]
        bd_plot[int(coord[0]),int(coord[1])] = 10

    for vertice_id in snake2:
        coord = graph.nodes[vertice_id]['index'].split(",")
        bd[int(coord[0]),int(coord[1])] = board[int(coord[0]),int(coord[1])]
        bd_plot[int(coord[0]),int(coord[1])] = 100

    return bd, bd_plot


def check_sum(graph, pair):
    """
    Check if the sum in the cells for both snakes are the same.
    """
    sum_snake1 = 0
    sum_snake2 = 0
    snake1, snake2, summ = pair
    for vertice_id in snake1:
        sum_snake1 += graph.nodes[vertice_id]['value']
    for vertice_id in snake2:
        sum_snake2 += graph.nodes[vertice_id]['value']

    if sum_snake1 == sum_snake2 and sum_snake1 == summ:
        return True
    else:
        print(sum_snake1)
        print(sum_snake2)
        print(summ)    
        return False

def plot_snakes_board(board):
    plt.clf()
    #https://stackoverflow.com/questions/19586828/drawing-grid-pattern-in-matplotlib
    data = np.ones((board.shape)) * np.nan
    x, y = board.shape
    for i in range(x):
        for j in range(y):
            if board[i,j]:
                data[i,j] = board[i,j]
                   
    # make a figure + axes
    fig, ax = plt.subplots(1, 1, tight_layout=True)
    # make color map
    my_cmap = matplotlib.colors.ListedColormap(['r', 'g', 'b'])
    # set the 'bad' values (nan) to be white and transparent
    my_cmap.set_bad(color='w', alpha=0)
    # draw the grid
    for i in range(x + 1):
        ax.axhline(i, lw=2, color='k', zorder=5)
        ax.axvline(i, lw=2, color='k', zorder=5)
    # draw the boxes
    ax.imshow(data, interpolation='none', cmap=my_cmap, extent=[0, x, 0, x], zorder=0)
    # turn off the axis labels
    ax.axis('off')
    plt.show()