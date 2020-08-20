# -*- coding: utf-8 -*-
"""
Created on Mon Jul 20 19:32:31 2020

@author: Administrator
"""
import fileinput
filename = 'data.txt'

for line in fileinput.FileInput(filename, inplace=1):
    print(line.replace('[', '')),
    
#for line in fileinput.FileInput(filename, inplace=1):
#    line.replace(']', '')
#    
#for line in fileinput.FileInput(filename, inplace=1):
#    line.replace('(', '')
#    
#for line in fileinput.FileInput(filename, inplace=1):
#    line.replace(')', '')
#    
#for line in fileinput.FileInput(filename, inplace=1):
#    line.replace('))', '')
#            
#for line in fileinput.FileInput(filename, inplace=1):
#    line.replace(',', '')
#        
#for line in fileinput.FileInput(filename, inplace=1):
#    line.replace('L', '')