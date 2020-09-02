# -*- coding: utf-8 -*-
"""
Created on Tue Sep  1 12:47:03 2020

@author: Javier
"""
import numpy as np

DOChannels = ['port0/line0:15', ]
InitSwitch = np.array([0, 1, 0, 0, 0, 0, 0, 0, 0, 0], dtype=np.uint8)

def truthtable(n):
    if n < 1:
        return[[]]
    subtable = truthtable(n-1)
    return [row+[v] for row in subtable for v in [0,1]]

Decoder = truthtable(5)
Dec = np.array([Decoder[0]], dtype=np.uint8)

