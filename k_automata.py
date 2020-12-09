#!/usr/bin/env python3


def bracket(string):
    if len(string) == 1:
        return string

    return "(" + string + ")"

class Node:
    def __init__(self, n, r, k):
        self.nxt = {}
        self.nxt_add = set()
        
        for i in range(k):
            self.add_path((r*k + i)%n, str(i))
        

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
        

def get_base(n, k):
    res = {}
    for r in range(n):
        res[r] = Node(n, r, k)
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

def split_regex(reg_str):
    prev = 0
    br = 0
    res = []

    for i in range(len(reg_str)):
        if reg_str[i] == "(":
            br += 1
        elif reg_str[i] == ")":
            br -= 1
        elif br == 0 and reg_str[i] == "|":
            res.append(reg_str[prev:i+1])
            prev = i+1
    res.append(reg_str[prev:len(reg_str)])

    return res


def remove_leading(reg_str):
    toks = split_regex(reg_str)
    del toks[0]

    res = "".join(toks)
    return "(" + bracket(res) + bracket(reg_str) + "*)|0"
        
 

def get_regex(n, k):
    aut = get_base(n, k)

    while len(aut) > 1:
        reduce(aut, select(aut))

    return "^" + bracket(remove_leading(aut[0].nxt[0])) + "$"
