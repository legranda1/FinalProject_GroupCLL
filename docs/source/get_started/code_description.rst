Code Description
++++++++++++++++

Purpose
=======
An executable python package that can calculate dimensions for the main
parts of a wastewater treatment plant using inflow quantities and
chemical properties.

The main parts and its functions are:

#. `Primary sedimentation tank <https://www.robuschi.com/en-gb/industries/wastewater-treatment/primary-sedimentation#:~:text=Primary%20sedimentation%20removes%20suspended%20solids,in%20the%20liquid%20waste%20stream>`_ for settleable solids.
#. `Activated sludge tank <https://en.wikipedia.org/wiki/Activated_sludge#:~:text=The%20activated%20sludge%20process%20for,from%20the%20clear%20treated%20water>`_ for organic matter removal through aeration and filtration.
#. `Secondary sedimentation tank <https://www.robuschi.com/en-cn/industries/wastewater-treatment/secondary-sedimentation>`_ for biomass separation through settlement.

.. image:: /images/flow_scheme.jpg
    :width: 90%
    :align: center

.. raw:: html

    <p style="text-align:center;">Fig 2. Basic flow scheme of a wastewater treatment plant. (source: Gujer 1999).</p>

.. list-table:: Inflow quantities and chemical properties
    :widths: 20 20 20
    :header-rows: 1

    * - Abbreviation
      - Description
      - Units
    * - Q\ :sub:`d,aM`
      - Daily inflow, annual mean
      - m\ :sup:`3`/d
    * - Q\ :sub:`DW,aM`
      - Dry weather flow as annual mean
      - L/s
    * - Q\ :sub:`DW,2h,max`
      - Maximum dry weather flow as 2 hourly mean
      - L/s
    * - Q\ :sub:`WW,aM`
      - Wastewater flow as annual mean
      - L/s
    * - Q\ :sub:`inf,aM`
      - Infiltration water flow as annual mean
      - L/s
    * - Q\ :sub:`comb`
      - Combined wastewater flow
      - m\ :sup:`3`/d
    * - B\ :sub:`d,BOD5`
      - Daily mean biochemical oxygen demand
      - kg/d
    * - B\ :sub:`d,Ntot`
      - Daily mean total nitrogen load
      - kg/d
    * - B\ :sub:`d,NO3-N`
      - Daily mean nitrate load
      - kg/d
    * - B\ :sub:`d,Ptot`
      - Daily mean phosphate load
      - kg/d
    * - T\ :sub:`dim`
      - Dimensioning temperature
      - °C

Motivation
==========

The ability to design a wastewater treatment plant having only inflow
data and some key biological parameters, skipping the tedious, table
filled, iterative process of which sedimentation tanks and biological
treatment design depend on:

* Discharges have a wide range depending on the population equivalents.
* Biochemical loads have expected unitary values, but will vary in their total quantities (regarding previous point).
* Wide range of tabulated design standards (this varies from country to country), which add tediousness on the path to a size-optimized wastewater treatment plant.

Goals
=====
*Fundamental components*

The ``wwtp_design`` package consists of 8 modules. First, ``data.py``
has been created as a class to import key data values for geometrical
design of a wastewater treatment plant from the input Excel file
``input_data.xlsx``. The list of inflows and chemical properties shown
above will be used in different modules and classes during running
process. Secondly, general functions and global variables (i.e., tables
of the corresponding standard) have been created in ``fun.py`` and
``config.py`` (being this a modifiable module, allowing flexibility,
since regulation values may vary from country to country) respectively.
Thirdly, ``pri_sed.py``, ``sec_sed.py``, and ``act_sludge.py`` are
modules where classes have been created to perform the respective
dimensioning of each tank. Last but not least, in ``main.py`` 3 Excel
files are generated and logged for each of the corresponding stages.

#. ``pri_sed_results.xlsx``
#. ``act_sludge_results.xlsx``
#. ``sec_sed_results.xlsx``

*Auxiliary components*

#. A class inheritance ``ActSludge(InputReader)`` in ``act_sludge.py``.
#. Creation of another class ``PriSed(InputReader)`` in ``pri_sed.py`` that also inherits, so in total there are 4 classes and 2 of them inherit.
#. Log actions files (info, error, and warning).

   * ``info.log``
   * ``error.log``
   * ``warning.log``
#. ``__init__.py`` is created in order to get a package.

Input
-----

The input file looks as shown in figure 3. Discharge values are related
to the inflow coming into the projected wastewater treatment plant.
The chemical parameters as well, will mainly be used in combination
with the limit values at the ``config.py`` to get other variables
required for design. Units must be respected since these will be
further on converted if needed. The ones seen on the input table are
the most common units utilized for these types of calculation.

.. image:: /images/input_data.jpg
    :width: 40%
    :align: center

.. raw:: html

    <p style="text-align:center;">Fig 3. Input data needed for dimensioning. (source: Sindelfingen Wastewater Treatment Plant 2006-2008).</p>


Primary Sedimentation
----------------------

Rectangular tanks will be used for the primary sedimentation designing
process as shown in figure 4.

.. image:: /images/rect_tank.JPG
    :width: 90%
    :align: center

.. raw:: html

    <p style="text-align:center;">Fig 4. Rectangular sedimentation tank. (source: Harald Schoenberger 2022).</p>

The focus of primary treatment of wastewater is to reduce the amount of
settleable solids and grit that may come into the treatment plant and
damage further devices. At figure 5, it can be seen that 90% of
settleable solids can be sedimented within ~45 minutes:

.. image:: /images/efficiency_ps.JPG
    :width: 90%
    :align: center

.. raw:: html

    <p style="text-align:center;">Fig 5. Efficiency of primary sedimentation. (source: ATV-Handbuch 1997a).</p>

For different types of treatments there is an optimal:

.. list-table:: Surface loading (q\ :sub:`a`), retention time, and tank depth
    :widths: 20 20 20 20
    :header-rows: 1

    * - Treatment method
      - q\ :sub:`a` [m / h]
      - t [min]
      - Depth [m]
    * - PS combined with activated sludge process (without excess sludge)
      - 6
      - 15
      - 1.5
    * - PS combined with activated sludge process (with excess sludge)
      - 2 - 3
      - 45
      - 2.0
    * - PS combined with trickling filter or rotating contactors (with / without excess sludge)
      - 3
      - 30
      - 1.5

The package has been written to design WWTPs with activated sludge
process (with addition of excess sludge) and as can be seen in the
retention time, this is exactly 45 minutes, the required to sediment
90% of settleable solids.

Once surface loading (q\ :sub:`a`) is defined (according to the
treatment method) total surface area is calculated with:

A\ :sub:`min` = Q\ :sub:`comb` / q\ :sub:`a`

where:

* A\ :sub:`min` is the total tank surface [ m\ :sup:`2` ]
* Q\ :sub:`comb` is the combined wastewater flow [ m\ :sup:`3` / h ]
* q\ :sub:`a` is the surface loading [ *m / h* ]


The tank surface is the total surface needed for the primary treatment,
it must be divided by the number of tanks, which will always initially
be 2 for the occasion in which one of them needs to be stopped for
maintenance:

A\ :sub:`per tank` = A\ :sub:`min` / N\ :sub:`tanks`

where:

* A\ :sub:`per tank` is the area per rectangular tank [ m\ :sup:`2` ]
* A\ :sub:`min` is the tank surface [ m\ :sup:`2` ]
* N\ :sub:`tanks` is the number of rectangular tanks [ - ]


From the unitary area, an initial width is selected such that the ratio
of width to length is within the established dimensional ratios:

L  = A\ :sub:`per tank` / W

1 m ≤ W ≤ 10 m

1:10 ≤ W:L ≤ 1:5

where:

* L is the length of the rectangular tank [ m ]
* A\ :sub:`per tank` is the area per tank [ m\ :sup:`2` ]
* W is the width of the rectangular tank [ m ]

Width cannot be over 10 meters as a rule, due to travelling bridge
stability.

The smallest ratio (1:10) in combination with the maximum width (10m)
also implicitly limit the maximum surface area per tank, and for this,
the package will automatically add another sedimentation tank and
recalculate dimensions until dimensional ratio between width and length
comply.

Once this finalizes, the total primary sedimentation tank volume is
calculated:

V\ :sub:`min` = N\ :sub:`tanks` · W · D · L

where:

* V\ :sub:`min` is the total tank volume [ m\ :sup:`3` ]
* N\ :sub:`tanks` is the number of rectangular tanks [ - ]
* W is the width of the rectangular tank [ m ]
* D is the depth of the rectangular tank [ m ]
* L is the length of the rectangular tank [ m ]

The result file, ``pri_sed_results.xlsx``, will
look the following way:

.. image:: /images/pri_sed_results.jpg
    :width: 45%
    :align: center

.. raw:: html

    <p style="text-align:center;">Fig 6. Screenshot of primary sedimentation dimensioning output (source: Authors, 2024).</p>

where:

* Tank_surf is the total surface required [ m\ :sup:`2` ]
* Depth is the depth per primary sedimentation tank [ m ]
* Area_per_tank is the area per primary sedimentation tank [ m\ :sup:`2` ]
* Quantity is the number of primary sedimentation tanks [ - ]
* Length is the length per primary sedimentation tank [ m ]
* Width is the width per primary sedimentation tank [ m ]
* Vmin is the minimum volume required [ m\ :sup:`3` ]

Activated Sludge Tank
---------------------

The activated sludge tank will have a pre-denitrification process and a
nitrification process with their respective aeration systems as shown
in the figure 7.

.. image:: /images/act_sludge_tank.jpg
    :width: 100%
    :align: center

.. raw:: html

    <p style="text-align:center;">Fig 7. Parts of Activated Sludge Tank (source: Authors, 2024).</p>

Below is the step-by-step dimensioning according to ATV-DVWK-A 131E
2000 German Standard:

1. Convert data loads to concentrations using the following formula:

C\ :sub:`XXX` or S\ :sub:`XXX` or X\ :sub:`XXX`
= ( B\ :sub:`XXX` / Q\ :sub:`d,aM` ) * 1000

where:

* C\ :sub:`XXX` is the concentration of the parameter XXX in the homogenised sample [ mg / L ]
* S\ :sub:`XXX` is the concentration of the parameter XXX in the filtered sample (0.45 µm membrane filter) [ mg / L ]
* X\ :sub:`XXX` is the concentration of the filter residue (solids), X\ :sub:`XXX` = C\ :sub:`XXX` - S\ :sub:`XXX` [ mg / L ]
* B\ :sub:`XXX` is the load of the parameter XXX [ kg / d ]
* Q\ :sub:`d,aM` is the daily inflow, annual mean [ m\ :sup:`3` / d ]

2. Nitrogen balance must be carried out with the following formulas:

S\ :sub:`NH4,`N` = C\ :sub:`N,IAT` - S\ :sub:`orgN,EST` -
S\ :sub:`NH4,EST` - X\ :sub:`orgN,BM`

where:

* S\ :sub:`NH4,`N` is the concentration of ammonium nitrogen to be nitrified [ mg / L ]
* C\ :sub:`N,IAT` is the concentration of total nitrogen from the influent to the activated sludge tank [ mg / L ]
* S\ :sub:`orgN,EST` is the concentration of organic nitrogen from the effluent of the secondary sedimentation tank [ mg / L ]
* S\ :sub:`NH4,EST` is the concentration of ammonium nitrogen from the effluent of the secondary sedimentation tank [ mg / L ]
* X\ :sub:`orgN,BM` is the concentration of phosphorus embedded in the biomass [ mg / L ]

S\ :sub:`NO3,D` = S\ :sub:`NH4,N` - S\ :sub:`NO3,EST`

where:

* S\ :sub:`NO3,D` is the concentration of nitrate nitrogen to be denitrified [ mg / L ]
* S\ :sub:`NH4,N` is the concentration of ammonium nitrogen to be nitrified [ mg / L ]
* S\ :sub:`NO3,EST` is the concentration of nitrate nitrogen from the effluent of the secondary sedimentation tank [  mg / L ]

3. Determination of V\ :sub:`D` / V\ :sub:`AT` by calculating
S\ :sub:`N03,D` / C\ :sub:`BOD,IAT` and using the table below:

.. list-table:: S\ :sub:`N03,D` / C\ :sub:`BOD,IAT`
    :widths: 20 20 20
    :header-rows: 1

    * - V\ :sub:`D` / V\ :sub:`AT`
      - Pre-anoxic zone denitrification and comparable processes
      - Simultaneous and intermittent denitrification
    * - 0.2
      - 0.11
      - 0.06
    * - 0.3
      - 0.13
      - 0.09
    * - 0.4
      - 0.14
      - 0.12
    * - 0.5
      - 0.15
      - 0.15

where:

* V\ :sub:`D` is the volume of the activated sludge tank used for denitrification [ m\ :sup:`3` ]
* V\ :sub:`AT` is the volume of the activated sludge tank [ m\ :sup:`3`]

4. Calculation of the required sludge age using the following formulas:

t\ :sub:`SS,aerob,dim` = SF · 3.4 · 1.103\ :sup:`( 15 - T )`

where:

* t\ :sub:`SS,aerob,dim` is the aerobic sludge age upon which dimensioning for nitrification is based  [ d ]
* SF is the safety factor for nitrification [ - ]
* T is the temperature for dimensioning [ °C ]

Considering also *denitrification*:

t\ :sub:`SS,dim` = t\ :sub:`SS,aerob,dim` · [ 1 ] / [ 1 -
( V\ :sub:`D` / V\ :sub:`AT` ) ]

where:

* t\ :sub:`SS,dim` is the sludge age upon which dimensioning is based [ d ]
* t\ :sub:`SS,aerob,dim` is the aerobic sludge age upon which dimensioning for nitrification is based  [ d ]
* V\ :sub:`D` / V\ :sub:`AT` is the volume ratio from the denitrification tank to activated sludge tank [ - ]

Alternatively, the following table can be used to find the required
sludge age.

.. list-table:: T and B\ :sub:`d,BOD,I`
    :widths: 20 20 20 20 20 20
    :header-rows: 1

    * - Treatment target
      - V\ :sub:`D` / V\ :sub:`AT`
      - 10 °C - up to 1200 kg/d
      - 12 °C - up to 1200 kg/d
      - 10 °C - over 6000 kg/d
      - 12 °C - over 6000 kg/d
    * - Without nitrification
      -
      - 5.0
      - 5.0
      - 4.0
      - 4.0
    * - With nitrification
      -
      - 10.0
      - 8.2
      - 8.0
      - 6.6
    * - Nitrification and denitrification
      - 0.2
      - 12.5
      - 10.3
      - 10.0
      - 8.3
    * - Nitrification and denitrification
      - 0.3
      - 14.3
      - 11.7
      - 11.4
      - 9.4
    * - Nitrification and denitrification
      - 0.4
      - 16.7
      - 13.7
      - 13.3
      - 11.0
    * - Nitrification and denitrification
      - 0.5
      - 20.0
      - 16.4
      - 16.0
      - 13.2
    * - Sludge stabilization including nitrogen removal
      -
      - 25.0
      - 25.0
      -
      -

where:

* T is the temperature for dimensioning [ °C ]
* B\ :sub:`d,BOD,I` is the daily BOD\ :sub:`5` load from influent to the wastewater treatment plan [ kg / d ]
* (V\ :sub:`D` / V\ :sub:`AT`) is the volume ratio from the denitrification tank to activated sludge tank [ - ]

5. Calculation of total excess sludge production by following these
steps:

First, the Inhabitant-SS load is extracted from the table below,
a retention time after primary sedimentation of 0.5 to 1 h is
sufficient. Remember to transform it to concentration.

.. list-table:: Inhabitant-specific loads [ *g / (I * d)* ]
    :widths: 20 20 20 20
    :header-rows: 1

    * - Parameter
      - Raw wastewater
      - 0.5 to 1.0 h of retention time after PS
      - 1.5 to 2.0 h of retention time after PS
    * - BOD\ :sub:`5`
      - 60
      - 45
      - 40
    * - COD
      - 120
      - 90
      - 80
    * - SS
      - 70
      - 35
      - 25
    * - TKN
      - 11
      - 10
      - 10
    * - P
      - 1.8
      - 1.6
      - 1.6

where:

* BOD\ :sub:`5` stands for biochemical oxygen demand
* COD stands for chemical oxygen demand
* SS stands for suspended solids
* TKN stands for total Kjeldahl nitrogen
* P stands for phosphorous

Second, calculation of the temperature factor for endogenous
respiration:

F\ :sub:`T` =  1.072\ :sup:`( T - 15 )`

where:

* F\ :sub:`T` is a temperature factor [ - ]
* T is the temperature for dimensioning [ °C  ]

Third, calculation of the sludge production from carbon removal:

SP\ :sub:`d,C` = B\ :sub:`d,BOD` ·  { [0.75] + [ 0.6 ·
( X\ :sub:`SS,IAT` / C\ :sub:`BOD,IAT` ) ] -
[ ( (1-0.2) · 0.17 · 0.75 · t\ :sub:`ss,dim` ·  F\ :sub:`T` ) /
( 1 + 0.17  ·  t\ :sub:`ss,dim` ·  F\ :sub:`T` ) ] }

where:

* SP\ :sub:`d,C` is the daily sludge production from carbon removal [ kg / d ]
* B\ :sub:`d,BOD` is the daily BOD\ :sub:`5` load [ kg / d ]
* X\ :sub:`SS,IAT` is the concentration of suspended solids from the influent to the activated sludge tank [ mg / L ]
* C\ :sub:`BOD,IAT` is the concentration of BOD\ :sub:`5` from the influent to the activated sludge tank [ mg / L ]
* t\ :sub:`ss,dim`  is the sludge age upon which dimensioning is based [ d ]
* F\ :sub:`T` is a temperature factor [ - ]

Alternatively, the following table can be used to find the specific
sludge production SP\ :sub:`C,BOD` [ kg SS / kg BOD\ :sub:`5` ]
at 10° to 12° C, and, then, multiply by the influent BOD\ :sub:`5`
load to find the sludge production from carbon removal.

.. list-table:: Sludge age [ d ]
    :widths: 20 20 20 20 20 20 20
    :header-rows: 1

    * - X\ :sub:`SS,IAT` / C\ :sub:`BOD,IAT`
      - 4
      - 8
      - 10
      - 15
      - 20
      - 25
    * - 0.4
      - 0.79
      - 0.69
      - 0.65
      - 0.59
      - 0.56
      - 0.53
    * - 0.6
      - 0.91
      - 0.81
      - 0.77
      - 0.71
      - 0.68
      - 0.65
    * - 0.8
      - 1.03
      - 0.93
      - 0.89
      - 0.83
      - 0.80
      - 0.77
    * - 1.0
      - 1.15
      - 1.05
      - 1.01
      - 0.95
      - 0.92
      - 0.89
    * - 1.2
      - 1.27
      - 1.17
      - 1.13
      - 1.07
      - 1.04
      - 1.01

where:

* X\ :sub:`SS,IAT` is the concentration of suspended solids from the influent to the activated sludge tank [ mg / L ]
* C\ :sub:`BOD,IAT` s the concentration of BOD<sub>5</sub> from the influent to the activated sludge tank  [ mg / L ]

Next, the phosphorus balance is calculated by first extracting the
C\ :sub:`P,EST` according to the size class in the following table:

.. list-table:: Concentrations according to the size class
    :widths: 20 20 20 20 20 20
    :header-rows: 1

    * - Size class
      - COD [ mg / L ]
      - BOD [ mg / L ]
      - NH\ :sub:`4`-N [ mg / L ]
      - N\ :sub:`tot` [ mg / L ]
      - P\ :sub:`tot` [ mg / L ]
    * - 1 (< 60 kgBOD\ :sub:`5`/d in raw water)
      - 150
      - 40
      -
      -
      -
    * - 2 (60 - 300 kgBOD\ :sub:`5`/d in raw water)
      - 110
      - 25
      -
      -
      -
    * - 3 (300 - 600 kgBOD\ :sub:`5`/d in raw water)
      - 90
      - 20
      - 10
      -
      -
    * - 4 (600 - 6000 kgBOD\ :sub:`5`/d in raw water)
      - 90
      - 20
      - 10
      - 18
      - 2
    * - 5 (> 6000 kgBOD\ :sub:`5`/d in raw water)
      - 75
      - 15
      - 10
      - 13
      - 1

X\ :sub:`P,Prec` = C\ :sub:`P,IAT` - C\ :sub:`P,EST` -
X\ :sub:`P,BM` - X\ :sub:`P,BioP`

where:

* X\ :sub:`P,Prec` is the concentration of phosphorus removed by simultaneous precipitation [ mg / L ]
* C\ :sub:`P,IAT` is the concentration of phosphorus from the influent to the activated sludge tank [ mg / L ]
* C\ :sub:`P,EST` is the concentration of phosphorus from the effluent of the secondary sedimentation tank [ mg / L ]
* X\ :sub:`P,BM` is the concentration of phosphorus embedded in the biomass [ mg / L ]
* X\ :sub:`P,BioP` is the concentration of phosphorus removed with biological excess phosphorus removal process [ mg / L ]

Now, the excess sludge production is calculated from the phosphorous
removal.

SP\ :sub:`d,P` =  { [ Q\ :sub:`DW` ] · [ ( 3 · X\ :sub:`P,BioP`
) + (6.8 · X\ :sub:`P,Prec,Fe`  ) + (5.3 · X\ :sub:`P,Prec,Al` ) ]
} / { 1000 }

where:

* SP\ :sub:`d,P` is the daily sludge production from phosphorus removal [ kg / d ]
* Q\ :sub:`DW` is the wastewater inflow with dry weather [ m\ :sup:`3` / d ]
* X\ :sub:`P,BioP` is the concentration of phosphorus removed with biological excess phosphorus removal process [ mg / L ]
* X\ :sub:`P,Prec,Fe` is the concentration of phosphorus removed by simultaneous precipitation using iron [ mg / L ]
* X\ :sub:`P,Prec,Al` is the concentration of phosphorus removed by simultaneous precipitation using aluminium [ mg / L ]

Finally, the total excess sludge production is calculated:

SP\ :sub:`d` = SP\ :sub:`d,C` + SP\ :sub:`d,P`

where:

* SP\ :sub:`d` is the sludge produced in an activated sludge plant [ kg / d ]
* SP\ :sub:`d,C` is the daily sludge production from carbon removal [ kg / d ]
* SP\ :sub:`d,P` is the daily sludge production from phosphorus removal [ kg / d ]

6. Calculation of the mass of suspended solids in the activated sludge
tank:

M\ :sub:`SS,AT` = t\ :sub:`SS,dim` · SP\ :sub:`d`

where:

* M\ :sub:`SS,AT` is the mass of suspended solids in the activated sludge tank [ kg ]
* t\ :sub:`SS,dim` is the sludge age upon which dimensioning is based [ d ]
* SP\ :sub:`d` is the sludge produced in an activated sludge plant [ kg / d ]

7. Calculation of required tank volumes:

V\ :sub:`AT`  = M\ :sub:`SS,AT`/ SS\ :sub:`AT`

where:

* V\ :sub:`AT` is volume of the activated sludge tank [ m\ :sup:`3` ]
* M\ :sub:`SS,AT` is the mass of suspended solids in the activated sludge tank [ kg ]
* SS\ :sub:`AT` is the suspended solids concentration in the activated sludge tank [ kg / m\ :sup:`3` ]

V\ :sub:`D` = ( V\ :sub:`D` / V\ :sub:`AT` ) · V\ :sub:`AT`

where:

* V\ :sub:`D` / V\ :sub:`AT` is the volume ratio from the denitrification tank to activated sludge tank [ - ]
* V\ :sub:`AT` is volume of the activated sludge tank [ m\ :sup:`3` ]

V\ :sub:`N` =  V\ :sub:`AT` - V\ :sub:`D`

where:

* V\ :sub:`N` is the volume of the activated sludge tank used for nitrification [ m\ :sup:`3` ]
* V\ :sub:`AT` is volume of the activated sludge tank [ m\ :sup:`3` ]
* V\ :sub:`D` is the volume of the activated sludge tank used for denitrification [ m\ :sup:`3` ]

8. Calculation of the total recirculation ratio at pre-anoxic zone
denitrification process:

RC = [ ( S\ :sub:`NH4,N` ) /  ( S\ :sub:`NO3,EST` ) ] - [ 1 ]

where:

* RC is the total recirculation ratio at pre-anoxic zone denitrification process [ - ]
* S\ :sub:`NH4,N`  is the concentration of ammonium nitrogen to be nitrified [ mg / L ]
* S\ :sub:`NO3,EST` is the concentration of nitrate nitrogen from the effluent of the secondary sedimentation tank [ mg / L ]

n\ :sub:`D` ≤  [ 1 ] - [ ( 1 ) / ( 1 + RC ) ]

where:

* n\ :sub:`D` is he maximum possible efficiency of denitrification [ - ]
* RC is the total recirculation ratio at pre-anoxic zone denitrification process [ - ]

9. Calculation of f\ :sub:`C` and f\ :sub:`N` by using the table
below:

.. list-table:: Sludge age [d]
    :widths: 20 20 20 20 20 20 20
    :header-rows: 1

    * - Peak factors
      - 4
      - 6
      - 8
      - 10
      - 15
      - 25
    * - f\ :sub:`C` and f\ :sub:`N`
      - 1.30
      - 1.25
      - 1.20
      - 1.20
      - 1.15
      - 1.10
    * - f\ :sub:`N`  for <= 1200 kgBOD\ :sub:`5` / d
      -
      -
      -
      - 2.50
      - 2.00
      - 1.50
    * - f\ :sub:`N`  for >= 6000 kgBOD\ :sub:`5` / d
      -
      -
      - 2.00
      - 1.80
      - 1.50
      -

10. Design of aeration system:

OU\ :sub:`d,C` = { B\ :sub:`d,BOD` }  · { [ 0.56 ] +
[ ( 0.15 · t\ :sub:`SS,dim` · F\ :sub:`T` ) /
( 1 + 0.17  · t\ :sub:`SS,dim` · F\ :sub:`T` ) ] }

where:

* OU\ :sub:`d,C` is the daily oxygen uptake for carbon removal [ ( kg O\ :sub:`2` ) / d ]
* B\ :sub:`d,BOD` is the daily BOD\ :sub:`5` load [ kg / d ]
* t\ :sub:`SS,dim` is the sludge age upon which dimensioning is based [ d ]
* F\ :sub:`T` is a temperature factor [ - ]

OU\ :sub:`d,N` = [ ( Q\ :sub:`DW` ) · ( 4.3 )  ·
( S\ :sub:`NO3,D` - S\ :sub:`NO3,IAT` + S\ :sub:`NO3,EST` ) ]
/ [ 1000 ]

where:

* OU\ :sub:`d,N` is the daily oxygen uptake for nitrification [ ( kg O\ :sub:`2` ) / d ]
* Q\ :sub:`DW` is the wastewater inflow with dry weather [ m\ :sup:`3` / d ]
* S\ :sub:`NO3,D` is the concentration of nitrate nitrogen to be denitrified [ mg / L ]
* S\ :sub:`NO3,IAT` is the concentration of nitrate nitrogen from the influent to the activated sludge tank [ mg / L ]
* S\ :sub:`NO3,EST` is the concentration of nitrate nitrogen from the effluent of the secondary sedimentation tank [ mg / L ]

OU\ :sub:`d,D` = [ ( Q\ :sub:`DW` )  · ( 2.9 ) ·
( S\ :sub:`NO3,D` ) ] / [ 1000 ]

where:

* OU\ :sub:`d,D` is the daily oxygen uptake for carbon removal which is covered by denitrification [ ( kg O\ :sub:`2` ) / d ]
* Q\ :sub:`DW` is the wastewater inflow with dry weather [ m\ :sup:`3` / d ]
* S\ :sub:`NO3,D` is the concentration of nitrate nitrogen to be denitrified [ mg / L ]

OU\ :sub:`h` = [ ( f\ :sub:`C` ) · ( OU\ :sub:`d,C` -
OU\ :sub:`d,D` )   +   ( f\ :sub:`N` ) · OU\ :sub:`d,N` ) ]
/ [ 24 ]

where:

* OU\ :sub:`h` is the hourly oxygen uptake rate [ ( kg O\ :sub:`2` ) / d ]
* f\ :sub:`C` is the peak factor for carbon respiration [ - ]
* f\ :sub:`N` is the peak  factor for ammonium oxidation  [ - ]
* OU\ :sub:`d,C` is the daily oxygen uptake for carbon removal [ ( kg O\ :sub:`2` ) / d ]
* OU\ :sub:`d,D` Daily oxygen uptake for carbon removal which is covered by denitrification [ ( kg O\ :sub:`2` ) / d ]
* OU\ :sub:`d,N` is the daily oxygen uptake for nitrification [ ( kg O\ :sub:`2` ) / d ]

Below is a screenshot of the output that would be obtained in a .xlsx
file if everything runs smoothly:

.. image:: /images/act_sludge_result.jpg
    :width: 40%
    :align: center

.. raw:: html

    <p style="text-align:center;">Fig 8. Activated sludge dimensioning output (source: Authors, 2024).</p>

where:

* C_BOD5_IAT is the concentration of BOD\ :sub:`5` from the influent to the activated sludge tank  [ mg / L ]
* C_N_IAT is the concentration of total nitrogen from the influent to the activated sludge tank [ mg / L ]
* S_orgN_EST is the concentration of organic nitrogen from the effluent of the secondary sedimentation tank [ mg / L ]
* S_NH4_EST is the concentration of ammonium nitrogen from the effluent of the secondary sedimentation tank [ mg / L ]
* X_orgN_BM is the concentration of organic nitrogen embedded in the biomass [ mg / L ]
* S_NH4_N is the concentration of ammonium nitrogen to be nitrified [ mg / L ]
* S_NO3_EST is the concentration of nitrate nitrogen from the effluent of the secondary sedimentation tank [ mg / L ]
* S_NO3_D is the concentration of nitrate nitrogen to be denitrified [ mg / L ]
* V_D/V_AT is the volume ratio, denitrification tank to aeration tank [ - ]
* SF is the safety factor for nitrification [ - ]
* T is the temperature for dimensioning [ °C ]
* t_SS_aerob_dim is the aerobic sludge age upon which dimensioning for nitrification is based [ days ]
* t_SS_dim is the sludge age upon which dimensioning is based [ days ]
* X_SS_IAT is the suspended solids concentration from the influent to the activated sludge tank [ mg / L ]
* F_T is the temperature factor for endogenous respiration [ - ]
* SP_d_C is the daily sludge production from carbon removal [ kg / d ]
* C_P_IAT is the concentration of phosphorus from the influent to the activated sludge tank [ mg / L ]
* C_P_EST is the concentration of phosphorus from the effluent of the secondary sedimentation tank [ mg / L ]
* X_P_BM is the concentration of phosphorus embedded in the biomass [ mg / L ]
* X_P_Prec is the concentration of phosphorus removed by simultaneous precipitation [ mg / L ]
* SP_d_P is the daily sludge production from phosphorus removal [ kg / d ]
* SP_d is the daily waste activated sludge production (solids) [ kg / d ]
* M_SS_AT is the mass of suspended solids in the activated sludge tank [ kg ]
* X_SS_AT is the suspended solids concentration in the activated sludge tank [ g / L ]
* V_AT is the volume of the activated sludge tank [ m\ :sup:`3` ]
* V_D is the volume of activated sludge tank destined to denitrification [ m\ :sup:`3` ]
* V_N is the volume of activated sludge tank destined to nitrification [ m\ :sup:`3` ]
* RC is the total recirculation ratio at pre-anoxic zone denitrification process [ - ]
* n_D is the maximum denitrification efficiency [ - ]
* OU_d_C is the daily oxygen uptake for carbon removal [ kgO\ :sub:`2` / d ]
* S_NO3_IAT is the concentration of nitrate nitrogen from the influent to the activated sludge tank [ mg / L ]
* OU_d_N is the daily oxygen uptake for nitrification [ kgO\ :sub:`2` / d ]
* OU_d_D is the daily oxygen uptake for carbon removal which is covered by denitrification [ kgO\ :sub:`2` / d ]
* f_C is the peak factor for carbon respiration [ - ]
* f_N is the peak factor for ammonium oxidation [ - ]
* OU_h is the oxygen uptake rate (hourly)  [ kgO\ :sub:`2` / h ]

Secondary Sedimentation
-----------------------

The design of the secondary sedimentation tank was made considering the
following criteria: circular tanks with
`horizontal flow <https://clearwaterind.com/how-sedimentation-water-treatment-works-and-how-to-make-it-efficient/#:~:text=Horizontal%20Flow%20Tank,the%20bottom%20of%20the%20tank.>`_
and
`scraper facilities <https://mena-water.com/products/circular-tank-scraper/#:~:text=Rotating%20Circular%20scrapers%20are%20designed,are%20collected%20by%20the%20skimmer.>`_
as shown in figure 9.

.. image:: /images/horizontal_flow.jpg
    :width: 100%
    :align: center

.. raw:: html

    <p style="text-align:center;">Fig 9. Main directions of flow and functional tank zones of horizontal flow circular secondary sedimentation tanks. (source: ATV-DVWK-A 131E 2000).</p>

Below is the step-by-step dimensioning according to ATV-DVWK-A 131E
2000 German Standard:

1. From the table below the
`SVI <https://en.wikipedia.org/wiki/Sludge_volume_index#:~:text=It%20is%20defined%20as%20'the,*%201000%20(mg%2Fg)>`_
(Sludge Volume Index) is extracted according to the design criteria, in
our case a nitrification and denitrification target treatment will be
performed. Plus, it is recommended to take an average value.

.. list-table:: SVI
    :widths: 20 20 20
    :header-rows: 1

    * - Treatment target
      - Favourable (ml/g)
      - Unfavourable (ml/g)
    * - Without nitrification
      - 100 - 150
      - 120 - 180
    * - Nitrification and denitrification
      - 100 - 150
      - 120 - 180
    * - Sludge stabilization
      - 75 - 120
      - 100 - 150


2. Now, the thickening time must be extracted according to the type of
treatment, with denitrification in our case. From experience, it is
advisable to choose the minimum values of the range because with long
time sludge flocs degrades, gas bubbles are formed, and, therefore,
sludge rises.

.. list-table:: Thickening time
    :widths: 20 20
    :header-rows: 1

    * - Type of wastewater treatment
      - Thickening time (h)
    * - Activated sludge plants without nitrification
      - 1.5 - 2.0
    * - Activated sludge plants with nitrification
      - 1.0 - 1.5
    * - Activated sludge plants with denitrification
      - 2.0 - (2.5)

3. Calculation of the suspended solids concentration in
the bottom sludge, return sludge, and activated sludge tank:

SS\ :sub:`BS` = ( 1000 / SVI ) · t\ :sub:`Th`\ :sup:`1/3`

where:

* SS\ :sub:`BS` is the suspended solids concentration in the bottom sludge [ g / L ]
* SVI is the sludge volume index [ mL/ g ]
* t\ :sub:`Th` is the thickening time [ h ]

SS\ :sub:`RS` = 0.7 · SS\ :sub:`BS`

where:

* SS\ :sub:`RS` is the suspended solids concentration of the return sludge  [ g / L ]
* SS\ :sub:`BS` is the suspended solids concentration in the bottom sludge [ g / L ]

SS\ :sub:`AT` = ( RS · SS\ :sub:`RS` ) / ( 1 + RS )

where:

* SS\ :sub:`AT` is the suspended solids concentration in the activated sludge tank  [ g / L ]
* SS\ :sub:`RS` is the suspended solids concentration in the bottom sludge [ g / L ]
* RS is the return sludge ratio always 0.75 [ - ]

4. Calculation of the surface overflow rate and tank surface area:

q\ :sub:`A` = q\ :sub:`SV` / DSV

where:

* q\ :sub:`A` is the surface overflow rate  [ m / h ]
* q\ :sub:`SV` is the sludge volume loading rate [ L / ( m\ :sup:`2` · h ) ]

  * q\ :sub:`SV` ≤ 500  for  [ L / ( m\ :sup:`2` · h ) ] for X\ :sub:`SS,EST` ≤ 20 [ mg / L ]
* DSV is the diluted sludge volume [ mL / L ]

  * DSV = SS\ :sub:`AT`  ·  SVI

    * SS\ :sub:`AT` is the suspended solids concentration in the activated sludge tank [ g / L ]
    * SVI is the sludge volume index [ mL / g ]

A\ :sub:`ST` = Q\ :sub:`comb` / q\ :sub:`A`

where:

* A\ :sub:`ST` is the secondary sedimentation tank surface area [ m\ :sup:`2` ]
* Q\ :sub:`comb` is the combined wastewater flow [ m\ :sup:`3` / h ]
* q\ :sub:`A` is the surface overflow rate [ m / h ]

5. Calculation of the different depths in the secondary sedimentation
tank:

h\ :sub:`1` = 0.5

where:

* h\ :sub:`1` is the clean water zone it is a safety zone with a minimum depth of 0.5 [ m ]

h\ :sub:`2` =
[ 0.5 · q\ :sub:`A` · ( 1 + RS ) ] / [ 1 - ( DSV / 1000 ) ]

where:

* h\ :sub:`2` is the separation/return flow zone [ m ]
* q\ :sub:`A` is the surface overflow rate [ m / h ]
* RS is the return sludge ratio always 0.75 [ - ]
* DSV is the diluted sludge volume [ mL / L ]

h\ :sub:`3` =
[ 1.5 · 0.3 · q\ :sub:`SV` · ( 1 + RS ) ] / [ 500 ]

where:

* h\ :sub:`3` is the density flow and storage zone [ m ]
* RS is the return sludge ratio always 0.75 [ - ]
* q\ :sub:`SV` is the sludge volume loading rate [ L / ( m\ :sub:`2` · h ) ]

h\ :sub:`4` = [ SS\ :sub:`AT`  · q\ :sub:`A` ·
( 1 + RS ) · t\ :sub:`Th`  ] / [ SS\ :sub:`BS` ]*

where:

* h\ :sub:`4` is the thickening and sludge removal zone [ m ]
* SS\ :sub:`AT` is the suspended solids concentration in the activated sludge tank  [ g / L ]
* q\ :sub:`A` is the surface overflow rate [ m / h ]
* RS is the return sludge ratio always 0.75 [ - ]
* t\ :sub:`Th` is the thickening time [ h ]
* SS\ :sub:`BS` is the suspended solids concentration in the bottom sludge [ g / L ]

h\ :sub:`tot` = h\ :sub:`1` +  h\ :sub:`2` +  h\ :sub:`3` +  h\ :sub:`4`

where:

* h\ :sub:`1` is the clean water zone  [ m ]
* h\ :sub:`2` is the separation/return flow zone [ m ]
* h\ :sub:`3` is the density flow and storage zone [ m ]
* h\ :sub:`4` is the thickening and sludge removal zone [ m ]

Below is a screenshot of the output that would be obtained in a .xlsx
file if everything runs smoothly:

.. image:: /images/sec_sed_results.jpg
    :width: 40%
    :align: center

.. raw:: html

    <p style="text-align:center;">Fig 10. Secondary sedimentation dimensioning output (source: Authors, 2024)</p>

where:

* SVI is the sludge volume index  [ mL / g ]
* t_TH is the thickening time of the sludge in the secondary sedimentation tank [ h ]
* X_SS_BS is the suspended solids concentration in the bottom sludge of secondary sedimentation tanks [ g / L ]
* X_SS_RS is the suspended solids concentration of the return (activated) sludge [ g / L ]
* X_SS_AT is the suspended solids concentration in the activated sludge tank [ g / L ]
* q_SV is the sludge volume surface loading rate of secondary sedimentation tanks [ L / ( m\ :sup:`2` · h )  ]
* q_A is the surface overflow rate of secondary sedimentation tanks [ m / h ]
* A_ST is the surface area of secondary sedimentation tanks [ m\ :sup:`2` ]
* Quantity is the number of circular secondary sedimentation tanks required [ - ]
* Diameter is the tank diameter [ m ]
* h1 is the depth of the clear water zone in secondary sedimentation tanks [ m ]
* h2 is the depth of the separation zone / return flow zone in secondary sedimentation tanks [ m ]
* h3 is the depth of the density flow and storage zone in secondary sedimentation tanks [ m ]
* h4 is the depth of the sludge thickening and removal zone in secondary sedimentation tanks [ m ]
* h_tot is the total water depth in the secondary sedimentation tank (sum of previous 4 heights) [ m ]
