import scipp as sc
from scipy.constants import neutron_mass, h

HDM = (h / neutron_mass) * (sc.units.m * sc.units.m / sc.units.s)

MAJOR = 0
MINOR = 0
MICRO = 1
__version__ = f'{MAJOR}.{MINOR}.{MICRO}'
