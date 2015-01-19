"""
.. moduleauthor:: Michael Clausen <clm@hevs.ch>
.. codeauthor:: Michael Clausen <clm@hevs.ch>
.. codeauthor:: Gillian Basso <gillian.basso@hevs.ch>

The :mod:`gridsim.recorder` module allows to record signals within the
gridsim simulation for later analysis. The module offers already a great
number of ready to use recorders - for example to write the data to text or
csv files or to plot the data after the simulation.

However if a special behavior is needed, custom recorders implementing the
:class:`.Recorder` can be implemented.

*Here an example illustrating the implementation of a custom recorder and how
recorders are added to the simulation:*

.. literalinclude:: ../../demo/consolerecorder.py
    :linenos:

- On line 9 to 24 we implement our custom recorder.

  - On line 15 we re-implement the abstract method
    :func:`gridsim.simulation.Recorder.on_simulation_reset`.
    We log which objects we observe.
  - On line 19 we implement the
    :func:`gridsim.simulation.Recorder.on_simulation_step` method.
    We just output the current time.
  - On line 22 we re-implement the abstract method
    :func:`gridsim.simulation.Recorder.on_observed_value()`.
    Basically we just output the value to the console.

- On line 27 we create the gridsim simulation object.
- On line 38 to 52 we setup a very simple thermal process, where we define 2
  rooms and a thermal coupling between them:

  - hot_room (line 39) has a ``surface`` of ``50m2`` and a ``height`` of
    ``2.5m``, so the ``volume`` is ``125m3``. The room is filled with
    :class:`gridsim.util.Air` (specific thermal capacity=`1.005 J/gK``) with
    the initial temperature of 60 degree celsius (line 38).
  - cold_room (line 45) has the same volume, but an initial temperature of 20
    degree celsius (line 44).
  - the two rooms are coupled with a thermal conductivity of ``100 Watts per
    Kelvin`` (line 51).

- On line 56 we add the recorder to the simulation. The recorder will listen all
  all :class:`ThermalProcess` and record their ``temperature`` parameter.
  The horizontal unit will be in second and the vertical unit in degree celsius.
  The simulation will call the recorder's
  **on_simulation_step()** and **on_observed_value()** method each time the
  simulation did a step.

- On line 60 we actually start the simulation for 1 hour with a resolution
  of 5 minutes.

*The output of the console logger should be something like this*::

    RESET, observing: ['hot_room', 'cold_room']
    time = 0 second:
        hot_room.temperature = 333.15 kelvin
        cold_room.temperature = 293.15 kelvin
    time = 300.0 second:
        hot_room.temperature = 325.189800995 kelvin
        cold_room.temperature = 301.110199005 kelvin
    time = 600.0 second:
        hot_room.temperature = 320.3978404 kelvin
        cold_room.temperature = 305.9021596 kelvin
    time = 900.0 second:
        hot_room.temperature = 317.513127803 kelvin
        cold_room.temperature = 308.786872197 kelvin
    time = 1200.0 second:
        hot_room.temperature = 315.776559523 kelvin
        cold_room.temperature = 310.523440477 kelvin
    time = 1500.0 second:
        hot_room.temperature = 314.731162698 kelvin
        cold_room.temperature = 311.568837302 kelvin
    time = 1800.0 second:
        hot_room.temperature = 314.101844211 kelvin
        cold_room.temperature = 312.198155789 kelvin
    time = 2100.0 second:
        hot_room.temperature = 313.723000744 kelvin
        cold_room.temperature = 312.576999256 kelvin
    time = 2400.0 second:
        hot_room.temperature = 313.494940746 kelvin
        cold_room.temperature = 312.805059254 kelvin
    time = 2700.0 second:
        hot_room.temperature = 313.357650897 kelvin
        cold_room.temperature = 312.942349103 kelvin
    time = 3000.0 second:
        hot_room.temperature = 313.275003774 kelvin
        cold_room.temperature = 313.024996226 kelvin
    time = 3300.0 second:
        hot_room.temperature = 313.225251028 kelvin
        cold_room.temperature = 313.074748972 kelvin
    time = 3600.0 second:
        hot_room.temperature = 313.19530037 kelvin
        cold_room.temperature = 313.10469963 kelvin
"""
from math import floor

from gridsim.iodata.output import AttributesGetter

from .unit import units
from .decorators import accepts
from .simulation import Recorder


class PlotRecorder(Recorder, AttributesGetter):

    @accepts((1, str),
             ((2, 3), (units.Quantity, type)))
    def __init__(self, attribute_name, x_unit, y_unit):
        """
        __init__(self, attribute_name, x_unit=None, y_unit=None)

        A :class:`PlotRecorder` can be used to record one or multiple signals
        and plot them at the end of the simulation either to a image file,
        add them to a PDF or show them on a window.

        :param attribute_name: The attribute name to observe. Every
            :class:`.AbstractSimulationElement` with a param of this name can
            be recorded
        :type attribute_name: str
        :param x_unit: The unit of the horizontal axis
        :type x_unit: type or unit see :mod:`gridsim.unit`
        :param y_unit: The unit of the vertical axis
        :type y_unit: type or unit see :mod:`gridsim.unit`

        *Example:*

        .. literalinclude:: ../../demo/plotrecorder.py
            :linenos:

        * In this example, only new concept are detailed.
        * On line 46, we create a :class:`PlotRecorder` which recorder the
          ``temperature`` attribute in Kelvin.
        * On line 47, we use that recorder in order to record all elements in
          the thermal module who have the attribute 'temperature' by using the
          powerful :func:`gridsim.simulation.Simulator.find()` method by asking
          to return a list of all elements that have the attribute 'temperature'.
        * On line 51, we create a very similar recorder as before,
        * On line 52, this time we do not want to record the temperature in
          Kelvin, we want the temperature in degrees celsius. As the
          simulator needs temperatures in kelvin (see :mod:`gridsim.unit` for
          mor information), we only have to give this information to the recorder,
          which will convert the temperature in degrees celsius.
        * On line 68, we create a first :class:`.FigureSaver` instance with the
          title 'Temperature (K)' which will use the data returned by the
          :class:`.Recorder` to :func:`save` the data in a figure.
        * On line 69, we also save the data of the other :class:`.Recorder`.
          The figures below show that the result is quite the same except that
          the y-coordinates have the right unit.
        * On line 72, we save the data using another saver: :class:`.CSVSaver`.

        The resulting 3 images of this simulation are show here:

        .. figure:: ../../demo/output/fig1.png
            :align: center

        .. figure:: ../../demo/output/fig2.png
            :align: center

        .. figure:: ../../demo/output/fig3.png
            :align: center

        """
        super(PlotRecorder, self).__init__(attribute_name, x_unit, y_unit)

        self._x = []
        self._y = {}

    def on_simulation_reset(self, subjects):
        """
        on_simulation_reset(self, subjects)

        :class:`.Recorder` implementation. Prepares the data structures.

        .. seealso:: :func:`gridsim.simulation.Recorder.on_simulation_reset()`
                     for details.
        """
        for subject in subjects:
            self._y[subject] = []

    def on_simulation_step(self, time):
        """
        on_simulation_step(self, time)

        :class:`.Recorder` implementation. Prepares the data structures.

        .. seealso:: :func:`gridsim.simulation.Recorder.on_simulation_step()`
                     for details.
        """
        if isinstance(self._x_unit, type):
            self._x.append(self._x_unit(time))
        else:
            self._x.append(units.value(units.convert(time, self._x_unit)))

    def on_observed_value(self, subject, time, value):
        """
        on_observed_value(self, subject, time, value)

        :class:`.Recorder` implementation. Saves the data in order to
        plot them afterwards.

        .. seealso:: :func:`gridsim.simulation.Recorder.on_observed_value()`
                     for details.
        """
        if isinstance(self._y_unit, type):
            self._y[subject].append(self._y_unit(value))
        else:
            self._y[subject].append(units.value(units.convert(value, self._y_unit)))

    def get_x_values(self):
        """
        get_x_values(self)

        Retrieves a list of time, on for each :func:`on_observed_value` and
        ordered following the call of :func:`gridsim.simulation.Simulator.step`.

        *Example*::

            sim = Simulator()

            kelvin = PlotRecorder('temperature')
            sim.record(kelvin, sim.thermal.find(has_attribute='temperature'))

            sim.step(17*units.second)
            sim.step(5*units.second)
            sim.step(42*units.second)

        In this example, this function should returns::

            [17, 5, 42]

        :return: time in second
        :rtype: list
        """
        return self._x

    def get_x_unit(self):
        """
        get_x_unit(self)

        Retrieves the unit of the time.

        :return: the time unit, see :mod:`gridsim.unit`
        :rtype: str
        """
        return self._x_unit

    def get_y_values(self):
        """
        get_y_values(self)

        Retrieves a map of the recorded data::

            {
                id1: [list of recorded values]
                id2: [list of recorded values]
            }

        with ``idX`` the ``subject`` given in parameter of :func:`on_observed_value`
        and :func:`on_simulation_reset`

        :return: a map associating id to recorded data
        :rtype: dict
        """
        return self._y

    def get_y_unit(self):
        """
        get_y_unit(self)

        Retrieves the unit od the recorded data.

        :return: the unit, see :mod:`gridsim.unit`
        :rtype: str
        """
        return self._y_unit


class HistogramRecorder(Recorder, AttributesGetter):

    @accepts((1, str),
             (4, int),
             ((5, 6), type))
    def __init__(self, attribute_name, x_min, x_max, nb_bins, x_unit, y_unit):
        """
        .. warning:: This class is currently not tested...

        :param attribute_name:
        :param x_min:
        :param x_max:
        :param nb_bins:
        :param x_unit: The unit of the horizontal axis
        :type x_unit: type or unit see :mod:`gridsim.unit`
        :param y_unit: The unit of the vertical axis
        :type y_unit: type
        :return:
        """
        if x_max <= x_min:
            raise TypeError("'x_max' must be larger than 'x_min'.")

        super(HistogramRecorder, self).__init__(attribute_name, x_unit, y_unit)

        self._x_min = x_min
        self._x_max = x_max
        self._N_bins = nb_bins
        self._x_delta = (x_max - x_min) / (nb_bins - 2)
        self._y = {}

    def on_simulation_reset(self, subjects):
        """
        :class:`RecorderInterface` implementation. Writes the header to the file
        defined by the _header_format attribute each time the simulation does a
        reset.

        .. seealso:: :func:`RecorderInterface.on_simulation_reset()`
                     for details.
        """
        for subject in subjects:
            label = subject + "." + self.attribute_name
            self._y[label] = [0 for _ in xrange(self._N_bins)]

    def on_simulation_step(self, time):
        """
        :class:`RecorderInterface` implementation. Called for each simulation
        step once per recorder.
        Writes the step separation to the file.

        .. seealso:: :func:`RecorderInterface.on_simulation_step()` for details.
        """
        pass

    def on_observed_value(self, subject, time, value):
        """
        :class:`RecorderInterface` implementation. Writes a (formatted) string
        into the file.

        .. seealso:: :func:`RecorderInterface.on_observed_value()` for details.
        """

        if value < self._x_min.total_seconds():
            bin_i = 0
        elif value >= self._x_max.total_seconds():
            bin_i = self._N_bins - 1
        else:
            bin_i = 1 + int(floor((value - self._x_min.total_seconds()) /
                                  self._x_delta))
        label = subject + "." + self.attribute_name
        self._y[label][bin_i] += 1

    def get_x_values(self):
        return []

    def get_x_unit(self):
        return ""

    def get_y_values(self):
        return self._y

    def get_y_unit(self):
        return self._y_unit
