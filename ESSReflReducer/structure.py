import json
from datetime import datetime


class Person:
    """
    Information about people.
    """

    def __init__(self, name, affiliation="European Spallation Source"):
        """
        Args:
            name (str): The name of the person.
            affiliation (str or list of str, optional): The affiliation(s) of the person. Defaults to 'European Spallation Source'.
        """
        self.name = name
        self.affiliation = affiliation

    def __repr__(self):
        return _repr(self)


class Creation:
    """
    Information about the data creation.
    """

    def __init__(self, owners, time=None, system="dmsc.ess.eu"):
        """
        Args:
            owners (list of ESSReflReducer.Person): The owner(s) of the reduced data, this may not be the same as the creator of the raw data.
            time (datetime.datetime, optional): The date and time of the reduction. Defaults to current date and time.
            system (str, optional): The machine name/IP address used for reduction. Defaults to 'dmsc.ess.eu'.
        """
        if isinstance(owners, Person):
            owners = [owners]
        self.owners = owners
        if time is None:
            time = datetime.now()
        self.time = time.strftime("%Y-%m-%d, %H:%M:%S")
        self.system = system

    def __repr__(self):
        return _repr(self)


class Origin:
    """
    Information about the source of the raw data that is being reduced.
    """

    def __init__(
        self,
        owners,
        experiment_id,
        title,
        facility="European Spallation Source",
        experiment_start=None,
        experiment_end=None,
    ):
        """
        Args:
            owners (list of ESSReflReducer.Person): The owner(s) of the raw data.
            experiment_id (str): The experiment identification string.
            title (str): A title for the experiment.
            facility (str, optional): Where the data originates from. Defaults to 'European Spallation Source'.
            experiment_date (datetime.datetime, optional): The start date for the experiment. Defaults to current date.
            experiment_end (datetime.datetime, optional): The end date of the experiment. Defaults to current date.
        """
        if isinstance(owners, Person):
            owners = [owners]
        self.owners = owners
        self.experiment_id = experiment_id
        self.title = title
        self.facility = facility
        if experiment_start is None:
            experiment_start = datetime.strptime(
                datetime.now().strftime("%Y-%m-%d"), "%Y-%m-%d"
            )
        if experiment_end is None:
            experiment_end = datetime.strptime(
                datetime.now().strftime("%Y-%m-%d"), "%Y-%m-%d"
            )
        self.experiment_start = experiment_start.strftime("%Y-%m-%d, %H:%M:%S")
        self.experiment_end = experiment_end.strftime("%Y-%m-%d, %H:%M:%S")

    def __repr__(self):
        return _repr(self)


class Layer:
    """
    A description of a layer.
    """

    def __init__(self, name, sld=None, thickness=None, magnetisation_vector=None):
        self.name = name
        if sld is not None:
            self.sld = sld
        if thickness is not None:
            self.thickness = thickness
        if magnetisation_vector is not None:
            self.magnetisation_vector = magnetisation_vector

    def __repr__(self):
        return _repr(self)


class Sample:
    """
    Information about the sample.
    """

    def __init__(self, name, description=None):
        self.name = name
        if description is not None:
            self.description = description

    def __repr__(self):
        return _repr(self)


class Measurement:
    """
    Measurement info
    """

    def __init__(
        self,
        scheme,
        wavelength_range,
        angular_range,
        wavelength_unit="Aa",
        angular_unit="deg",
        omega=0,
    ):
        self.scheme = scheme
        self.wavelength_range = wavelength_range
        self.angular_range = angular_range
        self.wavelength_unit = wavelength_unit
        self.angular_unit = angular_unit
        self.omega = omega

    def __repr__(self):
        return _repr(self)


class Probe:
    """"""

    def __init__(self, radiation, polarisation=None, energy=None):
        self.radiation = radiation
        if polarisation is not None:
            self.polarisation = polarisation
        if energy is not None:
            self.energy = energy

    def __repr__(self):
        return _repr(self)


class Experiment:
    """"""

    def __init__(self, instrument, probe, measurement, sample):
        self.instrument = instrument
        self.probe = probe
        self.measurement = measurement
        self.sample = sample

    def __repr__(self):
        return _repr(self)


class DataSource:
    """
    """
    def __init__(self, origin, experiment, links):
        self.origin = origin
        self.experiment = experiment
        self.links = links

    def __repr__(self):
        return _repr(self)


class File:
    """
    """
    def __init__(self, filename, creation_time=None):
        self.filename = filename
        if creation_time is None:
            creation_time = datetime.strptime(
                datetime.now().strftime("%Y-%m-%d"), "%Y-%m-%d"
            )
        self.creation_time = creation_time.strftime("%Y-%m-%d, %H:%M:%S")

    def __repr__(self):
        return _repr(self)


def _dumping(o):
    try:
        to_return = o.__dict__
    except AttributeError:
        to_return = o.__repr__()
    return to_return


def _repr(class_to_represent):
    return json.dumps(
        class_to_represent, default=lambda o: _dumping(o), sort_keys=True, indent=2
    )[2:-2]
