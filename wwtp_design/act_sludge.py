from sec_sed import *


# Author: Luis Granda
class ActSludge(InputReader):
    def __init__(self):
        """
        For initializing an ActSludge object with the given
        attributes and methods
        :return: None
        """
        InputReader.__init__(self)
        # frequently used parameter
        self.S_orgN_EST = 2  # assumption due to experience
        self.S_NH4_EST = 0  # from 0 to 1
        # from 9 to 10 according to European Union Laws
        self.S_NO3_EST = 9

    def c_n_iat(self):
        """
        Calculation of the total nitrogen concentration from the
        influent to the activated sludge tank
        :return: FLOAT result in mg/L
        """
        return (self.wwtp_params["Value"]["B d,Ntot"]
                / self.wwtp_params["Value"]["Q d,aM"]) * (10 ** 6 / 1000)

    def c_bod5_iat(self):
        """
        Calculation of the BOD5 concentration from the
        influent to the activated sludge tank
        :return: FLOAT result in mg/L
        """
        return (self.wwtp_params["Value"]["B d,BOD5"]
                / self.wwtp_params["Value"]["Q d,aM"]) * (10 ** 6 / 1000)

    def x_orgn_bm(self):
        """
        Calculation of the concentration of organic nitrogen
        embedded in biomass (about 5% of self.c_bod5)
        :return: FLOAT result in mg/L
        """
        return 0.05 * self.c_bod5_iat()

    def n_bal(self):
        """
        Calculation of the nitrogen balance
        :return: TUPLE with FLOATS of c_NH4_n and c_NO3_dn in mg/L
        """
        if self.S_orgN_EST + self.S_NH4_EST + self.S_NO3_EST < 13:
            # concentration of ammonium nitrogen to be nitrified
            S_NH4_N = (self.c_n_iat() - self.S_orgN_EST
                       - self.S_NH4_EST - self.x_orgn_bm())
            # daily average nitrate concentration to be denitrified
            S_NO3_D = S_NH4_N - self.S_NO3_EST
            return S_NH4_N, S_NO3_D
        else:
            return ("Check assumptions or choose low values"
                    " for C_NH4_E_SST or C_NO3_E_SST")

    def den_ratio(self):
        """
        Calculates the ratio of nitrate nitrogen concentration to BOD5
        input concentration to activated sludge tank in order to
        determine denitrification potential
        :return: dimensionless FLOAT result
        """
        return self.n_bal()[1] / self.c_bod5_iat()

    def inter_vd_vat(self):
        """
        Interpolates the corresponding value of "Vd/Vat" for a given
        target value (self.den_ratio()) in the "Pre-anoxic zone
        denitrification and comparable processes" column
        :return: dimensionless FLOAT result
        """
        return np.interp(self.den_ratio(),
                         S_NO3_D_C_BOD_IAT["Pre-anoxic zone "
                                           "denitrification and "
                                           "comparable processes"],
                         S_NO3_D_C_BOD_IAT.index)

    def s_f(self):
        """
        Calculation of the safety factor
        :return: dimensionless FLOAT result
        """
        if (self.wwtp_params["Value"]["B d,BOD5"] <= 1200 or
                self.wwtp_params["Value"]["Population"] <= 20000):
            return 1.8
        elif (self.wwtp_params["Value"]["B d,BOD5"] >= 6000 or
              self.wwtp_params["Value"]["Population"] >= 100000):
            return 1.45
        else:
            return "Approximate B d,BOD5 and Population to the closest value"

    def t_ss_aerob_dim(self):
        """
        Calculation of the (aerobic) dimensioning sludge age to be
        maintained for nitrification
        :return: FLOAT result in days
        """
        return (self.s_f() * 3.4
                * 1.103 ** (15 - self.wwtp_params["Value"]["Tdim"]))

    def t_ss_dim(self):
        """
        Calculation of the dimensioning sludge age for nitrification
        and denitrification
        :return: FLOAT result in days
        """
        return self.t_ss_aerob_dim() * (1 / (1 - (self.inter_vd_vat())))

    def inter_t_ss_dim(self):
        """
        Another way to calculate the dimensioning sludge age by
        interpolating the corresponding value of "t_ss_dim" for a
        given target value (inter_vd_vat()) in the corresponding
        column of "Tdim"
        :return: FLOAT result in days
        """
        if not 10.0 <= self.wwtp_params["Value"]["Tdim"] <= 12.0:
            return "Temperatures outside the 10 to 12°C range"

        start_weight, end_weight =\
            calc_weights(10, 12, self.wwtp_params["Value"]["Tdim"])

        if (self.wwtp_params["Value"]["B d,BOD5"] <= 1200 or
                self.wwtp_params["Value"]["Population"] <= 20000):
            root_key = f"up to 1200 kg/d"
            column_key =\
                f"{self.wwtp_params['Value']['Tdim']} °C - up to 1200 kg/d"
        elif (self.wwtp_params["Value"]["B d,BOD5"] >= 6000 or
              self.wwtp_params["Value"]["Population"] >= 100000):
            root_key = f"over 6000 kg/d"
            column_key =\
                f"{self.wwtp_params['Value']['Tdim']} °C - over 6000 kg/d"
        else:
            return "Approximate B d,BOD5 and Population to the closest ranges"

        T_SS_DIM[column_key] = (
                T_SS_DIM[f"10 °C - {root_key}"] * start_weight
                + T_SS_DIM[f"12 °C - {root_key}"] * end_weight
        )
        return np.interp(self.inter_vd_vat(), T_SS_DIM["Vd/Vat"],
                         T_SS_DIM[column_key])

    def b_d_ss_iat(self):
        """
        Calculation of the daily suspended solids load from the
        influent to the activated sludge tank
        :return: FLOAT result in kg/d
        :return:
        """
        return (INH_B["0.5 to 1.0 h of retention time"]["SS"]
                * self.wwtp_params["Value"]["Population"] / 1000)

    def x_ss_iat(self):
        """
        Calculation of the suspended solids concentration from the
        influent to the activated sludge tank
        :return: FLOAT result in mg/L
        """
        return ((self.b_d_ss_iat() / self.wwtp_params["Value"]["Q d,aM"])
                * (10 ** 6 / 1000))

    def ss_bod5_ratio(self):
        """
        Calculates the ratio of suspended solids input concentration
        and BOD5 input concentration to activated sludge tank
        :return: dimensionless FLOAT result
        """
        return self.x_ss_iat() / self.c_bod5_iat()

    def f_t(self):
        """
        Calculation of the temperature factor for endogenous respiration
        :return: dimensionless FLOAT result
        """
        return 1.072 ** (self.wwtp_params["Value"]["Tdim"] - 15)

    def sp_d_c(self):
        """
        Calculation of the sludge production from carbon removal
        :return: FLOAT result in kg/d
        """
        return (self.wwtp_params["Value"]["B d,BOD5"]
                * (0.75 + 0.6 * self.ss_bod5_ratio()
                   - (((1 - 0.2) * 0.17 * 0.75 * self.t_ss_dim() * self.f_t())
                      / (1 + 0.17 * self.t_ss_dim() * self.f_t()))))

    def inter_sp_c_bod(self):
        """
        Calculation of the specific sludge production by interpolating
        the corresponding value of "SP_C_BOD" for a given target value
        (X_ss_iat/C_bod_iat) in the corresponding column of the sludge
        age "self.t_ss_dim()"
        :return: FLOAT result in kgSS/kgBOD5
        """
        t_ss_ranges = [(4, 8), (8, 10), (10, 15), (15, 20), (20, 25)]
        for start, end in t_ss_ranges:
            if start <= self.t_ss_dim() <= end:
                start_weight, end_weight = calc_weights(start, end,
                                                        self.t_ss_dim())
                SP_C_BOD[self.t_ss_dim()] = (SP_C_BOD[start] * start_weight
                                             + SP_C_BOD[end] * end_weight)
                return np.interp(self.ss_bod5_ratio(),
                                 SP_C_BOD.index,
                                 SP_C_BOD[self.t_ss_dim()])
        return "Sludge age out of range"

    def inter_sp_d_c(self):
        """
        Another way to calculate the sludge production from carbon
        removal is to multiply the specific sludge production and the
        influent BOD5 load to the activated sludge tank.
        :return: FLOAT result in kgSS/d
        """
        return self.inter_sp_c_bod() * self.wwtp_params["Value"]["B d,BOD5"]

    def c_p_iat(self):
        """
        Calculation of the total phosphorus concentration from the
        influent to the activated sludge tank
        :return: FLOAT result in mg/L
        """
        return (self.wwtp_params["Value"]["B d,Ptot"]
                / self.wwtp_params["Value"]["Q d,aM"]) * (10 ** 6 / 1000)

    def c_p_er(self):
        """
        Searches for effluent requirement for phosphorus according
        to respective size class
        :return: FLOAT result in mg/L
        """
        if self.wwtp_params["Value"]["B d,BOD5"] < 60:
            return CLE_REQ["Ptot"]["1 (< 60 kgBOD5/d in raw water)"]
        elif 60 <= self.wwtp_params["Value"]["B d,BOD5"] <= 300:
            return CLE_REQ["Ptot"]["2 (60 - 300 kgBOD5/d in raw water)"]
        elif 300 < self.wwtp_params["Value"]["B d,BOD5"] <= 600:
            return CLE_REQ["Ptot"]["3 (300 - 600 kgBOD5/d in raw water)"]
        elif 600 < self.wwtp_params["Value"]["B d,BOD5"] <= 6000:
            return CLE_REQ["Ptot"]["4 (600 - 6000 kgBOD5/d in raw water)"]
        else:
            return CLE_REQ["Ptot"]["5 (> 6000 kgBOD5/d in raw water"]

    def c_p_est(self):
        """
        Calculation of the total phosphorus concentration from the
        effluent of the secondary sedimentation tank
        :return: FLOAT result in mg/L
        """
        # (0.6 - 0.7), choose the highest to have a better safety factor
        return 0.7 * self.c_p_er()

    def x_p_bm(self):
        """
        Calculation of the phosphorus necessary for the build-up
        heterotrophic biomass
        :return: FLOAT result in mg/L
        """
        # 1 % in AST but 0.5 % in Trickling Filter
        return 0.01 * self.c_bod5_iat()

    def x_p_biop(self, anaerobic_tanks=False, inter_rec_sludge=False):
        """
        Calculation of the excess biological phosphorus removal
        :param anaerobic_tanks: TRUE or FALSE if working with
        anaerobic tanks
        :param inter_rec_sludge: TRUE or FALSE if at low temperatures,
        the internal recirculation of pre-anoxic zone denitrification
        is discharged into the anaerobic tank
        :return: FLOAT result in mg/L
        """
        if anaerobic_tanks is True and self.S_NO3_EST >= 15:
            # 0.005 to 0.01 * self.c_bod5_iat()
            return 0.005 * self.c_bod5_iat()
        elif anaerobic_tanks is True and inter_rec_sludge is True:
            return 0.005 * self.c_bod5_iat()
        elif anaerobic_tanks is True:
            # 0.01 to 0.015 * self.c_bod5_iat()
            return 0.01 * self.c_bod5_iat()
        elif anaerobic_tanks is False:
            return 0.005 * self.c_bod5_iat()
        else:
            return "Check default keyword arguments"

    def x_p_prec(self, x_p_biop=False):
        """
        Calculation of the phosphorous balance or determination of the
        phosphate to be precipitated
        :param x_p_biop: TRUE or False if considering excess biological
        phosphorus removal
        :return: FLOAT result in mg/L
        """
        if x_p_biop is True:
            return (self.c_p_iat() - self.c_p_est()
                    - self.x_p_bm() - self.x_p_biop())
        else:
            return self.c_p_iat() - self.c_p_est() - self.x_p_bm()

    def sp_d_p(self, precipitant="Fe", x_p_biop=False):
        """
        Calculation of the sludge production from the phosphorus removal
        :param precipitant: STRING of the type of precipitant
        :param x_p_biop: TRUE or FALSE if considering excess biological
        phosphorus removal
        :return: FLOAT result in kg/d
        """
        # Fe is the cheapest precipitant
        if precipitant == "Fe" and x_p_biop is True:
            return (self.wwtp_params["Value"]["Q d,aM"]
                    * (3 * self.x_p_biop() + 6.8 * self.x_p_prec())) / 1000
        # Fe is the cheapest precipitant
        elif precipitant == "Fe" and x_p_biop is False:
            return (self.wwtp_params["Value"]["Q d,aM"]
                    * 6.8 * self.x_p_prec()) / 1000
        elif precipitant == "Al" and x_p_biop is True:
            return (self.wwtp_params["Value"]["Q d,aM"]
                    * (3 * self.x_p_biop() + 5.3 * self.x_p_prec())) / 1000
        elif precipitant == "Al" and x_p_biop is False:
            return (self.wwtp_params["Value"]["Q d,aM"]
                    * 5.3 * self.x_p_prec()) / 1000
        else:
            return "Check default keyword arguments"

    def sp_d(self):
        """
        Determination of sludge production in an activated sludge plant
        :return: FLOAT result in kg/d
        """
        return self.sp_d_c() + self.sp_d_p()

    def m_ss_at(self):
        """
        Calculation of the required mass of suspended solids
        in the activated sludge tank
        :return: FLOAT result in kg
        """
        return self.t_ss_dim() * self.sp_d()

    def v_at(self):
        """
        Calculation of the volume of the activated sludge tank
        :return: FLOAT result in m³
        """
        return self.m_ss_at() / SecSed().x_ss_at()

    def v_d(self):
        """
        Calculation of the volume of the activated sludge tank used
        for denitrification
        :return: FLOAT result in m³
        """
        return self.inter_vd_vat() * self.v_at()

    def v_n(self):
        """
        Calculation of the volume of the activated sludge tank used
        for nitrification
        :return: FLOAT result in m³
        """
        return (1 - self.inter_vd_vat()) * self.v_at()

    def rc(self):
        """
        Calculation of the necessary total recirculation flow ratio (RC)
        for pre-anoxic zone denitrification
        :return: dimensionless FLOAT result
        """
        return (self.n_bal()[0] / self.S_NO3_EST) - 1

    def n_d(self):
        """
        Calculation of maximum possible efficiency of denitrification
        :return: dimensionless FLOAT result
        """
        if 1 - (1 / (1 + self.rc())) >= 0.7:
            return 1 - (1 / (1 + self.rc()))
        else:
            return ("The minimum removal of 70% nitrogen established by"
                    " the European Union is not met. Modify S_NH4_N or "
                    "S_NO3_EST in the nitrogen balance")

    def ou_d_c(self):
        """
        Calculation of oxygen uptake for carbon removal
        :return: FLOAT result in kgO2/d
        """
        return (self.wwtp_params["Value"]["B d,BOD5"] *
                (0.56 + ((0.15 * self.t_ss_dim() * self.f_t()) /
                         (1 + 0.17 * self.t_ss_dim() * self.f_t()))))

    def s_no3_iat(self):
        """
        Calculation of the nitrate nitrogen concentration from the
        influent to the activated sludge tank
        :return: FLOAT result in mg/L
        """
        return (self.wwtp_params["Value"]["B d,NO3-N"]
                / self.wwtp_params["Value"]["Q d,aM"]) * (10 ** 6 / 1000)

    def ou_d_n(self):
        """
        Calculation of oxygen uptake for nitrification
        :return: FLOAT result in kgO2/d
        """
        return (self.wwtp_params["Value"]["Q d,aM"] * 4.3 *
                (self.n_bal()[1] - self.s_no3_iat() + self.S_NO3_EST) / 1000)

    def ou_d_d(self):
        """
        Calculation of oxygen uptake for denitrification
        :return: FLOAT result in kgO2/d
        """
        return (self.wwtp_params["Value"]["Q d,aM"]
                * 2.9 * self.n_bal()[1] / 1000)

    def inter_fc_fn(self):
        """
        Determining the peak factors for the oxygen uptake rate by
        calculating a new column in the DF for a given target value of
        (self.t_ss_dim) and extracting the respective fc and fn
        :return: TUPLE with dimensionless FLOATS results
        """
        t_ss_ranges = [(4, 6), (6, 8), (8, 10), (10, 15), (15, 25)]
        if (self.wwtp_params["Value"]["B d,BOD5"] <= 1200 or
                self.wwtp_params["Value"]["Population"] <= 20000):
            root_key = f"for <= 1200 kgBOD5/d"
        elif (self.wwtp_params["Value"]["B d,BOD5"] >= 6000 or
              self.wwtp_params["Value"]["Population"] >= 100000):
            root_key = f"for >= 6000 kgBOD5/d"
        else:
            return "Approximate B d,BOD5 and Population to the closest ranges"

        for start, end in t_ss_ranges:
            if start <= self.t_ss_dim() <= end:
                start_weight, end_weight = calc_weights(start, end,
                                                        self.t_ss_dim())
                FC_FN[self.t_ss_dim()] = (FC_FN[start] * start_weight +
                                          FC_FN[end] * end_weight)
                return (FC_FN[self.t_ss_dim()]["fc"],
                        FC_FN[self.t_ss_dim()][f"fn {root_key}"])
        return "Sludge age out of range"

    def ou_h(self):
        """
        Calculation of the oxygen uptake rate for the daily peak
        :return: FLOAT result in kgO2/h
        """
        return (self.inter_fc_fn()[0] * (self.ou_d_c() - self.ou_d_d())
                + self.inter_fc_fn()[1] * self.ou_d_n()) / 24
