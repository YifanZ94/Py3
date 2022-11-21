# -*- coding: utf-8 -*-
"""
Created on Tue Sep 13 11:48:56 2022

@author: Administrator
"""

import argparse
parser = argparse.ArgumentParser()
# parser.add_argument("square", type=int,
#                     help="display a square of a given number")
parser.add_argument("-v", "--verbose",
                    help="increase output verbosity", type=int)
args = parser.parse_args()
answer = args.verbose**2
if args.verbose:
    print(f"the square of {args.verbose} equals {answer}")
else:
    print(answer)