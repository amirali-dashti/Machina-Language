import numpy as np


class GNFADefine:
    def __init__(self, states):
        self.states = states
        self.table = Q
        
    def gUpdate(self, q1, q2, val):
        self.table[q1, q2] = val
        
    def gReturn(self):
        print(self.table)