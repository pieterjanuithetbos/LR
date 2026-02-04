import pandas as pd
import time
import numpy as np

#################
# PARAMETERS    #
#################

path_output_file = "output_2.xlsx"
excel_sheet = 'input.xlsx'
naam = 'CCP Siemens'
total_FPR = 1073
total_TPR = 398
minimum_FPR = 2
minimum_TPR = 2
verhouding = 1.5
breedte = 9


################
# LEES EXCEL   #
################

df = pd.read_excel(excel_sheet, sheet_name=naam, index_col=0)
# gebruik index_col=0 om de ID's van de rijen zoals weergegeven in excel te gebruiken


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
    """
    Vergelijkt de twee lijsten en geeft een nieuwe lijst terug met de ‘overlap’. In de
    nieuwe lijst, komen enkel unieke elementen voor.
    :param lijst1:
    :param lijst2:
    :return: lijst met indices van unieke elementen
    """
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
print("--------------- INFO GETRIMDE LIJSTEN ---------------")
print("Het aantal weerhouden koppels bedraagt:", len(idx))
print("De indices zijn:", idx)

def trim(lijst1, goede_elementen):
    '''
    Weerhoudt de elementen in lijst1 op de indices uit goede_elementen.
    :param lijst1:
    :param goede_elementen:
    :return: een lijst met unieke elementen.
    '''
    array_lijst1 = np.array(lijst1)
    nieuwe_lijst = array_lijst1[goede_elementen]
    return nieuwe_lijst.tolist()

FPR_getrimt = trim(FPR, idx)
TPR_getrimt = trim(TPR, idx)
threshold_getrimt = trim(threshold, idx)
# print("De weerhouden thresholds zijn:", threshold_getrimt)

#########################
# CONTROLE              #
#########################

def verschil(lijst):
    '''
    :param lijst1:
    :return:
    '''
    array = np.array(lijst)
    array_kopie = np.append(0, array[:-1])
    res = np.subtract(array, array_kopie)
    return res[1:].tolist()

assert 0 not in verschil(FPR_getrimt)
assert 0 not in verschil(TPR_getrimt)

def likelihood_helper(FPR, TPR, start_idx, eind_idx):
    """
    Gegeven de sensitiviteit en de specificiteit, samen met een startindex en een eindindex, berekent
    likelihood_helper de de richtingsafgeleide over het interval bepaald door de start- en
    eindindex.
    :param FPR:
    :param TPR:
    :param start_idx:
    :param eind_idx:
    :return: de richtingsafgeleide over [start_idx, eind_idx]
    """
    delta2 = TPR[eind_idx] - TPR[start_idx]
    delta1 = FPR[eind_idx] - FPR[start_idx]
    return delta2 / delta1

######################
# BACKTRACKING       #
######################

ACCEPT = "accept"
CONTINUE = "continue"
ABANDON = "abandon"

def extend(partial_solution, FPR, TPR, n, likelihood):
    '''
    :param partial_solution: lijst met weerhouden indices
    :param FPR: het laatste element in de FPR-lijst van de partial solution
    :param TPR: idem voor TPR
    :param n: lengte van de lijsten FPR en TPR
    :param likelihood: de LR van het laatste interval in de gevonden lijst
    :return: extended solutions die ...
    '''
    ext_sol = []
    a = partial_solution[-1]
    if True:
        for getal in range(a + 1, min(a + breedte, n)):
            if (likelihood_helper(FPR, TPR, a, getal)*verhouding < likelihood and
                abs(FPR[a] - FPR[getal])*total_FPR > minimum_FPR and
                abs(TPR[a] - TPR[getal])*total_TPR > minimum_TPR): # als de likelihood afneemt
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

def bereken_likelihood(FPR, TPR, verd):
    # zet om naar numpy arrays
    FPR_array = np.array(FPR)
    TPR_array = np.array(TPR)
    # bereken de delta's
    FPR_trimmed = FPR_array[verd]
    FPR_verschil = np.subtract(FPR_trimmed[1:], FPR_trimmed[:-1])
    TPR_trimmed = TPR_array[verd]
    TPR_verschil = np.subtract(TPR_trimmed[1:], TPR_trimmed[:-1])
    LR_array = np.divide(TPR_verschil, FPR_verschil)
    return LR_array.tolist()

start = time.perf_counter()
verd = verdeling(FPR_getrimt[:], TPR_getrimt[:])
stop = time.perf_counter()
print("--------------- RESULTAAT BACKTRACKING --------------")
print("Het aantal gevonden indices bedraagt:", len(verd))
print("tijd om de indices te berekenen:", stop - start)
# print("-----------------------------------------------------")

LR_20 = bereken_likelihood(FPR_getrimt[:], TPR_getrimt[:], verd)
thresh_20 = trim(threshold_getrimt[:], verd)


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
# EXTRA BEREKENINGEN    #
#########################


FPR_np = np.array(FPR_getrimt)
weerhouden_FPR = FPR_np[verd]
TPR_np = np.array(TPR_getrimt)
weerhouden_TPR = TPR_np[verd]
threshold_np = np.array(threshold_getrimt)
weerhouden_threshold = threshold_np[verd]

verschil_weerhouden_FPR = [weerhouden_FPR[0]] + verschil(weerhouden_FPR)
verschil_weerhouden_TPR = [weerhouden_TPR[0]] + verschil(weerhouden_TPR)

#########################
# SCHRIJF NAAR EXCEL    #
#########################


df2 = pd.DataFrame({
    "FPR": FPR_getrimt,
    "TPR": TPR_getrimt,
    # "verschil_FPR": ["nan"] +verschil_FPR,
    # "verschil_TPR": ["nan"] + verschil_TPR,
    # "likelihood": ["nan"] + likelihood,
    "threshold": threshold_getrimt,
})


df3 = pd.DataFrame({
    "weerhouden indices": verd,
    "weerhouden FPR": weerhouden_FPR,
    "weerhouden TPR": weerhouden_TPR,
    "weerhouden thresholds": weerhouden_threshold,
    "LR tussen intervallen": ['inf'] + LR_20
})

df4 = pd.DataFrame({
    "verschil FPR": verschil_weerhouden_FPR,
    "aantal FPR": np.multiply(verschil_weerhouden_FPR, total_FPR)
})

df5 = pd.DataFrame({
    "verschil TPR": verschil_weerhouden_TPR,
    "aantal TPR": np.multiply(verschil_weerhouden_TPR, total_TPR)
})

dfinfo = pd.DataFrame({
    "minimum FPR": minimum_FPR,
    "minimum TPR": minimum_TPR,
    "verhouding": verhouding
}, index=[0])


sheet_naam = naam + f" {minimum_FPR} " + f" {minimum_TPR}" + f" {verhouding}"
with pd.ExcelWriter(path_output_file, mode='a', if_sheet_exists="overlay") as writer:
    df2.to_excel(writer, sheet_name=sheet_naam)
    df3.to_excel(writer, sheet_name=sheet_naam, startcol=len(df2.columns) + 2)
    df4.to_excel(writer, sheet_name=sheet_naam, startcol=len(df2.columns) + 2 + len(df3.columns) + 2)
    df5.to_excel(writer, sheet_name=sheet_naam, startcol=len(df2.columns) + 2 + len(df3.columns) + 2 + len(df4.columns) + 2)
    dfinfo.to_excel(writer, sheet_name=sheet_naam, startcol=len(df2.columns) + 2, startrow=len(df3.index) + 2)




