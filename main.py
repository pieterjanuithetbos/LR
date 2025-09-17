import pandas as pd
import time
import numpy as np

#################
# TPR is y-as   #
# FPR is x-as   #
#################

# VUL IN
naam = 'BioFlash tTG'
b1 = 8
# b2 = 11
# b3 = 11

# gebruik index_col=0 om de ID's van de rijen zoals weergegeven in excel te gebruiken
# LEES EXCEL
df = pd.read_excel('input_derde_versie_tTG.xlsx', sheet_name=naam, index_col=0)

FPR = df['FPR']
TPR = df['TPR']
threshold = df['threshold']

# Save the NumPy array to a text file with space as the delimiter
# np.savetxt('FPR.txt', FPR, delimiter=' ')
# np.savetxt('TPR.txt', TPR, delimiter=' ')
# np.savetxt('threshold.txt', threshold, delimiter=' ')

######################
# DATA TRIMMEN       #
######################

def index_machine(lijst):
    '''
    Geeft een lijst terug met op elke positie de index van het laatst voorgekomen unieke element in de opgegeven lijst.
    :param lijst: een lijst getallen waar dubbels in staan
    :return indices, x-as: de indices van alle eerste voorkomens van unieke elementen, het gemiddelde van die indices
    '''
    indices = [0]  # initialiseer de indices-lijst
    n = len(lijst)
    i = 0
    while i < n:
        k = i + 1
        while k < n and lijst[k] == lijst[i]:
            indices.append(i)
            k += 1
            # element op positie k is nu het eerste 'nieuwe' element
        x_mean = (k + i) / 2
        # voeg de indices toe van de unieke elementen
        indices.append(k)
        # zoek verder vanaf het eerste 'nieuwe' element
        i = k
    return indices[:-1]

index_FPR = index_machine(FPR)
index_TPR = index_machine(TPR)

def kies_indices(lijst1, lijst2):
    assert len(lijst1) == len(lijst2)
    gekozen_indices = []
    n = len(lijst1)
    laatst_genomen1 = 0
    laatst_genomen2 = 0
    for k in range(n):
        if k in lijst1 and k in lijst2:
            gekozen_indices.append(k)
            laatst_genomen1 = lijst1[k]
            laatst_genomen2 = lijst2[k]

        if (k in lijst1 and k not in lijst2
            and lijst2[k] != laatst_genomen2):
            gekozen_indices.append(k)
            laatst_genomen1 = lijst1[k]
            laatst_genomen2 = lijst2[k]

        if (k in lijst2 and k not in lijst1
            and lijst1[k] != laatst_genomen1):
            gekozen_indices.append(k)
            laatst_genomen1 = lijst1[k]
            laatst_genomen2 = lijst2[k]

        if k not in lijst1 and k not in lijst2:
            print("beide niet in lijst.")
    return gekozen_indices


idx = kies_indices(index_FPR, index_TPR)
print("Het aantal weerhouden koppels bedraagt:", len(idx))
print("De indices zijn:", idx)

def trim(lijst1, goede_elementen):
    '''
    Weerhoudt de elementen in lijst1 op de indices uit goede_elementen.
    :param lijst1:
    :param goede_elementen:
    :return: een lijst met unieke elementen.
    '''
    nieuwe_lijst = []
    for k in goede_elementen:
        nieuwe_lijst.extend([lijst1[k]])
    return nieuwe_lijst

FPR_getrimt = trim(FPR, idx)
TPR_getrimt = trim(TPR, idx)
threshold_getrimt = trim(threshold, idx)
# print("De weerhouden thresholds zijn:", threshold_getrimt)

#########################
# CONTROLE              #
#########################

def verschil(lijst1):
    '''
    #todo aanvullen
    :param lijst1:
    :return:
    '''
    verschil_lijst = []
    for i in range(len(lijst1) - 1):
        verschil_waarde = lijst1[i + 1] - lijst1[i]
        verschil_lijst.append(verschil_waarde)
    return verschil_lijst

assert 0 not in verschil(FPR_getrimt)
assert 0 not in verschil(TPR_getrimt)

ACCEPT = "accept"
CONTINUE = "continue"
ABANDON = "abandon"

def likelihood_helper(FPR, TPR, start_idx, eind_idx):
    delta2 = TPR[eind_idx] - TPR[start_idx]
    delta1 = FPR[eind_idx] - FPR[start_idx]
    return delta2 / delta1

######################
# BACKTRACKING       #
######################

def extend(partial_solution, FPR, TPR, n, likelihood):
    ext_sol = []
    a = partial_solution[-1]
    if True:
        for getal in range(a + 1, min(a + b1, n)):
            if likelihood_helper(FPR, TPR, a, getal) < likelihood: # als de likelihood afneemt
                new_sol = partial_solution + [getal]
                ext_sol.append(new_sol)
    # if 30 < a < 70:
    #     for getal in range(a + 1, min(a + b2, n)):
    #         if likelihood_helper(FPR, TPR, a, getal) < likelihood: # als de likelihood afneemt
    #             new_sol = partial_solution + [getal]
    #             ext_sol.append(new_sol)
    # if 70 < a < 110:
    #     for getal in range(a + 1, min(a + b3, n)):
    #         if likelihood_helper(FPR, TPR, a, getal) < likelihood: # als de likelihood afneemt
    #             new_sol = partial_solution + [getal]
    #             ext_sol.append(new_sol)
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

def bereken_likelihood(FPR, TPR):
    likelihood_lijst = []
    verd = verdeling(FPR, TPR)
    for i in range(len(verd) - 1):
        LR = likelihood_helper(FPR, TPR, verd[i], verd[i + 1])
        likelihood_lijst += [LR]
    return likelihood_lijst

start = time.perf_counter()
verd_20 = verdeling(FPR_getrimt[:], TPR_getrimt[:])
stop = time.perf_counter()
print("Het aantal gevonden indices bedraagt:", len(verd_20))

print("tijd om de indices te berekenen:", stop - start)

LR_20 = bereken_likelihood(FPR_getrimt[:], TPR_getrimt[:])
thresh_20 = trim(threshold_getrimt[:], verd_20)


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

#########################
# SCHRIJF NAAR EXCEL    #
#########################

df3 = pd.DataFrame({
    "FPR_getrimt": FPR_getrimt,
    "TPR_getrimt": TPR_getrimt,
    # "verschil_FPR": ["nan"] +verschil_FPR,
    # "verschil_TPR": ["nan"] + verschil_TPR,
    # "likelihood": ["nan"] + likelihood,
    "threshold_getrimt_getrimt": threshold_getrimt}
                   )
df4 = pd.DataFrame({
    "indices_intervallen": verd_20,
    "thresholds_intervallen": thresh_20,
    "likelihood_tussen_intervallen": ['inf'] + LR_20
})
with pd.ExcelWriter("tTG_lijsten.xlsx", mode='a') as writer:
    df3.to_excel(writer, "getrimde_lijsten " + naam)
    df4.to_excel(writer, "intervallen " + naam)




