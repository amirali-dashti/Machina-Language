import numpy as np


class GNFADefine:
    def __init__(self, Q):
        self.qCount = len(Q)
        self.table = Q
        
    def gUpdate(self, q1, q2, val):
        self.table[q1, q2] = val
        
    def gReturn(self):
        print(self.table)