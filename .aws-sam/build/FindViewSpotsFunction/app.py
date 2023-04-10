import json
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

    nodes = [Node(node['id'], node['x'], node['y']) for node in mesh_data['nodes']]
    elements = [Element(elem['id'], elem['nodes']) for elem in mesh_data['elements']]
    values = {val['element_id']: val['value'] for val in mesh_data['values']}

    mesh = Mesh(nodes, elements, values)
    return mesh
mesh = read_mesh_file('mesh[1][1][1][1][1][1].json')

# two elements as neighbors if they share at least one node
# include elem itself
def get_neighbors(mesh, elem):

    neighbor = []

    for other_elem in mesh.elements:
        shared_nodes = set(elem.nodes).intersection(set(other_elem.nodes))
        if len(shared_nodes) > 0:
            neighbor.append(other_elem)

    return neighbor

neighbors = get_neighbors(mesh, mesh.elements[0])
# print(neighbors)

def find_view_spots(mesh, N):
    view_spots = []
    # Iterate over all elements in the mesh
    for elem in mesh.elements:

        # Check if the element is a local maximum
        is_local_max = True
        for neighbor in get_neighbors(mesh, elem):
            if mesh.values[neighbor.id]  > mesh.values[elem.id]:
                is_local_max = False
                break

        # If the element is a local maximum, add it to the list of view spots
        if is_local_max:
            view_spots.append({'element_id': elem.id, 'value': mesh.values[elem.id]})

    # Sort the view spots by height value in descending order
    view_spots.sort(key=lambda spot: spot['value'], reverse=True)

    # Return the first N view spots
    return view_spots[:N]
print(find_view_spots(mesh,5))