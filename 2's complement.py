# -*- coding: utf-8 -*-
"""
Created on Thu Jan 14 16:21:29 2021

@author: Administrator
"""

unsign_str = '0000000000101011'
ordi = len(unsign_str)

unsign = int(unsign_str,2)

if unsign < 2**(ordi-1):
    # signed = -(2**order - int(raw[6:],2))
    print('+')
    signed = unsign
else:
    print('-')
    signed = -(2**ordi - unsign)