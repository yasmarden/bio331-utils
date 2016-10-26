##Mina Marden

##This file calls all functions included in graph_utils.py and file_utils.py

import file_utils
import graph_utils

def main():
	nodes, edges, neighbors = readData('test_graph.txt', True)
	adj_mat = adj_mat_fun(nodes, edges)
	node_degs = node_deg_finder(nodes, neighbors)
	neighbors = neighbor_finder(nodes, edges)
	ER_nodes, ER_edges = erdos_renyi(10,20)
	BA_nodes, BA_edges = barabasi_albert(nodes, 2, 3, 5, 2)
	lgc, max_cc = find_largest_cc(nodes, edges)
	return


if __name__=='__main__':
	main()