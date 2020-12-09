#!/usr/bin/env python3

import k_automata as aut
import numpy as np
import re
import random as rnd

def my_match(string, reg):
    return reg.match(string) is not None

def divisible(k, n):
    return k%n == 0

def test_recognition(n, k):
    regex_str = aut.get_regex(n, k)
    regex = re.compile(regex_str)

    for i in range(10*n):
        if my_match(np.base_repr(i, k), regex) != divisible(i, n):
            raise Exception("recognition test n = " + str(n) + ", i = " + str(i) + " falied")
            

def test_leading(n, k):
    regex_str = aut.get_regex(n, k)
    regex = re.compile(regex_str)

    n_str = np.base_repr(n, k)
    n_str = "000" + n_str

    if my_match(n_str, regex):
        raise Exception("leading zero test for " + str(n) + " failed")

def run_tests(n, k):
    for i in range(1, n):
        test_recognition(i, k)  

    for i in range(1, n):
        test_leading(i, k)
    


def main():
    test_k = [2, 3, 4, 5, 6, 7]

    for i in test_k:
        print("testing k = ", i, '-', end=' ')
        try: 
            run_tests(10, i)
            test_leading(10, i)
        except Exception as e:
            print(e)
        else:
            print("OK")

    print()
    print("Example regex for n = 5, k = 2")
    print(aut.get_regex(5, 2))


if __name__ == "__main__":
    main()
