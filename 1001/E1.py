#!/usr/bin/env python
import os
import sys
from io import BytesIO, IOBase
from collections import deque, defaultdict
#from bisect import bisect_left as bl                #c++ lowerbound bl(array,element)
#from bisect import bisect_right as br               #c++ upperbound br(array,element)
class TreeNode:
    def __init__(self, data, weight=None):
        self.data = data  # Node's name (identifier)
        self.weight = weight  # Node's weight
        self.children = []  # List to store children nodes

# DFS function that checks if the target value exists in the subtree of a node with current_value (node identifier)
def dfs1(root, current_value, target):
    if root is None:
        return False
    # Check if the current node's identifier (node number) matches the current_value
    if root.data == current_value:  # Print the node's identifier and weight
        return dfs2(root, target)  # Once found, check if target exists in this node's subtree

    # If the current node isn't the one we're looking for, check its children
    for child in root.children:
        if dfs1(child, current_value, target):
            return True
    return False

# DFS to check if the target value exists in the subtree of the current node (based on weight)
def dfs2(root, target):
    # Base case: if the current node's weight matches the target
    if root.weight == target:
        return True
    # Recursively search the children of the node
    for child in root.children:
        if dfs2(child, target):
            return True
    return False

# Function to build the tree from edges and initialize the nodes with weights
def build_tree(edges, weights, root_value):
    # Creating a dictionary to represent the tree as an adjacency list
    tree = defaultdict(list)
    for u, v in edges:
        tree[u].append(v)
        tree[v].append(u)

    def dfs_build(node, parent):
        # Initialize the TreeNode with its identifier and corresponding weight
        weight = weights[node - 1]  # Assuming weights list is 0-indexed
        tree_node = TreeNode(node, weight)
        for neighbor in tree[node]:
            if neighbor != parent:
                tree_node.children.append(dfs_build(neighbor, node))
        return tree_node

    return dfs_build(root_value, None)

# Function to determine the max1 and max2 weights from the sorted weights
def max1_max2(sorted_weights):
    sorted_weights = sorted(sorted_weights, key=lambda x: x[1], reverse=True)
    max1 = sorted_weights[0][1]
    max2 = None  # Placeholder for the second-highest value

    for i in range(len(sorted_weights)):
        if sorted_weights[i][1] < max1:
            max2 = sorted_weights[i][1]
            break
    return max1, max2

# Function to find the nodes corresponding to max1 and max2 weights
def max1_max2_nodes(weights, max1, max2):
    max1_nodes = []
    max2_nodes = []
    for i, weight in enumerate(weights):
        if weight == max1:
            max1_nodes.append(i + 1)  # Node numbering starts from 1
        if weight == max2:
            max2_nodes.append(i + 1)
    return max1_nodes, max2_nodes


# Main function to run the logic
def main():
    sys.stdin = open('input.txt', 'r')
    sys.stdout = open('output.txt', 'w')
    
    for _ in range(int(input())):
        n = int(input())  # Number of nodes
        weights = list(map(int, input().split()))  # Weights of nodes

        edges = []
        for i in range(n - 1):
            x, y = map(int, input().split())
            edges.append((x, y))

        # Build the tree with the given edges and weights
        root = build_tree(edges, weights, 1)

        # Sort the nodes based on weights
        sorted_weights = [(index + 1, weight) for index, weight in enumerate(weights)]
        max1, max2 = max1_max2(sorted_weights)
        max1_nodes, max2_nodes = max1_max2_nodes(weights, max1, max2)
        flag = 1
        # Process the nodes with max2 weights to check if they have max1 in their subtree
        while max2 != -1:
            insubtree = []
            notinsubtree = []
            for node in max2_nodes:
                if dfs1(root, node, max1):
                    insubtree.append(node)
                else:
                    notinsubtree.append(node)

            if len(notinsubtree) >= 1:
                print(notinsubtree[0])
                flag = 0
                break
            elif len(insubtree) >= 2:
                print(insubtree[0])
                flag = 0
                break

            # Update max1 and max2
            for i in range(len(weights)):
                if weights[i] == max1:
                    weights[i] = -1
            
            sorted_weights = [(index + 1, weight) for index, weight in enumerate(weights)]
            max1, max2 = max1_max2(sorted_weights)
            max1_nodes, max2_nodes = max1_max2_nodes(weights, max1, max2)
        if flag:
            print(0)


#-----------------------------BOSS-------------------------------------!
# region fastio

BUFSIZE = 8192


class FastIO(IOBase):
    newlines = 0

    def __init__(self, file):
        self._fd = file.fileno()
        self.buffer = BytesIO()
        self.writable = "x" in file.mode or "r" not in file.mode
        self.write = self.buffer.write if self.writable else None

    def read(self):
        while True:
            b = os.read(self._fd, max(os.fstat(self._fd).st_size, BUFSIZE))
            if not b:
                break
            ptr = self.buffer.tell()
            self.buffer.seek(0, 2), self.buffer.write(b), self.buffer.seek(ptr)
        self.newlines = 0
        return self.buffer.read()

    def readline(self):
        while self.newlines == 0:
            b = os.read(self._fd, max(os.fstat(self._fd).st_size, BUFSIZE))
            self.newlines = b.count(b"\n") + (not b)
            ptr = self.buffer.tell()
            self.buffer.seek(0, 2), self.buffer.write(b), self.buffer.seek(ptr)
        self.newlines -= 1
        return self.buffer.readline()

    def flush(self):
        if self.writable:
            os.write(self._fd, self.buffer.getvalue())
            self.buffer.truncate(0), self.buffer.seek(0)


class IOWrapper(IOBase):
    def __init__(self, file):
        self.buffer = FastIO(file)
        self.flush = self.buffer.flush
        self.writable = self.buffer.writable
        self.write = lambda s: self.buffer.write(s.encode("ascii"))
        self.read = lambda: self.buffer.read().decode("ascii")
        self.readline = lambda: self.buffer.readline().decode("ascii")


sys.stdin, sys.stdout = IOWrapper(sys.stdin), IOWrapper(sys.stdout)
input = lambda: sys.stdin.readline().rstrip("\r\n")

# endregion

if __name__ == "__main__":
    main()