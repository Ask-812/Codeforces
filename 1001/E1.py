#!/usr/bin/env python
import os
import sys
from io import BytesIO, IOBase
from collections import deque, defaultdict
#from bisect import bisect_left as bl                #c++ lowerbound bl(array,element)
#from bisect import bisect_right as br               #c++ upperbound br(array,element)


# TreeNode class to represent each node in the tree
class TreeNode:
    def __init__(self, data):
        self.data = data
        self.children = []

# Build the tree from the edges
def build_tree(edges, root_value):
    tree = defaultdict(list)
    for u, v in edges:
        tree[u].append(v)
        tree[v].append(u)

    def dfs_build(node, parent):
        tree_node = TreeNode(node)
        for neighbor in tree[node]:
            if neighbor != parent:
                tree_node.children.append(dfs_build(neighbor, node))
        return tree_node

    return dfs_build(root_value, None)

# Function to get the first and second largest weights
def max1_max2(sorted_weights):
    sorted_weights = sorted(sorted_weights, key=lambda x: x[1], reverse=True)
    max1 = sorted_weights[0][1]
    max2 = None  # Placeholder for second-highest value

    for i in range(len(sorted_weights)):
        if sorted_weights[i][1] < max1:
            max2 = sorted_weights[i][1]
            break
    return max1, max2

# Get the nodes corresponding to max1 and max2 values
def max1_max2_nodes(weights, max1, max2):
    max1_nodes = []
    max2_nodes = []
    for i, weight in enumerate(weights):
        if weight == max1:
            max1_nodes.append(i + 1)  # 1-indexed
        if weight == max2:
            max2_nodes.append(i + 1)  # 1-indexed
    return max1_nodes, max2_nodes

# DFS to check if the target exists in the subtree of the node with current_value
def dfs1(root, current_value, target):
    if root is None:
        return False
    if root.data == current_value:
        return dfs2(root, target)

    for child in root.children:
        if dfs2(child, current_value):
            return True
    return False

# DFS to check if target exists in the subtree
def dfs2(root, target):
    if root.data == target:
        return True
    for child in root.children:
        if dfs2(child, target):
            return True
    return False

# Main function for processing input/output
def main():
    import sys
    sys.stdin = open('input.txt', 'r')
    sys.stdout = open('output.txt', 'w')

    for _ in range(int(input())):
        n = int(input())
        weights = list(map(int, input().split()))

        edges = []
        for i in range(n - 1):
            x, y = map(int, input().split())
            edges.append((x, y))

        root = build_tree(edges, 1)
        sorted_weights = [(index + 1, weight) for index, weight in enumerate(weights)]
        max1, max2 = max1_max2(sorted_weights)
        max1_nodes, max2_nodes = max1_max2_nodes(weights, max1, max2)

        while max2 is not None:
            insubtree = []
            notinsubtree = []

            # Check if max2_nodes are in the subtree of max1_nodes
            for node in max2_nodes:
                if dfs1(root, node, max1):
                    insubtree.append(node)
                else:
                    notinsubtree.append(node)

            if len(notinsubtree) >= 1:
                print(notinsubtree[0])  # Output the first not-insubtree node
                break
            elif len(insubtree) >= 2:
                print(insubtree[0])  # Output the first insubtree node
                break

            # Mark all max1 weights as processed
            for i in range(len(weights)):
                if weights[i] == max1:
                    weights[i] = -1

            # Update max1, max2 based on new weights
            max1, max2 = max1_max2(sorted_weights)
            max1_nodes, max2_nodes = max1_max2_nodes(weights, max1, max2)


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