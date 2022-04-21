
import numpy as np # Guardar en arreglos
import os

class Node:
    def __init__(self, node_no, data, parent, act, cost):
        self.data = data
        self.parent = parent
        self.act = act
        self.node_no = node_no
        self.cost = cost


def get_initial():
    print("Digite un número del 1 al 8,sin repetir")
    initial_state = np.zeros(9)
    for i in range(9):
            states = int(input("Ingrese " + str(i + 1) + " numero: "))

            if states < 0 or states > 8:
                print("Solo ingrese [0-8]")
                exit(0)
            else:
                initial_state[i] = np.array(states)
    return np.reshape(initial_state, (3, 3))


def find_index(puzzle):
    i, j = np.where(puzzle == 0)
    i = int(i)
    j = int(j)
    return i, j


def move_left(data):
    i, j = find_index(data)
    if j == 0:
        return None
    else:
        temp_arr = np.copy(data)
        temp = temp_arr[i, j - 1]

        temp_arr[i, j] = temp

        temp_arr[i, j - 1] = 0
        return temp_arr


def move_right(data):
    i, j = find_index(data)
    if j == 2:

        return None
    else:
        temp_arr = np.copy(data)
        temp = temp_arr[i, j + 1]
        temp_arr[i, j] = temp
        temp_arr[i, j + 1] = 0
        return temp_arr


def move_up(data):
    i, j = find_index(data)
    if i == 0:
        return None
    else:

        temp_arr = np.copy(data)
        temp = temp_arr[i - 1, j]
        temp_arr[i, j] = temp
        temp_arr[i - 1, j] = 0
        return temp_arr


def move_down(data):

    i, j = find_index(data)
    if i == 2:
        return None
    else:
        temp_arr = np.copy(data)
        temp = temp_arr[i + 1, j]
        temp_arr[i, j] = temp

        temp_arr[i + 1, j] = 0
        return temp_arr


def move_tile(action, data):
    if action == 'up':
        return move_up(data)
    if action == 'down':
        return move_down(data)
    if action == 'left':
        return move_left(data)
    if action == 'right':
        return move_right(data)
    else:

        return None


def print_states(list_final): # Ultimas etapas printeadas
    print("printing final solution")
    for l in list_final:

        print("Move : " + str(l.act) + "\n" + "Result : " + "\n" + str(l.data) + "\t" + "node number:" + str(l.node_no))


def write_path(path_formed): # Para escribir el camino final if os.path.exists("Path_file.txt"):
    if os.path.exists("Path_file.txt"):
        os.remove("Path_file.txt")

    f = open("Path_file.txt", "a")
    for node in path_formed:
        if node.parent is not None:
            f.write(str(node.node_no) + "\t" + str(node.parent.node_no) + "\t" + str(node.cost) + "\n")
    f.close()


def write_node_explored(explored): # Todos los nodos escritos if os.path.exists("Nodes.txt"):
   if os.path.exists("Nodes.txt"): 
    os.remove("Nodes.txt")

    f = open("Nodes.txt", "a")
    for element in explored:
        f.write('[')
        for i in range(len(element)):
            for j in range(len(element)):
                f.write(str(element[j][i]) + " ")
        f.write(']')
        f.write("\n")
    f.close()


def write_node_info(visited):
    if os.path.exists("Node_info.txt"):
        os.remove("Node_info.txt")

    f = open("Node_info.txt", "a")
    for n in visited:
        if n.parent is not None:

            f.write(str(n.node_no) + "\t" + str(n.parent.node_no) + "\t" + str(n.cost) + "\n")
    f.close()


def path(node): #Buscar el nodo meta
    p = []
    p.append(node)

    parent_node = node.parent
    while parent_node is not None:
        p.append(parent_node)
        parent_node = parent_node.parent
    return list(reversed(p))


def exploring_nodes(node):
    print("...")
    actions = ["down", "up", "left", "right"]
    goal_node = np.array([[1, 2, 3], [4, 5, 6], [7, 8, 0]])
    node_q = [node]
    final_nodes = []
    visited = []
    final_nodes.append(node_q[0].data.tolist())

    node_counter = 0 # un id especifico para nodos

    while node_q:

        current_root = node_q.pop(0) # Pop al elemento que esta al principio de la lista 
        if current_root.data.tolist() == goal_node.tolist():
            print("objetivo alcanzado!")
            return current_root, final_nodes, visited

        for move in actions:
            temp_data = move_tile(move, current_root.data)
            if temp_data is not None:
                node_counter += 1

                child_node = Node(node_counter, np.array(temp_data), current_root, move, 0) # Crear el nodo hijo
                if child_node.data.tolist() not in final_nodes: # añadir al final de la lista
                    node_q.append(child_node)
                    final_nodes.append(child_node.data.tolist())
                    visited.append(child_node)
                    if child_node.data.tolist() == goal_node.tolist():
                        print("Goal_reached")
                        return child_node, final_nodes, visited

    return None, None, None # devolver si no se logro

def check_correct_input(l):
    array = np.reshape(l, 9)
    for i in range(9):
        counter_appear = 0

        f = array[i]
        for j in range(9):
            if f == array[j]:
                counter_appear += 1
            if counter_appear >= 2:
                print("numero repetido")
                exit(0)


def check_solvable(g):
    arr = np.reshape(g, 9)
    counter_states = 0
    for i in range(9):
        if not arr[i] == 0:
         check_elem = arr[i]

        for x in range(i + 1, 9):
            if check_elem < arr[x] or arr[x] == 0:
                continue
            else:
                    counter_states += 1
    if counter_states % 2 == 0:
        print("El rompecabezas tiene solución")

    else:
        print("No tiene solucion")
