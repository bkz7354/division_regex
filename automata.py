#!/usr/bin/env python3

import numpy as np
import re
import random as rnd

def bracket(string):
    if len(string) == 1:
        return string

    return "(" + string + ")"

class Node:
    def __init__(self, n, r):
        self.nxt = {}
        self.nxt_add = set()
        
        self.add_path((r*2)%n, "0")
        self.add_path((r*2+1)%n, "1")

    def add_path(self, to, e_str):
        if to in self.nxt:
            self.nxt[to] += "|" + e_str
            self.nxt_add.add(to)
        else:
            self.nxt[to] = e_str
    
    def get_edge(self, to):
        if to not in self.nxt:
            raise Exception("bad edge")
        if to in self.nxt_add:
            return bracket(self.nxt[to])
        else:
            return self.nxt[to]
        

def get_base(n):
    res = {}
    for r in range(n):
        res[r] = Node(n, r)
    return res

def get_incoming(aut, r):
    res = []

    for i in aut:
        if i == r:
            continue
        if r in aut[i].nxt:
            res.append(i)
    
    return res

def get_cycle(aut, r):
    if r in aut[r].nxt:
        return bracket(aut[r].nxt[r]) + "*"
    else:
        return ""


def reduce(aut, r):
    cycle = get_cycle(aut, r)

    for fr in get_incoming(aut, r):
        inc_s = aut[fr].get_edge(r)
        for to in aut[r].nxt:
            out_s = aut[r].get_edge(to)
            if to == r:
                continue
            aut[fr].add_path(to, inc_s + cycle + out_s) 
        del aut[fr].nxt[r]
    del aut[r]

def weight(aut, r):
    return len(get_incoming(aut, r))*len(aut[r].nxt)

def select(aut):
    res = -1

    for i in aut:
        if i == 0:
            continue
        if res == -1 or weight(aut, i) < weight(aut, res):
            res = i
    return res

def get_regex(n):
    aut = get_base(n)

    while len(aut) > 1:
        reduce(aut, select(aut))

    return "^" + bracket(aut[0].nxt[0]) + "*$"


def my_match(string, reg):
    return reg.match(string) is not None

def divisible(k, n):
    return k%n == 0

def test(n):
    regex_str = get_regex(n)
    regex = re.compile(regex_str)

    for i in range(10*n):
        div = my_match(np.base_repr(i, 2), regex)
        if div != divisible(i, n):
            print(div, i%n)
            print("test n = " + str(n) + " i = " + str(i) + " falied")
            return False

    print("test for " + str(n) + " successful")
    return True

def run_tests():
    for i in range(1, 30):
        if not test(i):
            return False
    return True


def main():
    if run_tests():
        print("tested successfully")
    
    print()
    print("regex for 5")
    print(get_regex(5))
    

if __name__ == "__main__":
    main()
