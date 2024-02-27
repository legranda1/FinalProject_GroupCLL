Docs
++++

Project General Functions
=========================

This project contains a set of general functions that are used across
different modules for various calculations and logging purposes. These
functions provide essential functionalities for dimensioning
sedimentation and activated sludge tanks in wastewater treatment plants.

Functions Overview
------------------

#. ``x_ss_bs()``

   * *Description:* Calculates the suspended solids concentration in the bottom sludge.
   * *Parameters:* None.
   * *Returns:* Floating-point result in g/L or kg/m\ :sup:`3`.
#. ``x_ss_rs(using="scraper facilities")``

   * *Description:* Calculates the suspended solids concentration in the return sludge using scraper facilities or suction facilities.
   * *Parameters:*

     * ``using``: String indicating the type of facility to be used (default is "scraper facilities").
   * *Returns:* Floating-point result in g/L or kg/m\ :sup:`3`.
#. ``calc_weights(start, end, variable)``

   * *Description:* Calculates initial and final weights of the dimensioning sludge age.
   * *Parameters:*

     * ``start``: Integer representing the starting value in one of the sludge age ranges.
     * ``end``: Integer representing the ending value in one of the sludge age ranges.
     * ``variable``: Floating-point value of the variable to be found its weights.
   * *Returns:* Tuple with dimensionless floating-point results.
#. ``start_logging()``

   * *Description:* Sets up logging formats and log file names for different scenarios.
   * *Parameters:* None.
   * *Returns:* None, but creates three logger objects for logging information, warnings, and errors.
#. ``log_actions(fun)``

   * *Description:* Decorator function to log script execution messages
   * *Parameters:*

     * ``fun``: A function.
   * *Returns:* Result of applying the wrapper function to the corresponding ``fun``.


Project Classes
===============

InputReader Class
-----------------

Description
~~~~~~~~~~~

This class is responsible for reading input data from an Excel file
and storing it in a pandas DataFrame.

Usage
~~~~~

#. *Initialization*: Initialize an ``InputReader`` object with the option to specify the name of the input Excel file.
#. *Input Data Retrieval*: Use the ``get_input_data()`` method to read input data from the Excel file and store it in the ``wwtp_params`` DataFrame.

Class Methods
~~~~~~~~~~~~~

``__init__(self, xlsx_file_name="input_data.xlsx")``

For initializing an ``InputReader`` object with the given attributes
and methods.

* *Parameters*:

  * ``xlsx_file_name`` (optional): String of the corresponding .xlsx file name.
* *Returns*: None.

``get_input_data(self, xlsx_file_name)``

Reads input data from an Excel file and stores it in the ``wwtp_params``
DataFrame.

* *Parameters*:

  * ``xlsx_file_name``: String of the corresponding .xlsx file name.
* *Returns*: None if there is no error, -1 (integer) if there is an error.

PriSed Class
------------

Description
~~~~~~~~~~~

This class was developed by
`Lucas Tardio <https://www.linkedin.com/in/lucas-tardio-ascarrunz-48a70a158/>`_
in order to calculate parameters related to primary
sedimentation tanks in wastewater treatment plants.

Usage
~~~~~

#. *Initialization*: Initialize a ``PriSed`` object.
#. *Primary Surface Calculation*: Use the ``pri_surf()`` method to calculate the surface area of rectangular primary sedimentation tanks.
#. *Cross-Section and Volume Calculation*: Utilize the ``cross_volume()`` method to calculate the cross-section and volume for each rectangular primary sedimentation tank.

Class Methods
~~~~~~~~~~~~~

``__init__(self)``

For initializing a ``PriSed`` object with the given attributes
and methods.

``pri_surf(self)``

Rectangular primary sedimentation tank surface calculation.

* *Returns*: Floating-point result in m\ :sup:`2`.

``cross_volume(self)``

Calculation of cross-section and volume for each rectangular primary
sedimentation tank.

* *Returns*: Tuple with floating-point values of area in m\ :sup:`2`, num_tanks, length in m, width in m, and volume in m\ :sup:`3`.

ActSludge Class
---------------

Description
~~~~~~~~~~~

The ``ActSludge`` class was developed by
`Luis Granda <https://www.linkedin.com/in/luis-emilio-granda/>`_ which
implements methods for the calculation of various
parameters and factors related to activated sludge processes, including
nitrogen and phosphorus removal, sludge production, and oxygen uptake
rates.

Usage
~~~~~

#. *Initialization*: Instantiate an ``ActSludge`` object.
#. *Parameter Calculation*: Utilize the provided methods to calculate specific parameters related to activated sludge processes.

Class Methods
~~~~~~~~~~~~~

``__init__(self)``

Initializes an ``ActSludge`` object with default attributes.

``c_n_iat(self)``

Calculates the total nitrogen input concentration to the activated
sludge tank.

``c_bod5_iat(self)``

Calculates the BOD5 input concentration to the activated sludge tank.

``x_orgn_bm(self)``

Calculates the concentration of organic nitrogen incorporated
in biomass.

``n_bal(self)``

Calculates the nitrogen balance and returns concentrations of
NH\ :sub:`4`-N and NO\ :sub:`3`-N.

``den_ratio(self)``

Calculates the ratio of nitrate nitrogen concentration to BOD\ :sub:`5` input
concentration.

``inter_vd_vat(self)``

Interpolates the corresponding value of "V\ :sub:`d` / V\ :sub:`at`"
for a given target value (denitrification potential).

``s_f(self)``

Calculates the safety factor based on BOD\ :sub:`5` and population
criteria.

``t_ss_aerob_dim(self)``

Calculates the (aerobic) dimensioning sludge age for nitrification.

``t_ss_dim(self)``

Calculates the dimensioning sludge age for nitrification and
denitrification.

``inter_t_ss_dim(self)``

Interpolates the corresponding value of "t_ss_dim" for a given target
value.

``b_d_ss_iat(self)``

Calculates the daily suspended solids input load to the activated
sludge tank.

``x_ss_iat(self)``

Calculates the suspended solids input concentration to the activated
sludge tank.

``ss_bod5_ratio(self)``

Calculates the ratio of suspended solids input concentration and BOD5
input concentration.

``f_t(self)``

Calculates the temperature factor for endogenous respiration.

``sp_d_c(self)``

Calculates the sludge production from carbon removal.

``inter_sp_c_bod(self)``

Interpolates the specific sludge production for a given target value.

``inter_sp_d_c(self)``

Calculates the sludge production from carbon removal by interpolating
the specific sludge production.

``c_p_iat(self)``

Calculates the total phosphorus input concentration to the activated
sludge tank.

``c_p_er(self)``

Searches for effluent requirement for phosphorus according to
respective size class.

``c_p_est(self)``

Calculates total phosphorus effluent concentration to secondary
sedimentation tank.

``x_p_bm(self)``

Calculates phosphorus necessary for the build-up of heterotrophic
biomass.

``x_p_biop(self, anaerobic_tanks=False, inter_rec_sludge=False)``

Calculates excess biological phosphorus removal.

``x_p_prec(self, x_p_biop=False)``

Calculates phosphate to be precipitated.

``sp_d_p(self, precipitant="Fe", x_p_biop=False)``

Calculates sludge production from phosphorus removal.

``sp_d(self)``

Determines sludge production in an activated sludge plant.

``m_ss_at(self)``

Calculates the required mass of suspended solids in the activated
sludge tank.

``v_at(self)``

Calculates the volume of the activated sludge tank.

``v_d(self)``

Calculates the volume of the activated sludge tank used for
denitrification.

``v_n(self)``

Calculates the volume of the activated sludge tank used for
nitrification.

``rc(self)``

Calculates the necessary total recirculation flow ratio (RC) for
pre-anoxic zone denitrification.

``n_d(self)``

Calculates maximum possible efficiency of denitrification.

``ou_d_c(self)``

Calculates oxygen uptake for carbon removal.

``s_no3_iat(self)``

Calculates nitrate input concentration to activated sludge tank.

``ou_d_n(self)``

Calculates oxygen uptake for nitrification.

``ou_d_d(self)``

Calculates oxygen uptake for denitrification.

``inter_fc_fn(self)``

Determines peak factors for the oxygen uptake rate.

``ou_h(self)``

Calculates the oxygen uptake rate for the daily peak.

SecSed Class
------------

Description
~~~~~~~~~~~

This class was developed by
`Camila Alvarado <https://www.linkedin.com/in/camila98/>`_ which provides
methods for calculating various parameters related to secondary
sedimentation tanks in wastewater treatment plants.

Usage
~~~~~

#. *Initialization*: Initialize a ``SecSed`` object.
#. *Suspended Solids Concentration Calculation*: Use the ``x_ss_at()`` method to calculate the suspended solids concentration in the activated sludge tank.
#. *Surface Overflow Rate Calculation*: Utilize the ``q_a()`` method to calculate the surface overflow rate of the secondary sedimentation tank.
#. *Tank Surface Area Calculation*: Use the ``a_st()`` method to calculate the tank surface area and the number of circular tanks required.
#. *Diameter Calculation*: Utilize the ``diam_st()`` method to calculate the diameter of each secondary sedimentation tank.
#. *Zone Depth Calculations*: Use methods ``h2()``, ``h3()``, ``h4()`` to calculate the depths of various zones within the sedimentation tank.
#. *Total Depth Calculation*: Utilize the ``h_tot()`` method to calculate the total depth of the secondary circular sedimentation tank.

Class Methods
~~~~~~~~~~~~~

``__init__(self)``

For initializing a ``SecSed`` object with the given attributes and
methods.

``x_ss_at(self)``

Calculation of suspended solids concentration in the activated sludge
tank.

* *Returns*: Floating-point result in g/L or kg/m\ :sup:`3`.

``q_a(self)``

Calculation of the surface overflow rate of the secondary sedimentation
tank.

* *Returns*: Floating-point result in m/h.

``a_st(self)``

Calculation of tank surface area and number of circular tanks.

* *Returns*: Tuple containing a floating-point result in m\ :sup:`2` and a string indicating the number of circular tanks.

``diam_st(self)``

Calculation of the diameter of each of the secondary sedimentation
tank(s).

* *Returns*: Floating-point result in m.

``h2(self)``

Calculation of the separation and return flow zone.

* *Returns*: Floating-point result in m.

``h3(self)``

Calculation of the density flow and storage zone.

* *Returns*: Floating-point result in m.

``h4(self)``

Calculation of the thickening and sludge removal zone.

* *Returns*: Floating-point result in m.

``h_tot(self)``

Calculation of the total depth of the secondary circular sedimentation
tank.

* *Returns*: Floating-point result in m.

Project Main Module (main.py)
=============================

This module comprises the primary functionality of the project.
Below is a breakdown of the key components and functions:

Functions
---------

#. ``pri_sed_df()``

   * *Description:* Calculates and organizes results of primary sedimentation tank dimensioning into a DataFrame.
   * *Parameters:* None.
   * *Returns:* DataFrame containing dimensioning results with corresponding units.
#. ``sec_sed_df()``

   * *Description:* Calculates and organizes results of secondary sedimentation tank dimensioning into a DataFrame.
   * *Parameters:* None.
   * *Returns:* DataFrame containing dimensioning results with corresponding units.
#. ``act_sludge_df()``

   * *Description:* Calculates and organizes results of activated sludge tank dimensioning into a DataFrame.
   * *Parameters:* None.
   * *Returns:* DataFrame containing dimensioning results with corresponding units.
#. ``main()``

   * *Description:* Main functionality of the script. It generates log files and outputs dimensioning results.
   * *Parameters:* None.
   * *Returns:* None or -1 in case of an error.

Execution
---------

* The script checks for input data. If the input data is not available or incorrect, it logs the event as an error.
* If input data is available, it proceeds to perform dimensioning calculations for primary sedimentation tank, secondary sedimentation tank, and activated sludge tank.
* Dimensioning results are logged and saved into separate Excel files.
* If no warnings or errors occur during the process, it logs that accordingly.
* The performance of the script is evaluated by measuring the time elapsed during execution.
