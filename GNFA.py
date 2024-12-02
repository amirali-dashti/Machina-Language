import numpy as np


class GNFA:
    def __init__(self, Q, qs, qa):
        self.Q = Q
        self.qs = qs
        self.qa = qa
        self.table = np.full((self.Q, self.Q), "n", dtype=object)
        
    def gUpdate(self, q1, q2, val):
        self.table[q1, q2] = val

aGNFA = GNFA(5, 1, 5)

aGNFA.gUpdate(1, 3, "aab")


for row in aGNFA.table:
    print(row)
