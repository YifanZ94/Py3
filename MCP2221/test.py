# -*- coding: utf-8 -*-
"""
Created on Thu Oct 15 15:25:20 2020

@author: Administrator
"""

def add(a,b):
    s = a + b
    return s

class operates():
    
    def __init__(self):
        print('give a')
        self.a = int(input())
        print('give b')
        self.b = int(input())
        
    def do_add(self):
        self.s = add(self.a, self.b)
        return self.s
    
subject = operates()
print(subject.do_add())