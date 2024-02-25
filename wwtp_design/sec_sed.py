import math as m
from data import *


# Author: Camila Alvarado
class SecSed:
    def __init__(self):
        """
        For initializing a SecSed object with the given
        attributes and methods
        :return: None
        """
        # return sludge ratio always 0.75 dimensionless
        self.rs = 0.75
        # max sludge volume loading rate for horizontal flow (L/(m²*h))
        self.qsv = 500
        # clean water and return flow zone with minimum depth of 0.5 m
        self.h1 = 0.5

    def x_ss_at(self):
        """
        Calculation of suspended solids concentration in the activated
        sludge tank
        :return: FLOAT result in g/L or kg/m³
        """
        return (self.rs * x_ss_rs()) / (1 + self.rs)

    def q_a(self):
        """
        Calculation of the surface overflow rate of the secondary
        sedimentation tank
        :return: FLOAT result in m/h
        """
        if (self.qsv /
                (self.x_ss_at() *
                 np.mean(SVI["Favourable"]["Nitrification"
                                           " and denitrification"])) <= 1.6):
            return (self.qsv
                    / (self.x_ss_at() *
                       np.mean(SVI["Favourable"]["Nitrification"
                                                 " and denitrification"])))
        else:
            return "The surface overflow flow rate q_a was exceeded"

    def a_st(self):
        """
        Calculation of tank surface area and number of circular tanks
        :return: TUPLE containing a FLOAT result in m² and a STRING
        indicating the number of circular tanks
        """
        # With a limit value of 2827.43 m2 , the maximum diameter of
        # the collector bridge would be 60 m according to the
        # recommendations for stability in the collector bridge
        a_st = ((InputReader().wwtp_params["Value"]["Q comb"] / 24) /
                self.q_a())
        if a_st <= 2827.43:
            # Redundancy of 1 in case of collector bridge maintenance
            return a_st, 2
        elif 2827.44 < a_st <= 4250:
            return (a_st / 2), 3
        elif 4250 < a_st <= 5650:
            return (a_st / 3), 4
        elif 5650 < a_st <= 7100:
            return (a_st / 4), 5
        elif 7100 < a_st <= 8450:
            return (a_st / 5), 6
        else:
            return (a_st / 6), 7

    def diam_st(self):
        """
        Calculation of the diameter of each of the secondary
        sedimentation tank(s)
        :return: FLOAT result in m
        """
        return ((4 * self.a_st()[0]) / m.pi) ** (1/2)

    def h2(self):
        """
        Calculation of the separation and return flow zone
        :return: FLOAT result in m
        """
        return ((0.5 * self.q_a() * (1 + self.rs)) /
                (1 - ((self.x_ss_at() *
                       np.mean(SVI["Favourable"]
                               ["Nitrification and denitrification"]))
                      / 1000)))

    def h3(self):
        """
        Calculation of the density flow and storage zone
        :return: FLOAT result in m
        """
        return (1.5 * 0.3 * self.qsv * (1 + self.rs)) / 500

    def h4(self):
        """
        Calculation of the thickening and sludge removal zone
        :return: FLOAT result in m
        """
        return ((self.x_ss_at() * self.q_a()
                * (1 + self.rs) *
                TTH["Thickening time"]
                ["Activated sludge plants with denitrification"][0])
                / x_ss_bs())

    def h_tot(self):
        """
        Calculation of the total depth of the secondary circular
        sedimentation tank
        :return: FLOAT result in m
        """
        h_tot = self.h1 + self.h2() + self.h3() + self.h4()
        if h_tot >= 3:
            return h_tot
        else:
            return "The calculated circular tank depth is not sufficient"
