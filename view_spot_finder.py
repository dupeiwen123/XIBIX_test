import json
import sys
import time
import numpy as np

class Node:
    def __init__(self, id, x, y):
        self.id = id
        self.x = x
        self.y = y

class Element:
    def __init__(self, id, nodes):
        self.id = id
        self.nodes = nodes
class Mesh:
    def __init__(self, nodes, elements, values):
        self.nodes = nodes
        self.elements = elements
        self.values = values

def read_mesh_file(filename):
    with open(filename, 'r') as f:
        mesh_data = json.load(f)
    nodes = np.array([Node(node['id'], node['x'], node['y']) for node in mesh_data['nodes']])
    elements = np.array([Element(elem['id'], elem['nodes']) for elem in mesh_data['elements']])
    values = {val['element_id']: val['value'] for val in mesh_data['values']}

    mesh = Mesh(nodes, elements, values)
    return mesh


# find the neighbors for each element
def get_neighbors(mesh):
    # dict{node_id: elements}
    node_elems = {}
    for node in mesh.nodes:
        node_elems[node.id] = []
    for elem in mesh.elements:
        for node_id in elem.nodes:
            if node_id not in node_elems:
                node_elems[node_id] = []
            node_elems[node_id].append(elem.id)

    # Compute the neighbors of each element through the previously defined dict
    neighbors = {}
    for elem in mesh.elements:
        neighbors[elem.id] = []
        for node_id in elem.nodes:
            if node_id in node_elems:
                neighbors[elem.id].append(node_elems[node_id])
                
        neighbors[elem.id] = np.unique(np.concatenate(neighbors[elem.id]))       
    return neighbors


def find_view_spots(mesh, N):
    view_spots = []
    neighbors = get_neighbors(mesh)
    view_spots = []

    for elem in mesh.elements:
        if mesh.values[elem.id] >= np.max([mesh.values[n] for n in neighbors[elem.id].astype(int)]):
            view_spots.append({'element_id': elem.id, 'value': mesh.values[elem.id]})
            
    # Sort view_spots by height value in descending order
    view_spots_arr = np.array([spot['value'] for spot in view_spots])
    sorted_indexes = np.argsort(-view_spots_arr)
    sorted_view_spots = [view_spots[i] for i in sorted_indexes]
   
    # Return the first N view spots
    return sorted_view_spots[:N]

if __name__ == '__main__':
    # Read mesh file and N from command-line arguments
    mesh_file = sys.argv[1]
    mesh = read_mesh_file(mesh_file)
    N = int(sys.argv[2])
    view_spots = find_view_spots(mesh, N)
    print(view_spots)