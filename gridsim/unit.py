"""
.. moduleauthor:: Gillian Basso<gillian.basso@hevs.ch>
.. codeauthor:: Gillian Basso<gillian.basso@hevs.ch>

This module provides a unit management based on pint
(https://pypi.python.org/pypi/Pint/).

*******************************
How to use :mod:`gridsim.units`
*******************************

The unit in Gridsim are used for 'user interface' functions such as
:func:`gridsim.simulation.Simulator.run`, but for improves performance Gridsim
converts all units in SI base unit and uses them as number (int, float, complex).
Therefore some function parameters are float instead of unit especially when
extending Gridsim core (see :ref:`gridsim-core`).

It provides an object call ``units`` which is a wrapper to all useful features
of pint, thus it should used as follow::

    >>> from gridsim.unit import units
    >>> area = 1.2*units.meter * 2.5*units.meter
    >>> print area
    3.0 meter ** 2
    >>> print units.value(area)
    3.0
    >>> print units.dimension(area)
    [length] ** 2
    >>> print units.unit(area)
    meter ** 2

As it is possible to create a measurement by crossing a number value by the unit::

    >>> size1 = 1.2*units.meter

it is also possible to create a measurement in an oriented-object way::

    >>> size2 = units(1.2, units.meter)

and::

    >>> size1 == size2
    True

.. warning:: The second method to create a measurement MUST be used to define
             non standard temperature and SHALL be converted in standard unit
             before sending to the simulator unless
             a ``pint.unit.OffsetUnitCalculusError`` will be raised::

                celsius = units(20, units.degC)                                   # define temperature in degree celsius
                room = sim.thermal.add(ThermalProcess.room('room',
                                           50*units.meter*units.meter,            # define square metre
                                           2.5*units.metre,                       # define metre
                                           units.convert(celsius, units.kelvin))) # convert celsius to kelvin for the simulation

             Also, there is a delta counterpart to specify temperature
             differences. Absolute units have no delta counterpart.
             For example, the change in celsius is equal to the change
             in kelvin, but not in fahrenheit (as the scaling factor is
             different)::

                >>> hysteresis = 2.4*units.delta_degC
                >>> print(hysteresis.to(units.kelvin))
                2.4 kelvin
                >>> print(hysteresis.to(units.delta_degF))
                4.32 delta_degF

.. method:: to_si(unit)

    Returns the SI base unit of the given ``unit``::

        >>> mass = 1000*units.gram
        >>> print units.to_si(mass)
        1.0 kilogram
        >>> print units.to_si(units.kilometre)
        1000.0 meter

    :param value: the value of the measurement
    :type value: int, float
    :param unit: the unit of the measurement
    :type unit: see :ref:`all-unit`

.. method:: units(value, unit)

    Creates a measurement of ``value`` times ``unit``
    Equivalent to::

        value*unit

    :param value: the value of the measurement
    :type value: int, float
    :param unit: the unit of the measurement
    :type unit: see :ref:`all-unit`

.. method:: units.value(measurement)

    Returns the value of the ``measurement`` without any conversion::

        >>> size = 1.2*units.meter
        >>> print units.value(size)
        1.2
        >>> size = 34*units.kilometer
        >>> print units.value(size)
        34

    :returns: the value of the measurement
    :rtype: float

.. method:: units.unit(measurement)

    Returns the unit of the measurement::

        >>> size = 1*units.meter
        >>> print units.unit(size)
        meter
        >>> size = 1*units.kilometer
        >>> print units.unit(size)
        kilometer

    :returns: the unit of the measurement
    :rtype: str

.. method:: units.dimension(measurement)

    Returns the unit of the measurement::

        >>> size = 1*units.meter
        >>> print units.dimension(size)
        [length]
        >>> size = 1*units.kilometer
        >>> print units.dimension(size)
        [length]

    :returns: the unit of the measurement
    :rtype: str

.. method:: units.convert(measurement, unit)

    Converts the ``measurement`` to the unit if possible else raises
    ``pint.unit.DimensionalityError`` exception::

        >>> print units.convert(1*units.metre, units.centimetre)
        100.0 centimeter
        >>> print units.convert(1*units.metre, units.litre)
        [...]
        pint.unit.DimensionalityError: Cannot convert from 'meter' ([length]) to 'liter' ([length] ** 3)

    :returns: the converted measurement
    :rtype: unit

.. _all-unit:

*****************************
Information of existing units
*****************************

Here is a summary of all units that could be used to create a measurement.
This content is based on data of file ``default_en.txt`` of ``pint`` package.

References
==========

The data in **square brackets** ``[]`` are the dimension returned by
:func:`units.dimension`.

* ``meter = [length] = m = metre``
* ``second = [time] = s = sec``
* ``ampere = [current] = A = amp``
* ``candela = [luminosity] = cd = candle``
* ``kilogram = [mass] = kg``
* ``mole = [substance] = mol``
* ``kelvin = [temperature]; offset: 0 = K = degK``
* ``radian = [] = rad``
* ``bit = []``
* ``count = []``

Prefixes
========

Decimal prefixes
----------------

* ``yocto- = 1e-24 = y-``
* ``zepto- = 1e-21 = z-``
* ``atto- =  1e-18 = a-``
* ``femto- = 1e-15 = f-``
* ``pico- =  1e-12 = p-``
* ``nano- =  1e-9  = n-``
* ``micro- = 1e-6  = u-``
* ``milli- = 1e-3  = m-``
* ``centi- = 1e-2  = c-``
* ``deci- =  1e-1  = d-``
* ``deca- =  1e+1  = da-``
* ``hecto- = 1e2   = h-``
* ``kilo- =  1e3   = k-``
* ``mega- =  1e6   = M-``
* ``giga- =  1e9   = G-``
* ``tera- =  1e12  = T-``
* ``peta- =  1e15  = P-``
* ``exa- =   1e18  = E-``
* ``zetta- = 1e21  = Z-``
* ``yotta- = 1e24  = Y-``

Example::

    >>> print units.convert(1*units.yottagram, units.gram)
    1e+24 gram
    >>> print units.convert(1*units.Yg, units.g)
    1e+24 gram

Binary_prefixes
---------------

* ``kibi- = 2**10 = Ki-``
* ``mebi- = 2**20 = Mi-``
* ``gibi- = 2**30 = Gi-``
* ``tebi- = 2**40 = Ti-``
* ``pebi- = 2**50 = Pi-``
* ``exbi- = 2**60 = Ei-``
* ``zebi- = 2**70 = Zi-``
* ``yobi- = 2**80 = Yi-``

Example::

    >>> print units.convert(1*units.kibibit, units.bit)
    1024.0 bit
    >>> print units.convert(1*units.Kibit, units.bit)
    1024.0 bit

Other units
===========

Gridsim units
-------------

Gridsim defines its own units to simplify coding as these special units is used
often times.

* ``heat_capacity = joule/(kilogram*kelvin)``
* ``mass_density = kilogram/(metre*metre*metre)``
* ``thermal_conductivity = watt/(kelvin*metre)``


Acceleration
------------

* ``[acceleration] = [length] / [time] ** 2``

Angle
-----

* ``turn = 2 * pi * radian = revolution = cycle = circle``
* ``degree = pi / 180 * radian = deg = arcdeg = arcdegree = angular_degree``
* ``arcminute = arcdeg / 60 = arcmin = arc_minute = angular_minute``
* ``arcsecond = arcmin / 60 =  arcsec = arc_second = angular_second``
* ``steradian = radian ** 2 = sr``

Area
----

* ``[area] = [length] ** 2``
* ``are = 100 * m**2``
* ``barn = 1e-28 * m ** 2 = b``
* ``cmil = 5.067075e-10 * m ** 2 = circular_mils``
* ``darcy = 9.869233e-13 * m ** 2``
* ``acre = 4046.8564224 * m ** 2 = international_acre``
* ``US_survey_acre = 160 * rod ** 2``

Electromagnetism
----------------

* ``esu = 1 * erg**0.5 * centimeter**0.5 = statcoulombs = statC = franklin = Fr``
* ``esu_per_second = 1 * esu / second = statampere``
* ``ampere_turn = 1 * A``
* ``gilbert = 10 / (4 * pi ) * ampere_turn``
* ``coulomb = ampere * second = C``
* ``volt = joule / coulomb = V``
* ``farad = coulomb / volt = F``
* ``ohm = volt / ampere``
* ``siemens = ampere / volt = S = mho``
* ``weber = volt * second = Wb``
* ``tesla = weber / meter ** 2 = T``
* ``henry = weber / ampere = H``
* ``elementary_charge = 1.602176487e-19 * coulomb = e``
* ``chemical_faraday = 9.64957e4 * coulomb``
* ``physical_faraday = 9.65219e4 * coulomb``
* ``faraday =  96485.3399 * coulomb = C12_faraday``
* ``gamma = 1e-9 * tesla``
* ``gauss = 1e-4 * tesla``
* ``maxwell = 1e-8 * weber = mx``
* ``oersted = 1000 / (4 * pi) * A / m = Oe``
* ``statfarad = 1.112650e-12 * farad = statF = stF``
* ``stathenry = 8.987554e11 * henry = statH = stH``
* ``statmho = 1.112650e-12 * siemens = statS = stS``
* ``statohm = 8.987554e11 * ohm``
* ``statvolt = 2.997925e2 * volt = statV = stV``
* ``unit_pole = 1.256637e-7 * weber``

Energy
------

* ``[energy] = [force] * [length]``
* ``joule = newton * meter = J``
* ``erg = dyne * centimeter``
* ``btu = 1.05505585262e3 * joule = Btu = BTU = british_thermal_unit``
* ``eV = 1.60217653e-19 * J = electron_volt``
* ``thm = 100000 * BTU = therm = EC_therm``
* ``cal = 4.184 * joule = calorie = thermochemical_calorie``
* ``international_steam_table_calorie = 4.1868 * joule``
* ``ton_TNT = 4.184e9 * joule = tTNT``
* ``US_therm = 1.054804e8 * joule``
* ``watt_hour = watt * hour = Wh = watthour``
* ``E_h = 4.35974394e-18 * joule = hartree = hartree_energy``

Force
-----

* ``[force] = [mass] * [acceleration]``
* ``newton = kilogram * meter / second ** 2 = N``
* ``dyne = gram * centimeter / second ** 2 = dyn``
* ``force_kilogram = g_0 * kilogram = kgf = kilogram_force = pond``
* ``force_gram = g_0 * gram = gf = gram_force``
* ``force_ounce = g_0 * ounce = ozf = ounce_force``
* ``force_pound = g_0 * lb = lbf = pound_force``
* ``force_ton = 2000 * force_pound = ton_force``
* ``poundal = lb * feet / second ** 2 = pdl``
* ``kip = 1000*lbf``

Frequency
---------

* ``[frequency] = 1 / [time]``
* ``hertz = 1 / second = Hz = rps``
* ``revolutions_per_minute = revolution / minute = rpm``
* ``counts_per_second = count / second = cps``

Information
-----------

* ``byte = 8 * bit = Bo = octet``
* ``baud = bit / second = Bd = bps``

Length
------

* ``angstrom = 1e-10 * meter``
* ``inch = 2.54 * centimeter = in = international_inch = inches = international_inches``
* ``foot = 12 * inch = ft = international_foot = feet = international_feet``
* ``mile = 5280 * foot = mi = international_mile``
* ``yard = 3 * feet = yd = international_yard``
* ``mil = inch / 1000 = thou``
* ``parsec = 3.08568025e16 * meter = pc``
* ``light_year = speed_of_light * julian_year = ly = lightyear``
* ``astronomical_unit = 149597870691 * meter = au``
* ``nautical_mile = 1.852e3 * meter = nmi``
* ``printers_point = 127 * millimeter / 360 = point``
* ``printers_pica = 12 * printers_point = pica``
* ``US_survey_foot = 1200 * meter / 3937``
* ``US_survey_yard =  3 * US_survey_foot``
* ``US_survey_mile = 5280 * US_survey_foot = US_statute_mile``
* ``rod = 16.5 * US_survey_foot = pole = perch``
* ``furlong = 660 * US_survey_foot``
* ``fathom = 6 * US_survey_foot``
* ``chain = 66 * US_survey_foot``
* ``barleycorn = inch / 3``
* ``arpentlin = 191.835 * feet``
* ``kayser = 1 / centimeter = wavenumber``

Mass
----

* ``dram = oz / 16 = dr = avoirdupois_dram``
* ``ounce = 28.349523125 * gram = oz = avoirdupois_ounce``
* ``pound = 0.45359237 * kilogram = lb = avoirdupois_pound``
* ``stone = 14 * lb = st``
* ``carat = 200 * milligram``
* ``grain = 64.79891 * milligram = gr``
* ``long_hundredweight = 112 * lb``
* ``short_hundredweight = 100 * lb``
* ``metric_ton = 1000 * kilogram = t = tonne``
* ``pennyweight = 24 * gram = dwt``
* ``slug = 14.59390 * kilogram``
* ``troy_ounce = 480 * gram = toz = apounce = apothecary_ounce``
* ``troy_pound = 12 * toz = tlb = appound = apothecary_pound``
* ``drachm = 60 * gram = apdram = apothecary_dram``
* ``atomic_mass_unit = 1.660538782e-27 * kilogram =  u = amu = dalton = Da``
* ``scruple = 20 * gram``
* ``bag = 94 * lb``
* ``ton = 2000 * lb = short_ton``

Textile
-------

* ``denier =  gram / (9000 * meter)``
* ``tex = gram/ (1000 * meter)``
* ``dtex = decitex``

Power
-----

* ``[power] = [energy] / [time]``
* ``watt = joule / second = W = volt_ampere = VA``
* ``horsepower = 33000 * ft * lbf / min = hp = UK_horsepower = British_horsepower``
* ``boiler_horsepower = 33475 * btu / hour``
* ``metric_horsepower =  75 * force_kilogram * meter / second``
* ``electric_horsepower = 746 * watt``
* ``hydraulic_horsepower = 550 * feet * lbf / second``
* ``refrigeration_ton = 12000 * btu / hour = ton_of_refrigeration``

Pressure
--------

* ``[pressure] = [force] / [area]``
* ``Hg = gravity * 13.59510 * gram / centimeter ** 3 = mercury = conventional_mercury``
* ``mercury_60F = gravity * 13.5568 * gram / centimeter ** 3``
* ``H2O = gravity * 1000 * kilogram / meter ** 3 = h2o = water = conventional_water``
* ``water_4C = gravity * 999.972 * kilogram / meter ** 3 = water_39F``
* ``water_60F = gravity * 999.001 * kilogram / m ** 3``
* ``pascal = newton / meter ** 2 = Pa``
* ``bar = 100000 * pascal``
* ``atmosphere = 101325 * pascal = atm = standard_atmosphere``
* ``technical_atmosphere = kilogram * gravity / centimeter ** 2 = at``
* ``torr = atm / 760``
* ``psi = pound * gravity / inch ** 2 = pound_force_per_square_inch``
* ``ksi = kip / inch ** 2 = kip_per_square_inch``
* ``barye = 0.1 * newton / meter ** 2 = barie = barad = barrie = baryd = Ba``
* ``mmHg = millimeter * Hg = mm_Hg = millimeter_Hg = millimeter_Hg_0C``
* ``cmHg = centimeter * Hg = cm_Hg = centimeter_Hg``
* ``inHg = inch * Hg = in_Hg = inch_Hg = inch_Hg_32F``
* ``inch_Hg_60F = inch * mercury_60F``
* ``inch_H2O_39F = inch * water_39F``
* ``inch_H2O_60F = inch * water_60F``
* ``footH2O = ft * water``
* ``cmH2O = centimeter * water``
* ``foot_H2O = ft * water = ftH2O``
* ``standard_liter_per_minute = 1.68875 * Pa * m ** 3 / s = slpm = slm``

Radiation
---------

* ``Bq = Hz = becquerel``
* ``curie = 3.7e10 * Bq = Ci``
* ``rutherford = 1e6*Bq = rd = Rd``
* ``Gy = joule / kilogram = gray = Sv = sievert``
* ``rem = 1e-2 * sievert``
* ``rads = 1e-2 * gray``
* ``roentgen = 2.58e-4 * coulomb / kilogram``

Temperature
-----------

* ``degC = kelvin; offset: 273.15 = celsius``
* ``degR = 5 / 9 * kelvin; offset: 0 = rankine``
* ``degF = 5 / 9 * kelvin; offset: 255.372222 = fahrenheit``

.. warning:: As temperature can have an offset, it could be necessary to :func:`units.convert`
             degree to kelvin to avoid errors.

Delta temperature
-----------------

There is a delta counterpart to specify temperature differences. Absolute
units have no delta counterpart. For example, the change in celsius is equal to
the change in kelvin, but not in fahrenheit (as the scaling factor is
different).

* ``delta_degC``
* ``delta_degF``
* ``kelvin``
* ``rankine``

Time
----

* ``minute = 60 * second = min``
* ``hour = 60 * minute = hr``
* ``day = 24 * hour``
* ``week = 7 * day``
* ``fortnight = 2 * week``
* ``year = 31556925.9747 * second``
* ``month = year/12``
* ``shake = 1e-8 * second``
* ``sidereal_day = day / 1.00273790935079524``
* ``sidereal_hour = sidereal_day/24``
* ``sidereal_minute=sidereal_hour/60``
* ``sidereal_second =sidereal_minute/60``
* ``sidereal_year = 366.25636042 * sidereal_day``
* ``sidereal_month = 27.321661 * sidereal_day``
* ``tropical_month = 27.321661 * day``
* ``synodic_month = 29.530589 * day = lunar_month``
* ``common_year = 365 * day``
* ``leap_year = 366 * day``
* ``julian_year = 365.25 * day``
* ``gregorian_year = 365.2425 * day``
* ``millenium = 1000 * year = millenia = milenia = milenium``
* ``eon = 1e9 * year``
* ``work_year = 2056 * hour``
* ``work_month = work_year/12``

Velocity
--------

* ``[speed] = [length] / [time]``
* ``knot = nautical_mile / hour = kt = knot_international = international_knot = nautical_miles_per_hour``
* ``mph = mile / hour = MPH``
* ``kph = kilometer / hour = KPH``

Viscosity
---------

* ``[viscosity] = [pressure] * [time]``
* ``poise = 1e-1 * Pa * second = P``
* ``stokes = 1e-4 * meter ** 2 / second = St``
* ``rhe = 10 / (Pa * s)``

Volume
------

* ``[volume] = [length] ** 3``
* ``liter = 1e-3 * m ** 3 = l = L = litre``
* ``cc = centimeter ** 3 = cubic_centimeter``
* ``stere = meter ** 3``
* ``gross_register_ton = 100 * foot ** 3 = register_ton = GRT``
* ``acre_foot = acre * foot = acre_feet``
* ``board_foot = foot ** 2 * inch = FBM``
* ``bushel = 2150.42 * inch ** 3 = bu = US_bushel``
* ``dry_gallon = bushel / 8 = US_dry_gallon``
* ``dry_quart = dry_gallon / 4 = US_dry_quart``
* ``dry_pint = dry_quart / 2 = US_dry_pint``
* ``gallon = 231 * inch ** 3 = liquid_gallon = US_liquid_gallon``
* ``quart = gallon / 4 = liquid_quart = US_liquid_quart``
* ``pint = quart / 2 = pt = liquid_pint = US_liquid_pint``
* ``cup = pint / 2 = liquid_cup = US_liquid_cup``
* ``gill = cup / 2 = liquid_gill = US_liquid_gill``
* ``fluid_ounce = gill / 4 = floz = US_fluid_ounce = US_liquid_ounce``
* ``imperial_bushel = 36.36872 * liter = UK_bushel``
* ``imperial_gallon = imperial_bushel / 8 = UK_gallon``
* ``imperial_quart = imperial_gallon / 4 = UK_quart``
* ``imperial_pint = imperial_quart / 2 = UK_pint``
* ``imperial_cup = imperial_pint / 2 = UK_cup``
* ``imperial_gill = imperial_cup / 2 = UK_gill``
* ``imperial_floz = imperial_gill / 5 = UK_fluid_ounce = imperial_fluid_ounce``
* ``barrel = 42 * gallon = bbl``
* ``tablespoon = floz / 2 = tbsp = Tbsp = Tblsp = tblsp = tbs = Tbl``
* ``teaspoon = tablespoon / 3 = tsp``
* ``peck = bushel / 4 = pk``
* ``fluid_dram = floz / 8 = fldr = fluidram``
* ``firkin = barrel / 4``

"""
import os
from pint import UnitRegistry


class _Unit(object):

    def __init__(self):
        """
        Also commented in top of file for website.

        It provides an object call ``units`` which is a wrapper to all useful features
        of pint, thus it should used as follow::

            >>> from gridsim.unit import units
            >>> area = 1.2*units.meter * 2.5*units.meter
            >>> print area
            3.0 meter ** 2
            >>> print units.value(area)
            3.0
            >>> print units.dimension(area)
            [length] ** 2
            >>> print units.unit(area)
            meter ** 2

        As it is possible to create a measurement by crossing a number value by the unit::

            >>> size1 = 1.2*units.meter

        it is also possible to create a measurement in an oriented-object way::

            >>> size2 = units(1.2, units.meter)

        and::

            >>> size1 == size2
            True

        .. warning:: The second method to create a measurement MUST be used to define
                     non standard temperature and SHALL be converted in standard unit
                     before sending to the simulator unless
                     a ``pint.unit.OffsetUnitCalculusError`` will be raised::

                        celsius = units(20, units.degC)                                   # define temperature in degree celsius
                        room = sim.thermal.add(ThermalProcess.room('room',
                                                   50*units.meter*units.meter,            # define square metre
                                                   2.5*units.metre,                       # define metre
                                                   units.convert(celsius, units.kelvin))) # convert celsius to kelvin for the simulation

                     Also, there is a delta counterpart to specify temperature
                     differences. Absolute units have no delta counterpart.
                     For example, the change in celsius is equal to the change
                     in kelvin, but not in fahrenheit (as the scaling factor is
                     different)::

                         >>> hysteresis = 2.4*units.delta_degC
                         >>> print(hysteresis.to(units.kelvin))
                         2.4 kelvin
                         >>> print(hysteresis.to(units.delta_degF))
                         4.32 delta_degF


        """
        self._registry = UnitRegistry(os.path.dirname(__file__)+'/gridsim_en.unit')
        self._registry.define('heat_capacity = J/(kg*K)')
        self._registry.define('mass_density = kg/(m*m*m)')
        self._registry.define('thermal_conductivity = W/(K*m)')

        self._Quantity_class = self._registry.Quantity
        self._Unit_class = self._registry.Quantity

    @property
    def Quantity(self):
        return self._Quantity_class

    @property
    def Unit(self):
        return self._Unit_class

    def __call__(self, *args, **kwargs):
        if len(args) is 1:
            return self._registry(args[0])
        return self._Quantity_class(args[0], args[1])

    def __getattr__(self, item):
        return getattr(self._registry, item)

    def to_si(self, measurement_or_unit):
        if isinstance(measurement_or_unit, self._Quantity_class):
            _measurement = measurement_or_unit.to_base_units()
            return _measurement
        elif isinstance(measurement_or_unit, self._Unit_class):
            _unit = self.unit(self.to_si(1*measurement_or_unit))
            return _unit
        else:
            raise AttributeError('Attribute must be a unit or a measurement not a '+str(type(measurement_or_unit)))

    def value(self, measurement, unit=None):
        if unit is not None:
            _measurement = self.convert(measurement, unit)
        else:
            _measurement = measurement

        if isinstance(_measurement, self._Quantity_class):
            return _measurement.magnitude
        else:
            return _measurement

    def unit(self, measurement):
        if isinstance(measurement, self._Quantity_class):
            return str(measurement.units)
        else:
            return ""

    def dimension(self, measurement):
        if isinstance(measurement, self._Quantity_class):
            return str(measurement.dimensionality)
        else:
            return ""

    def convert(self, m, u):
        if isinstance(m, (int, float)):
            return self._Quantity_class(m, u)
        else:
            return m.to(u)

units = _Unit()
