from data import *


# Author: Lucas Tardio
class PriSed(InputReader):
    def __init__(self):
        """
        For initializing a PriSed object with the given
        attributes and methods
        :return: None
        """
        InputReader.__init__(self)
        # starting values
        self.num_tanks = 2
        self.width = 1
        self.pri_deep = (
            PARAMS_PRI)["Depth"][("PS combined with activated sludge"
                                  " process (with excess sludge)")]

    def pri_surf(self):
        """
        Rectangular primary sedimentation tank surface calculation
        :return: FLOAT result in m²
        """
        return (
                (self.wwtp_params["Value"]["Q comb"] / 24)
                / PARAMS_PRI["q_A"]
                ["PS combined with activated sludge process"
                 " (with excess sludge)"][1]
        )

    def cross_volume(self):
        """
        Calculation of cross-section and volume for each rectangular
        primary sedimentation tank
        :return: TUPLE with FLOATS of area in m², num_tanks, length
        in m, width in m, and volume in m³
        """
        # Maximum width of 10 m according to recommendations
        while self.width <= 10:
            area = self.pri_surf() / self.num_tanks
            length = area / self.width
            ratio = self.width / length
            volume = self.num_tanks * self.width * self.pri_deep * length
            if 0.1 <= ratio <= 0.2:
                return area, self.num_tanks, length, self.width, volume
            elif self.width >= 10:
                self.num_tanks += 1
                self.width = 1
            else:
                self.width += 0.5
