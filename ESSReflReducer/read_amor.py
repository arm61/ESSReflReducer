import copy
import numpy as np
import h5py
from ESSReflReducer import HDM
from scipy.special import erf
from datetime import datetime
import scipp as sc
class Creator:
    """
    Information about the creator of the reduced data. This is not necessarily who collect the data in the first place.
    """
    def __init__(self, name, affiliation="European Spallation Source",
                 time=None, system="Unknown"):
        """
        Args:
            name (str): The name of the creator.
            affiliation (str or list of str): The affiliation(s) of the creator.
        """
        self.name = name
        self.affiliation = affiliation



class RawData:
    """
    This class will store the "raw" data from a reflectometry measurements.
    """
    def __init__(self, filename, instru):
        """
        Args:
            filename (str): The raw data file name.
        """
        self.filename = filename




class AmorDataReader:
    """
    A class to store information from an AMOR data file.
    """
    def __init__(self, filename, mask_data=True, chopper_speed=20/3/sc.units.s,
                 chopper_phase=-8. * sc.units.dimensionless,
                 lambda_cut=2.4e-10 * sc.units.m,
                 sample_detector_distance=4.0 * sc.units.m,
                 chopper_detector_distance=1.9e1 * sc.units.m,
                 detector_angle=5.0 * sc.units.deg,
                 detector_blade_z=10.11e-3 * sc.units.m,
                 sample_angle_horizon_offset=0 * sc.units.deg,
                 y_min=1e-3 * sc.units.m, y_max=29e-3 * sc.units.m,
                 lambda_min=2.4e-10 * sc.units.m, lambda_max=None,
                 theta_min=0 * sc.units.deg, theta_max=180 * sc.units.deg,
                 sample_size=0.01 * sc.units.m, beam_size=0.001 * sc.units.m,
                 gravity=True):
        """
        Args:
            filename (str): The .hdf file to be read.
            mask_data (bool): Data masking. Optional, default `True`.
            chopper_speed (`sc.Variable`): Rotational velocity of the chopper. Optional, default `6.6666... s^{-1}`.
            chopper_phase (`sc.Variable`): Phase offset between chopper pulse and ToF zero. Optional, default `-9.36`.
            lambda_cut (`sc.Variable`): Reshuffle value for the ToF. Optional, default `2.5e-10 m`.
            sample_detector_distance (`sc.Variable`): Distance from sample to detector. Optional, default `4.0 m`.
            chopper_detector_distance (`sc.Variable`): Distance from chopper to detector. Optional, default `19 m`.
            detector_angle (`sc.Variable`): Angle for detector. Optional, default `5 degrees of arc`.
            detector_blade_z (`sc.Variable`): Distance between detector blades. Optional, default `10.11e-3 m`.
            sample_angle_horizon_offset (`sc.Variable`): Correction for misalignment of sample. Optional, default `0 degrees of arc`.
            y_min (`sc.Variable`): Minimum cutoff for detector y-dimension. Optional, default `1e-3 m`.
            y_max (`sc.Variable`): Maximum cutoff for detector y-dimension. Optional, default `29e-3 m`.
            lambda_min (`sc.Variable`): Minimum cutoff for wavelength. Optional, default `2.4e-10 m`.
            lambda_max (`sc.Variable`): Maximum cutoff for wavelength. Optional, default `lambda_min + tau * HDM / chopper_detector_distance`.
            theta_min (`sc.Variable`): Minimum cutoff for angle. Optional, default `0 degrees of arc`.
            theta_max (`sc.Variable`): Maximum cutoff for angle. Optional, default `180 degrees of arc`.
            sample_size (`sc.Variable`): Size of the sample in direction of the beam. Optional, default `0.01 m`.
            beam_size (`sc.Variable`): Size of the beam perpendicular to the scattering surface. Optional, default `0.001 m`.
        """
        f = h5py.File(filename, 'r')
        self.detector_angle = detector_angle
        self.sample_detector_distance = sample_detector_distance
        self.chopper_detector_distance = chopper_detector_distance
        self.beam_size = beam_size
        self.sample_size = sample_size
        self.title = (f['/experiment/title'][0]).decode("utf-8")
        self.detector_pixel_id = f['/experiment/data/event_id'][:].astype(float)
        self.event_time_offset = sc.Variable(values=f['/experiment/data/event_time_offset'][:].astype(float) / 1e9, unit=sc.units.s, dims=['event'])
        self.detector_angle_horizon = float(-1*f['/instrument/stages/com/value'][0]) * sc.units.deg
        self.sample_angle_horizon = float(f['/instrument/stages/som/value'][0]) * sc.units.deg + sample_angle_horizon_offset
        self.tau = 1 / (2 * chopper_speed)
        try:
            self.monitor = float(sum(f['/experiment/proton_current/value'][:]) * self.tau)
        except KeyError:
            self.monitor = (f['experiment/data/event_time_zero'][-1] - f['experiment/data/event_time_zero'][0]) / 1e9
        f.close()
        self.n_events = len(self.detector_pixel_id)
        data = sc.broadcast(sc.Variable(value=1.0, variance=1.0, dtype=sc.dtype.float64), dims=['event'], shape=[self.n_events])
        tof_offset = self.tau * chopper_phase / 180.
        tof_e = self.event_time_offset
        tof_cut = lambda_cut * chopper_detector_distance / HDM
        tof_e = sc.Variable(values=np.remainder((tof_e - tof_cut + self.tau).values, self.tau.values), unit=sc.units.s, dims=['event']) + tof_cut + tof_offset
        proto_events = {'data': data, 'coords': {'tof': tof_e}}
        self.data = sc.DataArray(**proto_events)

    def detector_reconstruction(self,
                                detector_blade_z=10.11e-3 * sc.units.m):
        """
        Generate the detector image for all data.
        """
        detector_dz = (4.0e-3 * sc.units.m * sc.sin(self.detector_angle))
        detector_zero = 2.5 * detector_blade_z
        a, b = np.divmod(self.detector_pixel_id, 32*32)
        c, d = np.divmod(b, 32)
        self.data.attrs['blade-nr'] = sc.Variable(values=a, dims=['event'], dtype=float)
        self.data.attrs['z-on-blade'] = sc.Variable(values=c, dims=['event'], dtype=float)
        self.data.coords['y'] = sc.Variable(values=d * 1e-3, dims=['event'], dtype=float, unit=sc.units.m)
        self.data.coords['z'] = detector_zero - self.data.attrs['blade-nr'] * detector_blade_z - self.data.attrs['z-on-blade'] * detector_dz

    def tof_to_lambda(self):
        """
        """
        detector_dx = (4.0e-3 * sc.units.m * sc.cos(self.detector_angle))
        self.data.attrs['flight-path-length'] = self.chopper_detector_distance + self.data.attrs['z-on-blade'] * detector_dx + self.sample_detector_distance * (1./sc.cos(self.detector_angle_horizon)-1.)
        self.data.coords['lambda'] = self.data.coords['tof'] * HDM / self.data.attrs['flight-path-length']

    def find_theta(self, gravity=True):
        """
        """
        if gravity:
            self.gravity_drop = -3.07 * self.sample_detector_distance.values * self.sample_detector_distance.values * self.data.coords['lambda'].values * self.data.coords['lambda'].values
            if self.sample_angle_horizon.values > 0:
                theta = self.sample_angle_horizon.values + (np.degrees(np.arctan2(self.data.coords['z'].values, self.sample_detector_distance.values))) - (np.degrees(np.arctan2(self.gravity_drop, self.sample_detector_distance.values)))
            else:
                theta = -1 * self.sample_angle_horizon.values - (np.degrees(np.arctan2(self.data.coords['z'].values, self.sample_detector_distance.values))) + (np.degrees(np.arctan2(self.gravity_drop, self.sample_detector_distance.values)))
            self.data.coords['theta'] = sc.Variable(values=theta, unit=sc.units.deg, dims=['event'])
        else:
            self.data.coords['theta'] = self.detector_angle_horizon - self.sample_angle_horizon + self.data.coords['z'] / self.sample_detector_distance * (180. * sc.units.deg) / np.pi

    def find_qz(self):
        qz_m = 4. * np.pi * sc.sin(self.data.coords['theta']) / self.data.coords['lambda']
        self.data.coords['qz'] = sc.Variable(values=qz_m.values * 1e-10, unit=(1 / sc.units.angstrom).unit, dims=['event'])

    def apply_masks(self, y_min=1e-3 * sc.units.m, y_max=29e-3 * sc.units.m,
                    lambda_min=2.4e-10 * sc.units.m, lambda_max=None,
                    theta_min=0 * sc.units.deg, theta_max=180 * sc.units.deg):
        """
        Perform masking of data based on y-detector, wavelength and theta values.
        """
        if lambda_max is None:
            lambda_max = lambda_min + self.tau * HDM / self.chopper_detector_distance
        else:
            lambda_max = lambda_max
        self.data.masks['y'] = (self.data.coords['y'] < y_min) | (self.data.coords['y'] > y_max)
        self.data.masks['lambda'] = (self.data.coords['lambda'] < lambda_min) | (self.data.coords['lambda'] > lambda_max)
        self.data.masks['theta'] = (self.data.coords['theta'] < theta_min) | (self.data.coords['theta'] > theta_max)

    def copy(self):
        return copy.deepcopy(self)

class AmorReducer:
    """
    Reduction of AMOR data.
    """
    def __init__(self, reference, data, q_bins):
        """
        Args:
            reference_list (list): List of `AmorDataReader` objects for the reference data.
            data_list (list): List of `AmorDataReader` objects for the measured data.
        """
        self.reference_counts = 0
        self.reference_monitor = 0
        self.data_counts = 0
        self.data_monitor = 0
        self.reference = reference.copy()
        self.data = data.copy()
        self.reference_counts += self.reference.n_events
        self.reference_monitor += self.reference.monitor
        self.reference.data /= self.reference.monitor
        self.reference.data /= sc.array(values=illumination_correction(self.reference.beam_size, self.reference.sample_size, self.reference.data.coords['theta']), dims=['event'])
        reference_intensity = sc.histogram(self.reference.data, sc.Variable(values=q_bins, dims=['qz'], unit=(1 / sc.units.angstrom).unit))
        supermirror = sc.Variable(values=(-2.5510204081632653 * (q_bins[:-1] + (0.5 * (np.diff(q_bins)))) + 1.028061224489796), dims=['qz'])
        self.reference_intensity = reference_intensity / supermirror
        self.data_counts += self.data.n_events
        self.data_monitor += self.data.monitor
        self.data.data /= self.data.monitor
        self.data.data /= sc.array(values=illumination_correction(self.data.beam_size, self.data.sample_size, self.data.data.coords['theta']), dims=['event'])
        self.data_intensity = sc.histogram(self.data.data, sc.Variable(values=q_bins, dims=['qz'], unit=(1 / sc.units.angstrom).unit))
        self.reflectivity = self.data_intensity / self.reference_intensity

def illumination_correction(beam_size, sample_size, theta):
    """
    The factor by which the intensity should be multiplied to account for the
    scattering geometry, where the beam is Gaussian in shape.

    Args:
        beam_width (:py:attr:`float`): Width of incident beam, in metres.
        sample_size (:py:attr:`uncertainties.core.Variable`): Width of sample
            in the dimension of the beam, in metres.
        theta (:py:attr:`sc.Variable`): Incident angle, in degrees.

    Returns:
        (:py:attr:`array_like`): Correction factor.
    """
    sample_size_perp = sample_size * (theta * np.pi / (180 * sc.units.deg))
    scale_factor = erf((sample_size_perp / beam_size * 2.35482).values)
    return scale_factor
