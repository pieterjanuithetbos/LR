import numpy as np

from versie3.trimmen import FPR_getrimt

FPR = np.loadtxt('FPR.txt', delimiter=' ')
TPR = np.loadtxt('TPR.txt', delimiter=' ')
threshold = np.loadtxt('threshold.txt', delimiter=' ')

def index_machine(lijst):
    '''
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

# print(index_machine(FPR))

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
print(idx)
print(len(idx))


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

FPR_69 = trim(FPR, idx)
TPR_69 = trim(TPR, idx)
threshold_69 = trim(threshold, idx)
print(threshold_69)

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

assert 0 not in verschil(FPR_69)
assert 0 not in verschil(TPR_69)


np.savetxt('FPR_getrimt.txt', FPR_69, delimiter=' ')
np.savetxt('TPR_getrimt.txt', TPR_69, delimiter=' ')
np.savetxt('threshold_getrimt.txt', threshold_69, delimiter=' ')

