import networkx as nx
import matplotlib.pyplot as plt

INFINITY = 1000

def read_input_file():
    path = input("Enter full path of file: ")
    with open(path, "r") as f:
        lines = f.readlines()
        f.close()
    split_lines = [line.replace('\n', '').split(',') for line in lines]
    for line in split_lines[1:]:
        line[2] = {'weight': int(line[2])}
    split_lines = [tuple(line) for line in split_lines]
    return int(split_lines[0][0]), int(split_lines[0][1]), {line[0] for line in split_lines[1:]} | {line[1] for line in split_lines[1:]}, split_lines[1:]

def display_forwarding_table(current_node, shortest_path_table):
    links = {}
    for node in shortest_path_table:
        if node == current_node:
            continue
        check_node = node
        while True:
            if shortest_path_table[check_node][1] == current_node:
                links.update({node: (current_node, check_node)})
                break
            else:
                check_node = shortest_path_table[check_node][1]
    
    print("\nForwarding table for node: " + str(current_node))
    print("+++++++++++++++++++++++++++")
    print("| Destination |    Link   |")
    print("+++++++++++++++++++++++++++")
    for node in shortest_path_table:
        if node == current_node:
            continue
        print("\t" + str(node) + "\t" + str(links[node]))
    print("+++++++++++++++++++++++++++")

def present_shortest_path_table(shortest_path_table):
    print("\nShortest Path Table:")
    print("++++++++++++++++++++++++++++++++++++++++++++++")
    print("|  node  | Shortest Distance | Previous Node |")
    print("++++++++++++++++++++++++++++++++++++++++++++++")
    for node in shortest_path_table:
        print("    " + str(node) + "\t\t   " + str(shortest_path_table[node][0]) + "\t\t   " + str(shortest_path_table[node][1]))
    print("++++++++++++++++++++++++++++++++++++++++++++++")

def draw(graph):
    pos = nx.spring_layout(graph, seed=7)
    nx.draw_networkx_nodes(graph, pos, node_size=700)
    nx.draw_networkx_edges(graph, pos, width=6)
    nx.draw_networkx_edges(graph, pos, width=6, alpha=0.5, edge_color="b", style="dashed")
    nx.draw_networkx_labels(graph, pos, font_size=20, font_family="sans-serif")
    edge_labels = nx.get_edge_attributes(graph, "weight")
    nx.draw_networkx_edge_labels(graph, pos, edge_labels)
    ax = plt.gca()
    ax.margins(0.08)
    plt.axis("off")
    plt.tight_layout()
    plt.show()

def create_graph(edges):
    graph = nx.Graph()
    graph.add_edges_from(edges)
    draw(graph)
    return graph

def find_partial_match(edges, edge):
    for i in range(len(edges)):
        if (edges[i][0] == edge[0] and edges[i][1] == edge[1]) or (edges[i][0] == edge[1] and edges[i][1] == edge[0]):
            return edges[i]

def create_shortest_path_graph(table, edges, source):
    new_edges = []
    for node in table:
        if node == source:
            continue
        new_edges.append(find_partial_match(edges, (table[node][1], node)))
    create_graph(new_edges)

def minimum_distance_node(unvisited_nodes, shortest_path_table):
    min = unvisited_nodes[0]
    for node in unvisited_nodes:
        if shortest_path_table[node][0] < shortest_path_table[min][0]:
            min = node
    return min

def dijkstra(graph, source):
    visited_nodes = []
    unvisited_nodes = list(graph.nodes)
    shortest_path_table = {node:[INFINITY, None] for node in graph.nodes}
    shortest_path_table[source][0] = 0
    
    while len(unvisited_nodes):
        current_node = minimum_distance_node(unvisited_nodes, shortest_path_table)

        for neighbor in graph[current_node]:
            if shortest_path_table[neighbor][0] > shortest_path_table[current_node][0] + graph[current_node][neighbor]['weight'] and neighbor in unvisited_nodes:
                shortest_path_table[neighbor][0] = shortest_path_table[current_node][0] + graph[current_node][neighbor]['weight']
                shortest_path_table[neighbor][1] = current_node

        visited_nodes.append(current_node)
        unvisited_nodes.remove(current_node)
    
    return shortest_path_table

if __name__ == "__main__":
    n, m, nodes, edges = read_input_file()
    
    if n != len(nodes) or m != len(edges):
        print("Data is not consistent!")
    else:
        graph = create_graph(edges)
        for node in graph.nodes:
            shortest_path_table = dijkstra(graph, node)
            display_forwarding_table(node, shortest_path_table)
            present_shortest_path_table(shortest_path_table)
            create_shortest_path_graph(shortest_path_table, edges, node)