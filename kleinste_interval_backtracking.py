import time

import pandas as pd
import numpy as np

# df = pd.read_excel('getrimde_lijsten.xlsx', index_col=0)
#
# FPR_getrimt = df['FPR']
# TPR_getrimt = df['TPR']
# threshold_getrimt = df['threshold_getrimt']

# Read the text file back into a NumPy array
FPR_getrimt = np.loadtxt('FPR_getrimt.txt', delimiter=' ')
TPR_getrimt = np.loadtxt('TPR_getrimt.txt', delimiter=' ')
threshold_getrimt = np.loadtxt('threshold_getrimt.txt', delimiter=' ')

# start = time.perf_counter()
# print("FPR", FPR)
# stop = time.perf_counter()
# print("TPR", TPR)
# print("threshold", threshold)
# print("tijd:", stop - start)

ACCEPT = "accept"
CONTINUE = "continue"
ABANDON = "abandon"

def trim(lijst1, goede_elementen):
    '''
    Trimt de lijst, zodat enkel de 'goede' elementen overblijven
    :param lijst1:
    :param goede_elementen:
    :return:
    '''
    nieuwe_lijst = []
    for k in goede_elementen:
        nieuwe_lijst.extend([lijst1[k]])
    return nieuwe_lijst


def likelihood_helper(FPR, TPR, start_idx, eind_idx):
    delta2 = TPR[eind_idx] - TPR[start_idx]
    delta1 = FPR[eind_idx] - FPR[start_idx]
    return delta2 / delta1

# TESTS
# likelihood_helper(FPR_getrimt, TPR_getrimt, 1, 2)
# print("1, 2", likelihood_helper(FPR_getrimt, TPR_getrimt, 1, 2))
# print("3, 4", likelihood_helper(FPR_getrimt, TPR_getrimt, 3, 4))
# print("10, 11", likelihood_helper(FPR_getrimt, TPR_getrimt, 10, 11))
# print("1, 15", likelihood_helper(FPR_getrimt, TPR_getrimt, 1, 15))

def extend(partial_solution, FPR, TPR, n, likelihood):
    ext_sol = []
    a = partial_solution[-1]
    for getal in range(partial_solution[-1] + 1,n):
        if likelihood_helper(FPR, TPR, a, getal) < likelihood: # als de likelihood afneemt
            new_sol = partial_solution + [getal]
            ext_sol.append(new_sol)
    return ext_sol

def examine(partial_solution, n):
    if partial_solution[-1] == n - 1:
        return ACCEPT
    return CONTINUE

def solve(partial_solution, FPR, TPR):
    assert len(FPR) == len(TPR)
    n = len(FPR)
    best_sol = []
    exam = examine(partial_solution, n)
    if exam == ACCEPT:
        return partial_solution
    if exam == CONTINUE:
        if len(partial_solution) == 1:
            likelihood = float('inf')
        else:
            likelihood = likelihood_helper(FPR, TPR, partial_solution[-2], partial_solution[-1])
        ext_sol = extend(partial_solution, FPR, TPR, n, likelihood)
        for new_sol in ext_sol:
            recurs_sol = solve(new_sol, FPR, TPR)
            if len(recurs_sol) > len(best_sol):
                best_sol = recurs_sol
        return best_sol

def verdeling(FPR, TPR):
    partial_solution = [0]
    return solve(partial_solution, FPR, TPR)

verd_20 = verdeling(FPR_getrimt, TPR_getrimt)
print("indices:", verd_20)

def bereken_likelihood(FPR, TPR):
    likelihood_lijst = []
    verd = verdeling(FPR, TPR)
    for i in range(len(verd) - 1):
        LR = likelihood_helper(FPR, TPR, verd[i], verd[i + 1])
        likelihood_lijst += [LR]
    return likelihood_lijst

LR_20 = bereken_likelihood(FPR_getrimt, TPR_getrimt)
print("LR:", LR_20)


thresh_20 = trim(threshold_getrimt, verd_20)
print("thresh", thresh_20)

'''
Kies de oplossing waarbij het laaste interval de laagste likelihood-ratio heeft.
    1. zoek alle oplossingen 
    2. selecteer de beste
'''

#####################
# PLOT              #
#####################

# import matplotlib.pyplot as plt
# import numpy as np
# 
# x = thresh_20[1:]
# y = LR_20
# 
# fig, ax = plt.subplots()
# ax.plot(x, y, 'o')
# ax.set_xlabel("Threshold")
# ax.set_ylabel("LR")
# plt.show()

