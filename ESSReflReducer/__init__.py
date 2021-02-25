import scipp as sc
from scipy.constants import neutron_mass, h

HDM = (h / neutron_mass) * (sc.units.m * sc.units.m / sc.units.s)
