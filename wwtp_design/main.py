import sys
from act_sludge import *
from pri_sed import *
from time import perf_counter


def pri_sed_df():
    """
    Places the results of the primary sedimentation tank dimensioning
    in a data frame
    :return: DATAFRAME with the final results
    """
    params = ["Tank_surf", "Depth", "Area_per_tank",
              "Quantity", "Length", "Width", "Vmin"]
    results = [PriSed().pri_surf(), PriSed().pri_deep,
               PriSed().cross_volume()[0], PriSed().cross_volume()[1],
               PriSed().cross_volume()[2], PriSed().cross_volume()[3],
               PriSed().cross_volume()[4]]
    units = ["m2", "m", "m2", "rectangular tanks", "m", "m", "m3"]
    df = pd.DataFrame({"Results": results, "Units": units}, index=params)
    return df.round(2)


def sec_sed_df():
    """
    Places the results of the secondary sedimentation tank dimensioning
    in a data frame
    :return: DATAFRAME with the final results
    """
    params = ["SVI", "t_TH", "X_SS_BS", "X_SS_RS", "X_SS_AT", "q_SV", "q_A",
              "A_ST", "Quantity", "Diameter", "h1", "h2", "h3", "h4", "h_tot"]
    results = [
        np.mean(SVI["Favourable"]["Nitrification and denitrification"]),
        TTH["Thickening time"]["Activated sludge"
                               " plants with denitrification"][0], x_ss_bs(),
        x_ss_rs(), SecSed().x_ss_at(), SecSed().qsv, SecSed().q_a(),
        SecSed().a_st()[0], SecSed().a_st()[1], SecSed().diam_st(),
        SecSed().h1, SecSed().h2(), SecSed().h3(), SecSed().h4(),
        SecSed().h_tot()
    ]
    units = (["mL/g", "h"] + ["g/L"] * 3 + ["L/(m2*h)", "m/h", "m2"] +
             ["circular tanks"] + ["m"] * 6)
    df = pd.DataFrame({"Results": results, "Units": units}, index=params)
    return df.round(2)


def act_sludge_df():
    """
    Places the results of the activated sludge tank dimensioning
    in a data frame
    :return: DATAFRAME with the final results
    """
    a = ActSludge()
    params = ["C_BOD5_IAT", "C_N_IAT", "S_orgN_EST", "S_NH4_EST", "X_orgN_BM",
              "S_NH4_N", "S_NO3_EST", "S_NO3_D", "V_D/V_AT", "SF", "T",
              "t_SS_aerob_dim", "t_SS_dim", "X_SS_IAT", "F_T", "SP_d_C",
              "C_P_IAT", "C_P_EST", "X_P_BM", "X_P_Prec", "SP_d_P", "SP_d",
              "M_SS_AT", "X_SS_AT", "V_AT", "V_D", "V_N", "RC", "n_D",
              "OU_d_C", "S_NO3_IAT", "OU_d_N", "OU_d_D", "f_C", "f_N", "OU_h"]
    results = [a.c_bod5_iat(), a.c_n_iat(), a.S_orgN_EST, a.S_NH4_EST,
               a.x_orgn_bm(), a.n_bal()[0], a.S_NO3_EST, a.n_bal()[1],
               a.inter_vd_vat(), a.s_f(),
               InputReader().wwtp_params["Value"]["Tdim"], a.t_ss_aerob_dim(),
               a.t_ss_dim(), a.x_ss_iat(), a.f_t(), a.sp_d_c(), a.c_p_iat(),
               a.c_p_est(), a.x_p_bm(), a.x_p_prec(), a.sp_d_p(), a.sp_d(),
               a.m_ss_at(), SecSed().x_ss_at(), a.v_at(), a.v_d(), a.v_n(),
               a.rc(), a.n_d(), a.ou_d_c(), a.s_no3_iat(), a.ou_d_n(),
               a.ou_d_d(), a.inter_fc_fn()[0], a.inter_fc_fn()[1], a.ou_h()]
    units = (
            ["mg/L"] * 8 + ["-"] * 2 + ["C", "d", "d", "mg/L"] + ["-", "kg/d"]
            + ["mg/L"] * 4 + ["kg/d"] * 2 + ["kg", "g/L"] + ["m3"] * 3 + ["-"]
            * 2 + ["kgO2/d", "mg/L"] + ["kgO2/d"] * 2 + ["-"] * 2 + ["kgO2/h"]
    )
    df = pd.DataFrame({"Results": results, "Units": units}, index=params)
    return df.round(2)


@log_actions
def main():
    """
    Main functionality of the script
    :return: None or -1, but generates three log files
    """
    # retrieves logger objects from the logging system
    info_logger = logging.getLogger("info_logger")
    error_logger = logging.getLogger("error_logger")
    warning_logger = logging.getLogger("warning_logger")
    if InputReader().get_input_data("input_data.xlsx") == -1:
        info_logger.info("Nothing to show")
        warning_logger.warning("An unexpected event has occurred. "
                               "It is most likely an error")
        error_logger.error("The input file does not exist or is opened"
                           " by another program")
    else:
        # log of information
        info_logger.info("Using the following dimensioning data")
        info_logger.info(InputReader().wwtp_params)
        info_logger.info(
            "Results of the dimensioning of the primary sedimentation tank")
        pri_sed_df().to_excel(
            os.path.abspath("..") + "\\pri_sed_results.xlsx")
        info_logger.info(pri_sed_df())
        info_logger.info(
            "Results of the dimensioning of the secondary sedimentation tank")
        sec_sed_df().to_excel(
            os.path.abspath("..") + "\\sec_sed_results.xlsx")
        info_logger.info(sec_sed_df())
        info_logger.info(
            "Results of the dimensioning of the activated sludge tank")
        act_sludge_df().to_excel(
            os.path.abspath("..") + "\\act_sludge_results.xlsx")
        info_logger.info(act_sludge_df())
        # log of warnings
        warning_logger.warning("No warnings are reported")
        # log of errors
        error_logger.error("No errors are reported")


if __name__ == "__main__":
    if len(sys.argv) > 1:
        print("Too many command-line arguments")
    else:
        # run code and evaluate performance
        t0 = perf_counter()
        main()
        t1 = perf_counter()
        print("Time elapsed: " + str(t1 - t0))
