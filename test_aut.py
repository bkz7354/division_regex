#!/usr/bin/env python3

import automata as aut
import numpy as np
import re
import random as rnd

def my_match(string, reg):
    return reg.match(string) is not None

def divisible(k, n):
    return k%n == 0

def test_recognition(n):
    regex_str = aut.get_regex(n)
    regex = re.compile(regex_str)

    for i in range(10*n):
        if my_match(np.base_repr(i, 2), regex) != divisible(i, n):
            raise Exception("recognition test n = " + str(n) + " i = " + str(i) + " falied")
            

def test_leading(n):
    regex_str = aut.get_regex(n)
    regex = re.compile(regex_str)

    n_str = np.base_repr(n, 2)
    n_str = "000" + n_str

    if my_match(n_str, regex):
        raise Exception("leading zero test for " + str(n) + " failed")

def run_tests(n):
    for i in range(1, n):
        test_recognition(i)  

    for i in range(1, n):
        test_leading(i)
    


def main():
    try: 
        run_tests(25)
    except Exception as e:
        print(e)
    else:
        print("tested successfully")
    
    test_leading(10)
    print()

    print("regex for 5")
    print(aut.get_regex(5))
    

if __name__ == "__main__":
    main()
