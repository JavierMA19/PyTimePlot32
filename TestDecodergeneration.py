# -*- coding: utf-8 -*-
"""
Created on Tue Sep  1 12:47:03 2020

@author: Javier
"""
import numpy as np

DOChannels = ['port0/line10:15', ]
InitSwitch = np.array([0, 1, 0, 0, 0, 0, 0, 0, 0, 0], dtype=np.uint8)

DigColumns = ['Col07', 'Col26']

def truthtable(n):
    if n < 1:
        return[[]]
    subtable = truthtable(n-1)
    return [row+[v] for row in subtable for v in [0,1]]

Decoder = truthtable(5)
Dec = np.array(Decoder, dtype=np.uint8)

Dict32 = {}

Dict32 = {'Col01': None,
          'Col02': None,
          'Col03': None,
          'Col04': None,
          'Col05': None,
          'Col06': None,
          'Col07': None,
          'Col08': None,
          'Col09': None,
          'Col10': None,
          'Col11': None,
          'Col12': None,
          'Col13': None,
          'Col14': None,
          'Col15': None,
          'Col16': None,
          'Col17': None,
          'Col18': None,
          'Col19': None,
          'Col20': None,
          'Col21': None,
          'Col22': None,
          'Col23': None,
          'Col24': None,
          'Col25': None,
          'Col26': None,
          'Col27': None,
          'Col28': None,
          'Col29': None,
          'Col30': None,
          'Col31': None,
          'Col32': None,
    }

DecDigital = {}
DOut = np.array([], dtype=np.bool)
index = 0
digInd = 0
for n, i in Dict32.items():
    if n in DigColumns:
        print(n)
        Dict32[n] = (Dec[index], index)
        DecDigital[digInd] = Dec[index]
        Cout = Dec[index]
        DOut = np.vstack((DOut, Cout)) if DOut.size else Cout

        digInd += 1
    index += 1


