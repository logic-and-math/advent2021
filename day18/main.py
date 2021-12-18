import os
from pathlib import Path
import math

class Node:
    left = None
    right = None
    value = None
    parent = None

def read_number(line):
    root = Node()
    node = root

    for c in line:
        if c == '[':
            new_node = Node()
            node.left = new_node
            new_node.parent = node
            node = new_node
        elif c == ']':
            node = node.parent
        elif c == ',':
            new_node = Node()
            node.right = new_node
            new_node.parent = node
            node = new_node
        else:
            node.value = int(c)
            node = node.parent

    return root

def get_node_to_explode(node, level):
    if level == 4:
        return node if node.value is None else None

    if node.left is not None:
        ret_node = get_node_to_explode(node.left, level + 1)
        if ret_node is not None:
            return ret_node

    if node.right is not None:
        ret_node = get_node_to_explode(node.right, level + 1)
        if ret_node is not None:
            return ret_node

    return None

def get_nodes(node, nodes):
    nodes.append(node)
    if node.value is not None:
        return     
    get_nodes(node.left, nodes)
    get_nodes(node.right, nodes)


def explode(root):
    n_explosions = 0
    while True:
        nodes = []
        get_nodes(root, nodes)

        node_to_explode = get_node_to_explode(root, 0)
        if node_to_explode is None:
            return n_explosions

        loc = nodes.index(node_to_explode)
        left = [n for n in nodes[:loc] if n.value is not None]
        if len(left) > 0:
            left[-1].value += node_to_explode.left.value

        if loc + 3 < len(nodes): #if its not the last node
            right = [n for n in nodes[loc+3:] if n.value is not None]
            if len(right) > 0:
                right[0].value += node_to_explode.right.value

        node_to_explode.value = 0
        node_to_explode.left = None
        node_to_explode.right = None
        n_explosions += 1


def split(root):
    nodes = []
    get_nodes(root, nodes)
    nodes_to_split = [n for n in nodes if n.value is not None and n.value >= 10]
    if len(nodes_to_split) > 0:
        node_to_split = nodes_to_split[0]

        node_to_split.left = Node()
        node_to_split.left.parent = node_to_split
        node_to_split.left.value = math.floor(node_to_split.value / 2)


        node_to_split.right = Node()
        node_to_split.right.parent = node_to_split
        node_to_split.right.value = math.ceil(node_to_split.value / 2)

        node_to_split.value = None
        return 1
    return 0


def add(root1, root2):
    root = Node()
    root.left = root1
    root.right = root2
    return root


def magnitude(node):
    if node.value is not None:
        return node.value
    
    m = 3 * magnitude(node.left) + 2 * magnitude(node.right)
    return m


def full_addition(root1, root2):
    root = add(root1, root2)
    while True:
        n_explosions = explode(root)
        n_splits = split(root)
        if n_explosions == 0 and n_splits == 0:
            break
    return root

def copy_tree(root):
    nodes = []
    get_nodes(root, nodes)
    node_to_new_node = {n: Node() for n in nodes}
    for (old, new) in node_to_new_node.items():
        new: Node
        new.left = node_to_new_node[old.left] if old.left is not None else None
        new.right = node_to_new_node[old.right] if old.right is not None else None
        new.parent = node_to_new_node[old.parent] if old.parent is not None else None
        new.value = old.value
    
    return node_to_new_node[root]

def print_tree(root):
    nodes = []
    get_nodes(root, nodes)
    vals = [n.value for n in nodes if n.value is not None]
    print(vals)

input_p = Path(os.getcwd()) / 'input'
text = input_p.read_text()
lines = text.splitlines()

def part_1(lines):
    numbers = [read_number(line) for line in lines]
    root = numbers[0]
    for root2 in numbers[1:]:
        root = full_addition(root, root2)

    print(magnitude(root))

def part_2(lines):
    og_numbers = [read_number(line) for line in lines]
    numbers = [copy_tree(r) for r in og_numbers]

    import itertools
    combinations = itertools.permutations(range(len(lines)), 2)

    results = []
    for (i,j) in combinations:
        results.append(full_addition(numbers[i], numbers[j]))
        #replace the two trees on which i worked
        numbers[i] = copy_tree(og_numbers[i])
        numbers[j] = copy_tree(og_numbers[j])

    magnitudes = [magnitude(r) for r in results]
    print(max(magnitudes))

part_1(lines)
part_2(lines)