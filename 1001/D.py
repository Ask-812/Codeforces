#!/usr/bin/env python
import os
import sys
from io import BytesIO, IOBase
from collections import defaultdict, deque
sys.setrecursionlimit(10**6)



def find_optimal_move(n, weights, edges):
    max1 = max(weights)
    
    adj_list = [[] for _ in range(n+1)]
    for u, v in edges:
        adj_list[u].append(v)
        adj_list[v].append(u)
    
    def dfs(node, parent):
        max_child = 0
        for child in adj_list[node]:
            if child != parent:
                max_child = max(max_child, dfs(child, node))
        return max(max_child, weights[node-1])
    
    for i in range(1, n+1):
        if weights[i-1] == max1:
            all_smaller = True
            for child in adj_list[i]:
                if dfs(child, i) >= max1:
                    all_smaller = False
                    break
            if all_smaller:
                return i
    
    return 0

def solve_test_case():
    n = int(input())
    weights = list(map(int, input().split()))
    edges = [list(map(int, input().split())) for _ in range(n-1)]
    return find_optimal_move(n, weights, edges)


def solve():
    t = int(input())
    for _ in range(t):
        print(solve_test_case())

def main():
    sys.stdin = open('input.txt', 'r')
    sys.stdout = open('output.txt', 'w')
    solve()


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