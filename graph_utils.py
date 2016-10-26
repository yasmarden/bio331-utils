import random

##Uses a nodes list and a dictionary of edges to create an adjacency matrix list
##of lists where there is a 1 if two nodes are connected by an edge and a 0, otherwise.
def adj_mat_fun(nodes, edges):
	adj_mat = [[]]*len(nodes)
	for i in range(len(nodes)):
		adj_mat[i] = [0]*len(nodes)
	for node1 in nodes:
		if node1 in edges:
			index1 = nodes.index(node1)
			for node2 in nodes:
				index2 = nodes.index(node2)
				for i in range(len(edges[node1])):
					if node2 in edges[node1][i][0]:
						adj_mat[index1][index2]=1
	return adj_mat

##Uses a nodes list and a dictionary of neighbors to create a list of node
##degrees that corresponds with the order of the nodes list given.
def node_deg_finder(nodes, neighbors):
	node_degs = [0]*len(nodes)
	for node in nodes:
		node_degs[nodes.index(node)] = len(neighbors[node])
	return node_degs

##Called by neighbor_finder in order to create a dictionary where the key is the source node
##and the entry is a list of target nodes.
def neighbor_dict_builder(u, v, neighbors, used_nodes):
	if str(u) not in neighbors:
		neighbors[u]=[v]
	elif v not in neighbors[u] and v not in neighbors[u]:
		neighbors[u] = neighbors[u]+[v]
	if str(v) not in neighbors:
		neighbors[v]=[u]
	elif u not in neighbors[v] and u not in neighbors[v]:
		neighbors[v] = neighbors[v]+[u]
	if u not in used_nodes:
		used_nodes.append(u)
	if v not in used_nodes:
		used_nodes.append(v)

	return neighbors, used_nodes

##Creates a dictionary of neighbors using a nodes list and edges. The function first checks 
##to see if edges is a list or a dictionary and then sets the source and target nodes 
##accordingly so that when node_dict_builder is called, node_dict_builder uses the right
##nodes to build the dictionary.
def neighbor_finder(nodes, edges):
	neighbors = {}
	used_nodes = []
	if isinstance(edges, dict):
		for node in edges:
			for neigh in edges[node]:
				neighbors, used_nodes = neighbor_dict_builder(node, neigh[0], neighbors, used_nodes)
	if isinstance(edges, list):
		for edge in edges:
			neighbors, used_nodes = neighbor_dict_builder(edge[0], edge[1], neighbors, used_nodes)

	for node in nodes:
		if node not in used_nodes:
			neighbors[node] = []

	return neighbors

##Takes a node and edge values and then returns an Erdos-Renyi graph with that number of
##nodes and edges
def erdos_renyi(n,m):
	nodes = [str(x) for x in range(1,n+1)]
	edges = []
	i=1
	while i in range(m+1):
		node_tracker = nodes[::]
		u = random.choice(nodes)
		node_tracker.remove(u)
		v = random.choice(node_tracker)
		if [u,v] not in edges and [v,u] not in edges:
			edges = edges + [[u,v]]
			i=i+1
	return nodes, edges

##Called in the barabasi() function to create new edges to add to the list edges.
def edge_maker(nodes, x):
	edges = []
	for i in range(1,x+1):
		u = random.choice(nodes)
		v = random.choice(nodes)
		while u==v or [u,v] in edges or [v,u] in edges:
			u = random.choice(nodes)
			v = random.choice(nodes)
		edges = edges + [[u,v]]
	return edges

##Computes the probability of a node degree and returns a list of all node degree probabilities
##that corresponds with the order of the nodes list given.
def deg_prop(nodes, edges, neighbors):
	node_degree_list = node_deg_finder(nodes,neighbors)
	deg_prop_list = []
	for i in range(len(nodes)):
		if node_degree_list[i]!=0:
			deg_prop_list + [nodes[i]]*node_degree_list[i]
	return deg_prop_list

##Creates a Barabasi-Albert model given the total number of nodes in the model, the number of
##times to add a new set of edges, the number of nodes at the beginning of the model, the number of edges
##at the beginning of the model, and the amount of edges that should be added during each time step.
def barabasi_albert(nodes, t, n_start, m_start, m_inc):
	random.seed(1)
	start_nodes = random.sample(nodes,n_start)
	extra_nodes = []
	for i in range(len(nodes)):
		if nodes[i] not in start_nodes:
			extra_nodes = extra_nodes + [nodes[i]]
	edges = edge_maker(nodes, t*m_inc+m_start)
	start_edges = random.sample(edges, m_start)

	final_edges = []
	for i in range(len(edges)):
		if edges[i] not in start_edges:
			final_edges.append(edges[i])

	neighbors = neighbor_finder(nodes, edges)
	for i in range(t):
		deg_prop_list = deg_prop(start_nodes, edges, neighbors)
		if extra_nodes!=[]:
			u = random.choice(extra_nodes)
			extra_nodes.remove(u)
		if deg_prop_list!=[]:
			for j in range(m_inc):
				v = random.choice(deg_prop_list)
				while [u,v] in edges or [v,u] in edges:
					v = random.choice(deg_prop_list)
				start_nodes = start_nodes + [u]
				edges = edges + [[u,v]]
	return nodes, edges

##Determines the longest connected path in a model given a specified starting node, the length of
##said path, and also returns a list of the nodes that do not need to be checked for longest 
##connected components in the future.
def BFS(nodes, edges, start_node, checked_nodes):
	info_mat = []
	new_checked_nodes = [start_node]
	max_list = new_checked_nodes[::]
	max_dis = 0
	d = {}
	for node in nodes:
		d[node]=0
	q = [start_node]
	visited = [start_node]
	while q!=[]:
		node = q[0]
		q = q[1:]
		if node in edges:
			current_neigh = edges[node][0][0]
			if current_neigh not in visited:
				q.append(current_neigh)
				visited.append(current_neigh)
				d[current_neigh]=d[node]+1
			if d[current_neigh]>max_dis:
				max_dis = d[current_neigh]
			if current_neigh not in new_checked_nodes:
				new_checked_nodes.append(current_neigh)
	return new_checked_nodes


##Continously calls BFS to find the longest connected component given a node until every node has
##appeared in a connected component. The longest is then chosen and returned along with its length.
def find_largest_cc(nodes, edges):
	checked_nodes = []
	final_nodes = nodes[::]
	lgc = []
	max_cc = 0
	while final_nodes:
		start_node = final_nodes[0]
		new_checked_nodes = BFS(nodes, edges, start_node, checked_nodes)
		for node in new_checked_nodes:
			if node in final_nodes:
				final_nodes.remove(node)
			if node not in checked_nodes:
				checked_nodes.append(node)
		if len(new_checked_nodes)>max_cc:
			max_cc = len(new_checked_nodes)-1
			lgc = new_checked_nodes
	return lgc, max_cc
