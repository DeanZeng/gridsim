"""
.. moduleauthor:: Michael Clausen (clm@hevs.ch)

The thermal simulation module offers a very abstract thermal simulation. The
simulation is based on the thermal capacity of a thermal process (envelope)
and the energy flows between those processes via thermal couplings that result
as consequence of the temperature differences between the thermal processes and
the thermal conductivity of the couplings between them.

*Example*:

.. literalinclude:: ../../demos/thermal.py
    :linenos:

* On line 7 we create a new simulation.
* On lines 17 to 19 we create a very simple thermal process with one room and
    the outside temperature from a data file.
* On line 22 we create a plot recorder and on line 23 we record all temperatures
    using the plot recorder.
* On line 26 & 27 we initialize the simulation and start the simulation for the
    month avril with a resolution of 1 hour.
* On line 30 we save the figure.

The figure looks like this one:

.. figure:: ./figures/thermal-example.png
            :align: center

"""
from gridsim.decorators import accepts
from gridsim.util import Air, Position
from gridsim.unit import units
from gridsim.core import AbstractSimulationElement


class AbstractThermalElement(AbstractSimulationElement):

    @accepts((1, str),
             (2, Position))
    def __init__(self, friendly_name, position=Position()):
        """
        Base class of all elements which can be part of a thermal simulation.

        :param friendly_name: User friendly name to give to the element.
        :type friendly_name: str

        :param position: The position of the thermal element.
            Defaults to [0,0,0].
        :type position: :class:`Position`
        """
        super(AbstractThermalElement, self).__init__(friendly_name)

        self._position = position

    @property
    def position(self):
        """
        Returns the thermal simulation element's position.

        :returns: Position of the element.
        """
        return self._position


class ThermalProcess(AbstractThermalElement):

    @accepts((1, str),
             (5, Position))
    def __init__(self, friendly_name,
                 thermal_capacity, initial_temperature, mass=1*units.kilogram,
                 position=Position()):
        """
        The very basic element of a thermal simulation. A thermal process
        represents a closed thermal envelope like a room or a amount of
        matter which has an uniform thermal capacity and and stores an amount of
        thermal energy resulting in a temperature. Those thermal processes
        can be coupled by :class:`ThermalCoupling` elements.

        :param friendly_name: The name to give to the thermal process.
        :type friendly_name: str

        :param thermal_capacity: The thermal capacity of the process.
            See :class:`Material`.
        :type thermal_capacity: heat_capacity

        :param initial_temperature: The initial temperature of the process in
            degrees.
        :type initial_temperature: kelvin

        :param position: The position of the process.
        :type position: :class:`Position`
        """
        super(ThermalProcess, self).__init__(friendly_name, position)
        self._initial_temperature = initial_temperature

        self._mass = mass

        self._internal_thermal_energy = initial_temperature * \
            thermal_capacity * mass

        self.thermal_capacity = thermal_capacity
        """
        The thermal capacity of the thermal process.
        """

        self.temperature = initial_temperature
        """
        The temperature of the process.
        """

        self.thermal_energy = self._internal_thermal_energy
        """
        The thermal energy stored inside the thermal process.
        """

    def add_energy(self, delta_energy):
        """
        Adds a given amount of energy to the thermal process.

        :param delta_energy: The energy to add to the thermal process.
        :type delta_energy: joule
        """
        self._internal_thermal_energy += delta_energy

    def reset(self):
        """
        AbstractSimulationElement implementation

        .. seealso:: :func:`gridsim.core.AbstractSimulationElement.reset`.
        """
        self.temperature = self._initial_temperature

        self._internal_thermal_energy = \
            self._initial_temperature * self.thermal_capacity * self._mass

        self.thermal_energy = self._internal_thermal_energy

    def calculate(self, time, delta_time):
        """
        AbstractSimulationElement implementation

        .. seealso:: :func:`gridsim.core.AbstractSimulationElement.calculate`.
        """
        pass

    def update(self, time, delta_time):
        """
        AbstractSimulationElement implementation

        .. seealso:: :func:`gridsim.core.AbstractSimulationElement.update`.
        """
        self.thermal_energy = self._internal_thermal_energy
        self.temperature = self.thermal_energy / \
                           (self.thermal_capacity * self._mass)

    @staticmethod
    @accepts((0, str),
             (4, Position))
    def room(friendly_name,
             surface, height,
             initial_temperature=293.15*units.kelvin,
             position=Position()):
        """
        Returns the thermal process of a room filled with air and the given
        surface, height and initial temperature.

        :param friendly_name: Friendly name to give to the returned object.
        :type friendly_name: str
        :param surface: The room's surface in m2.
        :type surface: square_meter
        :param height: The room's height in m.
        :type height: meter
        :param initial_temperature: The initial temperature inside the room in
            degrees celsius.
        :type initial_temperature: kelvin
        :param position: The position of the process.
        :type position: :class:`Position`
        :return: A new thermal process object representing the room or None on
            error.
        """
        return ThermalProcess(friendly_name,
                              Air().thermal_capacity,
                              initial_temperature,
                              surface * height * Air().weight,
                              position)

    @staticmethod
    def solid(friendly_name,
              specific_thermal_capacity, mass,
              initial_temperature=20*units.degC.to(units.kelvin),
              position=Position()):
        """
        Returns the thermal process of a solid body and the given mass, initial
        temperature.

        :param friendly_name: Friendly name to give to the returned object.
        :type friendly_name: str
        :param specific_thermal_capacity: The thermal capacity per g.
        :type specific_thermal_capacity: thermal_capacity
        :param mass: The solid's mass in g.
        :type mass: mass
        :param initial_temperature: The initial temperature of the solid.
        :type initial_temperature: temperature
        :param position: The position of the solid.
        :type position: :class:`Position`
        :return: A new thermal process object representing the solid or None
            on error.
        """
        return ThermalProcess(friendly_name, specific_thermal_capacity,
                              initial_temperature, mass, position)


class ThermalCoupling(AbstractThermalElement):

    @accepts((1, str),
             ((3, 4), ThermalProcess))
    def __init__(self, friendly_name, thermal_conductivity,
                 from_process,
                 to_process,
                 contact_area=1*units.metre*units.metre,
                 thickness=1*units.metre):
        """
        A thermal coupling connects two thermal processes allowing them to
        exchange thermal energy.

        :param friendly_name: The friendly name to identify the element.
        :type friendly_name: str

        :param thermal_conductivity: The thermal conductivity of the thermal
            element in W/K.
        :type thermal_conductivity: thermal conductivity units

        :param from_process: The first process coupled or the ID of the first
            process.
        :type from_process: int (ID), :class:`ThermalProcess`

        :param to_process: The second process coupled or the ID of the second
            process.
        :type to_process: int (ID), :class:`ThermalProcess`
        """
        super(ThermalCoupling, self).__init__(friendly_name)

        self.thermal_conductivity = thermal_conductivity
        """
        The thermal conductivity of the coupling in W/K.
        """

        self.from_process_id = None
        """
        The ID of the first process.
        """

        self.to_process_id = None
        """
        The ID of the second process.
        """

        self._contact_area = contact_area
        """
        The size of the contact area between the two `class::ThermalProcess`
        """
        self._thickness = thickness
        """
        The thickness of the material between the two `class::ThermalProcess`
        """

        if isinstance(from_process, ThermalProcess) \
                and not from_process is None \
                and not from_process.id is None:
            self.from_process_id = from_process.id
        elif isinstance(from_process, int):
            self.from_process_id = from_process
        else:
            raise RuntimeError('Missing or invalid from_process reference.')
        if isinstance(to_process, ThermalProcess) \
                and not to_process is None \
                and not to_process.id is None:
            self.to_process_id = to_process.id
        elif isinstance(to_process, int):
            self.to_process_id = to_process
        else:
            raise RuntimeError('Missing or invalid to_process reference.')
        self._simulator = None

        self._delta_energy = 0*units.joule

        self.power = None
        """
        Thermal power that gets conducted by the thermal coupling.
        """

    @property
    def contact_area(self):
        return self._contact_area

    @property
    def thickness(self):
        return self._thickness

    def reset(self):
        """
        AbstractSimulationElement implementation

        .. seealso:: :func:`gridsim.core.AbstractSimulationElement.reset`.
        """
        self._delta_energy = 0*units.joule
        pass

    def calculate(self, time, delta_time):
        """
        AbstractSimulationElement implementation

        .. seealso:: :func:`gridsim.core.AbstractSimulationElement.calculate`.
        """
        # Nothing to do, we do all calculations in simulator main module.
        pass

    def update(self, time, delta_time):
        """
        AbstractSimulationElement implementation

        .. seealso:: :func:`gridsim.core.AbstractSimulationElement.update`.
        """
        self.power = self._delta_energy / delta_time
        pass