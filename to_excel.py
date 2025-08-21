import pandas as pd
import numpy as np

FPR_getrimt = np.loadtxt('FPR_getrimt.txt', delimiter=' ')
TPR_getrimt = np.loadtxt('TPR_getrimt.txt', delimiter=' ')
threshold_getrimt = np.loadtxt('threshold_getrimt.txt', delimiter=' ')

df1 = pd.DataFrame({
    "FPR_getrimt": FPR_getrimt,
    "TPR_getrimt": TPR_getrimt,
    # "verschil_FPR": ["nan"] + verschil_FPR,
    # "verschil_TPR": ["nan"] + verschil_TPR,
    # "likelihood": ["nan"] + likelihood,
    "threshold_getrimt": threshold_getrimt}
                   )
df1.to_excel("getrimde_data.xlsx")