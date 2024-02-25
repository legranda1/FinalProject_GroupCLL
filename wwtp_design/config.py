import pandas as pd
import numpy as np

# Parameters for Primary Sedimentation according
# to DIN EN 12255-6
params_pri = {
    "Treatment method": [
        "PS combined with activated sludge process (without excess sludge)",
        "PS combined with activated sludge process (with excess sludge)",
        "PS combined with trickling filter or rotating contactors"
        " (with / without excess sludge)"
    ],
    "q_A": [6, np.arange(2, 4, 1), 3],
    "t": [15, 45, 30],
    "Depth": [1.5, 2.0, 1.5]
}
PARAMS_PRI = pd.DataFrame(params_pri)
PARAMS_PRI.set_index("Treatment method", inplace=True)

# Standard values for the sludge volume index according
# to ATV-DVWK-A 131E
svi = {
    "Treatment target": [
        "Without nitrification",
        "Nitrification and denitrification",
        "Sludge stabilization"
    ],
    "Favourable": [[100, 150], [100, 150], [75, 120]],
    "Unfavourable": [[120, 180], [120, 180], [100, 150]]
}
SVI = pd.DataFrame(svi)
SVI.set_index("Treatment target", inplace=True)

# Recommended thickening time in dependence on the degree of wastewater
# treatment according to ATV-DVWK-A 131E
tth = {
    "Type of WWTP": [
        "Activated sludge plants without nitrification",
        "Activated sludge plants with nitrification",
        "Activated sludge plants with denitrification"
    ],
    "Thickening time": [np.arange(1.5, 2.5, 0.5), np.arange(1.0, 2.0, 0.5),
                        np.arange(2.0, 3.0, 0.5)],
}
TTH = pd.DataFrame(tth)
TTH.set_index("Type of WWTP", inplace=True)

# Standard values for dimensioning of denitrification for dry weather
# at temperatures from 10° to 12° C and common conditions (kg nitrate
# nitrogen to be denitrified per kg influent BOD5) according to
# ATV-DVWK-A 131E
s_no3_d_c_bod_iat = {
    "Vd/Vat": [0.2, 0.3, 0.4, 0.5],
    "Pre-anoxic zone denitrification and comparable processes": [
        0.11, 0.13, 0.14, 0.15
    ],
    "Simultaneous and intermittent denitrification": [0.06, 0.09, 0.12, 0.15]
}
S_NO3_D_C_BOD_IAT = pd.DataFrame(s_no3_d_c_bod_iat)
S_NO3_D_C_BOD_IAT.set_index("Vd/Vat", inplace=True)

# Dimensioning sludge age in days dependent on the treatment target and
# the temperature as well as the plant size (intermediate values are to
# be estimated) according to ATV-DVWK-A 131E
t_ss_dim = {
    "Treatment target": [
        "Without nitrification",
        "With nitrification",
        "Nitrification and denitrification",
        "Nitrification and denitrification",
        "Nitrification and denitrification",
        "Nitrification and denitrification",
        "Sludge stabilization including nitrogen removal"
    ],
    "Vd/Vat": [np.nan, np.nan, 0.2, 0.3, 0.4, 0.5, np.nan],
    "10 °C - up to 1200 kg/d": [5.0, 10.0, 12.5, 14.3, 16.7, 20.0, 25.0],
    "12 °C - up to 1200 kg/d": [5.0, 8.2, 10.3, 11.7, 13.7, 16.4, 25.0],
    "10 °C - over 6000 kg/d": [4.0, 8.0, 10.0, 11.4, 13.3, 16.0, np.nan],
    "12 °C - over 6000 kg/d": [4.0, 6.6, 8.3, 9.4, 11.0, 13.2, np.nan],
}
T_SS_DIM = pd.DataFrame(t_ss_dim)
T_SS_DIM.set_index("Treatment target", inplace=True)

# Inhabitant-specific loads in g/(I·d), which are undercut on 85 % of
# the days, without taking into account sludge liquor according to
# ATV-DVWK-A 131E
inh_b = {
    "Parameter": ["BOD5", "COD", "SS", "TKN", "P"],
    "Raw wastewater": [60, 120, 70, 11, 1.8],
    "0.5 to 1.0 h of retention time": [45, 90, 35, 10, 1.6],
    "1.5 to 2.0 h of retention time": [40, 80, 25, 10, 1.6],
}
INH_B = pd.DataFrame(inh_b)
INH_B.set_index("Parameter", inplace=True)

# Specific sludge production SPC,BOD [kg SS/kg BOD5] at 10° to 12° C
# according to ATV-DVWK-A 131E
sp_c_bob = {
    "X_ss_iat/C_bod_iat": [0.4, 0.6, 0.8, 1.0, 1.2],
    4: [0.79, 0.91, 1.03, 1.15, 1.27],
    8: [0.69, 0.81, 0.93, 1.05, 1.17],
    10: [0.65, 0.77, 0.89, 1.01, 1.13],
    15: [0.59, 0.71, 0.83, 0.95, 1.07],
    20: [0.56, 0.68, 0.80, 0.92, 1.04],
    25: [0.53, 0.65, 0.77, 0.89, 1.01]
}
SP_C_BOD = pd.DataFrame(sp_c_bob)
SP_C_BOD.set_index("X_ss_iat/C_bod_iat", inplace=True)

# Treatment requirements on wastewater for the discharge point depend in
# Germany on the size class of the wastewater treatment plant according
# to the German Wastewater Ordinance (AbwV) Appendix 1
cle_req = {
    "Size class": [
        "1 (< 60 kgBOD5/d in raw water)",
        "2 (60 - 300 kgBOD5/d in raw water)",
        "3 (300 - 600 kgBOD5/d in raw water)",
        "4 (600 - 6000 kgBOD5/d in raw water)",
        "5 (> 6000 kgBOD5/d in raw water"
    ],
    "COD": [150, 110, 90, 90, 75],
    "BOD": [40, 25, 20, 20, 15],
    "NH4-N": [np.nan, np.nan, 10, 10, 10],
    "Ntot": [np.nan, np.nan, np.nan, 18, 13],
    "Ptot": [np.nan, np.nan, np.nan, 2, 1]
}
CLE_REQ = pd.DataFrame(cle_req)
CLE_REQ.set_index("Size class", inplace=True)

# Peak factors for the oxygen uptake rate (to cover the 2 h peaks
# compared with the 24 h average, if no measurements are available)
# according to ATV-DVWK-A 131E
fc_f_n = {
    "Peak factors": [
        "fc",
        "fn for <= 1200 kgBOD5/d",
        "fn for >= 6000 kgBOD5/d"
    ],
    4: [1.30, np.nan, np.nan],
    6: [1.25, np.nan, np.nan],
    8: [1.20, np.nan, 2.00],
    10: [1.20, 2.50, 1.80],
    15: [1.15, 2.00, 1.50],
    25: [1.10, 1.50, np.nan]
}
FC_FN = pd.DataFrame(fc_f_n)
FC_FN.set_index("Peak factors", inplace=True)
