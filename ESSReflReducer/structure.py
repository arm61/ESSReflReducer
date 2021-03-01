import json
from pathlib import Path
from datetime import datetime, date
from ESSReflReducer import __version__


class Structure:
    def __repr__(self):
        return _repr(self)


class Person(Structure):
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


class Creation(Structure):
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


class Origin(Structure):
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
            experiment_start = date.today()
        if experiment_end is None:
            experiment_end = date.today()
        self.experiment_start = experiment_start
        self.experiment_end = experiment_end


class Layer(Structure):
    """
    A description of a layer.
    """

    def __init__(self, name, sld=None, thickness=None, magnetisation_vector=None):
        """
        Args:
            name (str): Idenfitier for the layer.
            sld (float or complex): Layer scattering length density.
            thickness (float): Layer thickness.
            magnetisation_vector (float): Layer magnetisation vector.
        """
        self.name = name
        if sld is not None:
            self.sld = sld
        if thickness is not None:
            self.thickness = thickness
        if magnetisation_vector is not None:
            self.magnetisation_vector = magnetisation_vector


class Sample(Structure):
    """
    Information about the sample.
    """

    def __init__(self, name, description=None):
        """
        Args:
            name (str): Identifier of the sample.
            description (list of ESSReflReducer.structure.Layer): A series of layers describing the sample.
        """
        self.name = name
        if description is not None:
            self.description = description


class Measurement(Structure):
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
        """
        Args:
            scheme (str): A description of the measurement style, i.e. 'Angle- and energy-dispersive'.
            wavelength_range (float or list): Wavelength range for energy-dispersive measurements, single value for monochromatic.
            angular_range (float or list): Angle range for angle-dispersive measurements, single value for single angle.
            wavelength_unit (str, optional): The wavelength unit. Defaults to 'Aa'.
            angular_unit (str, optional): The angle unit. Defaults to 'deg'.
            omega (float, optional): Sample stage rotation, the units for this should match the angular_unit. Defaults to 0.
        """
        self.scheme = scheme
        self.wavelength_range = wavelength_range
        self.angular_range = angular_range
        self.wavelength_unit = wavelength_unit
        self.angular_unit = angular_unit
        self.omega = omega


class Probe(Structure):
    """
    Information about the probing radiation used.
    """

    def __init__(self, radiation, polarisation=None, energy=None):
        """
        Args:
            radiation (str): The probing radiation, i.e. 'neutron'.
            polarisation (float, optional): The polarisation degree. Defaults to None.
        """
        self.radiation = radiation
        if polarisation is not None:
            self.polarisation = polarisation


class Experiment(Structure):
    """
    Information about the experiment as a whole
    """

    def __init__(self, instrument, probe, measurement, sample):
        """
        Args:
            instrument (str): Identifier for the instrument used.
            probe (ESSReflReducer.structure.Probe): Probing radiation.
            measurement (ESSReflReducer.structure.Measurement): Description of the measurement.
            sample (ESSReflReducer.structure.Sample): Sample description.
        """
        self.instrument = instrument
        self.probe = probe
        self.measurement = measurement
        self.sample = sample


class DataSource(Structure):
    """
    Information about the source of the data being reduced.
    """

    def __init__(self, origin, experiment, links):
        """
        Args:
            origin (ESSReflReducer.structure.Origin): The origin of the data.
            experiment (ESSReflReducer.structure.Experiment): The experimental information for the data.
            links (dict): Links to other data and publications relevant to the reduced data.
        """
        self.origin = origin
        self.experiment = experiment
        self.links = links


class File(Structure):
    """
    File information
    """

    def __init__(self, filename, creation_time=None):
        """
        Args:
            filename (str): The path to the file.
            creation_time (datetime.datetime): Date and time of file creation.
        """
        self.filename = Path(filename)
        if creation_time is None:
            creation_time = datetime.now()
        self.creation_time = creation_time

    @property
    def dir(self):
        """
        Get the directory of the file.

        Returns:
            (str): File directory.
        """
        return self.filename.parent.as_posix()

    @property
    def ext(self):
        """
        Get the extention of the file.

        Returns:
            (str): File ext.
        """
        return self.filename.suffix

    @property
    def name(self):
        """
        Get the name of the file.

        Returns:
            (str): File name.
        """
        return self.filename.stem


class Software(Structure):
    """
    Information on the software used.
    """
    def __init__(self, script):
        """
        Args:
            script (ESSReflReducer.structure.File): The file for the script used in reduction.
        """
        self.name = "ESSReflReducer"
        self.version = __version__
        self.script = script


class DataState(Structure):
    """
    Information about what has been done to the data.
    """
    def __init__(self):
        self.footprint = None
        self.intensity = None
        self.resolution = None
        self.absorption = None
        self.background = None


class Data(Structure):
    """
    The structure of the data in the file.
    """
    def __init__(self, columns):
        """
        Args:
            columns (dict): A dictionary describing the columns in the data.
        """
        self.columns = columns


def _dumping(o):
    """
    Determines what is dumped to json in the _repr function.

    Args:
        o (object): The object being dumped.

    Returns:
        (str or dict): The dump.
    """
    if isinstance(o, datetime):
        to_return = o.strftime("%Y-%m-%d, %H:%M:%S")
    elif isinstance(o, date):
        to_return = o.strftime("%Y-%m-%d")
    elif isinstance(o, Path):
        to_return = o.as_posix()
    else:
        try:
            to_return = o.__dict__
        except AttributeError:
            to_return = o.__repr__()
    return to_return


def _repr(class_to_represent):
    """
    The representation object for all the Structure sub-classes. This returns a string in a json-like format which will be ORSO compatible.

    Args:
        class_to_represent (class): The class to be represented.

    Returns:
        (str): A string representation.
    """
    return json.dumps(
        class_to_represent, default=lambda o: _dumping(o), sort_keys=True, indent=2
    )[2:-2]
