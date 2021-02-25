"""
Tests for structure module
"""

# Copyright (c) Andrew R. McCluskey
# Distributed under the terms of the MIT License
# author: Andrew R. McCluskey

import unittest
from numpy.testing import assert_almost_equal, assert_equal
from datetime import datetime
from ESSReflReducer import structure

PERSON = structure.Person("Brian", "A N University")
TODAY = datetime.now().strftime("%Y-%m-%d")


class TestStructure(unittest.TestCase):
    def test_person_init_a(self):
        p = structure.Person("Brian")
        assert_equal(p.name, "Brian")
        assert_equal(p.affiliation, "European Spallation Source")

    def test_person_init_b(self):
        assert_equal(PERSON.name, "Brian")
        assert_equal(PERSON.affiliation, "A N University")

    def test_person_repr(self):
        expect = '  "affiliation": "A N University",\n  "name": "Brian"'
        assert_equal(PERSON.__repr__(), expect)

    def test_creation_init_a(self):
        c = structure.Creation(PERSON)
        assert_equal(len(c.owners), 1)
        assert_equal(c.owners[0], PERSON)
        assert_equal(c.time[:-10], f"{TODAY}")
        assert_equal(c.system, "dmsc.ess.eu")

    def test_creation_init_b(self):
        c = structure.Creation([PERSON, structure.Person("Colin")])
        assert_equal(len(c.owners), 2)
        assert_equal(c.owners[0], PERSON)
        assert_equal(c.owners[1].name, "Colin")
        assert_equal(c.owners[1].affiliation, "European Spallation Source")
        assert_equal(c.time[:-10], f"{TODAY}")
        assert_equal(c.system, "dmsc.ess.eu")

    def test_creation_init_c(self):
        c = structure.Creation(PERSON, time=datetime(2021, 2, 25, 13, 11, 10, 981419))
        assert_equal(len(c.owners), 1)
        assert_equal(c.owners[0], PERSON)
        assert_equal(c.time, "2021-02-25, 13:11:10")

    def test_creation_init_d(self):
        c = structure.Creation(PERSON, system="estia.ess.eu")
        assert_equal(len(c.owners), 1)
        assert_equal(c.owners[0], PERSON)
        assert_equal(c.system, "estia.ess.eu")

    def test_creation_print(self):
        c = structure.Creation(PERSON, time=datetime(2021, 2, 25, 13, 11, 10, 981419))
        assert_equal(
            c.__repr__(),
            '  "owners": [\n    {\n      "affiliation": "A N University",\n      "name": "Brian"\n    }\n  ],\n  "system": "dmsc.ess.eu",\n  "time": "2021-02-25, 13:11:10"',
        )

    def test_origin_init_a(self):
        o = structure.Origin(PERSON, "40208", "An example experiment")
        assert_equal(len(o.owners), 1)
        assert_equal(o.owners[0], PERSON)
        assert_equal(o.experiment_id, "40208")
        assert_equal(o.title, "An example experiment")
        assert_equal(o.facility, "European Spallation Source")
        assert_equal(o.experiment_start, "2021-02-25, 00:00:00")
        assert_equal(o.experiment_end, "2021-02-25, 00:00:00")

    def test_origin_init_b(self):
        o = structure.Origin(
            [PERSON, structure.Person("Colin")], "40208", "An example experiment"
        )
        assert_equal(len(o.owners), 2)
        assert_equal(o.owners[0], PERSON)
        assert_equal(o.owners[1].name, "Colin")
        assert_equal(o.owners[1].affiliation, "European Spallation Source")
        assert_equal(o.experiment_id, "40208")
        assert_equal(o.title, "An example experiment")
        assert_equal(o.facility, "European Spallation Source")
        assert_equal(o.experiment_start, f"{TODAY}, 00:00:00")
        assert_equal(o.experiment_end, f"{TODAY}, 00:00:00")

    def test_origin_init_c(self):
        o = structure.Origin(
            [PERSON, structure.Person("Colin")],
            "40208",
            "An example experiment",
            facility="Paul Scherrer Institut, SINQ",
        )
        assert_equal(len(o.owners), 2)
        assert_equal(o.owners[0], PERSON)
        assert_equal(o.owners[1].name, "Colin")
        assert_equal(o.owners[1].affiliation, "European Spallation Source")
        assert_equal(o.experiment_id, "40208")
        assert_equal(o.title, "An example experiment")
        assert_equal(o.facility, "Paul Scherrer Institut, SINQ")
        assert_equal(o.experiment_start, f"{TODAY}, 00:00:00")
        assert_equal(o.experiment_end, f"{TODAY}, 00:00:00")

    def test_origin_init_d(self):
        o = structure.Origin(
            [PERSON, structure.Person("Colin")],
            "40208",
            "An example experiment",
            experiment_start=datetime(1992, 7, 14, 6, 11, 20),
        )
        assert_equal(len(o.owners), 2)
        assert_equal(o.owners[0], PERSON)
        assert_equal(o.owners[1].name, "Colin")
        assert_equal(o.owners[1].affiliation, "European Spallation Source")
        assert_equal(o.experiment_id, "40208")
        assert_equal(o.title, "An example experiment")
        assert_equal(o.facility, "European Spallation Source")
        assert_equal(o.experiment_start, "1992-07-14, 06:11:20")
        assert_equal(o.experiment_end, "2021-02-25, 00:00:00")

    def test_origin_init_e(self):
        o = structure.Origin(
            [PERSON, structure.Person("Colin")],
            "40208",
            "An example experiment",
            experiment_end=datetime(1994, 11, 29, 2, 50, 42),
        )
        assert_equal(len(o.owners), 2)
        assert_equal(o.owners[0], PERSON)
        assert_equal(o.owners[1].name, "Colin")
        assert_equal(o.owners[1].affiliation, "European Spallation Source")
        assert_equal(o.experiment_id, "40208")
        assert_equal(o.title, "An example experiment")
        assert_equal(o.facility, "European Spallation Source")
        assert_equal(o.experiment_start, "2021-02-25, 00:00:00")
        assert_equal(o.experiment_end, "1994-11-29, 02:50:42")

    def test_origin_print(self):
        o = structure.Origin(PERSON, "40208", "An example experiment")
        assert_equal(
            o.__repr__(),
            '  "experiment_end": "2021-02-25, 00:00:00",\n  "experiment_id": "40208",\n  "experiment_start": "2021-02-25, 00:00:00",\n  "facility": "European Spallation Source",\n  "owners": [\n    {\n      "affiliation": "A N University",\n      "name": "Brian"\n    }\n  ],\n  "title": "An example experiment"',
        )

    def test_layer_init_a(self):
        l = structure.Layer("Air")
        assert_equal(l.name, "Air")

    def test_layer_print_a(self):
        l = structure.Layer("Air")
        assert_equal(l.__repr__(), '  "name": "Air"')

    def test_layer_init_b(self):
        l = structure.Layer("Air", sld=2 + 3j)
        assert_equal(l.name, "Air")
        assert_almost_equal(l.sld, 2 + 3j)

    def test_layer_print_b(self):
        l = structure.Layer("Air", sld=2 + 3j)
        assert_equal(l.__repr__(), '  "name": "Air",\n  "sld": "(2+3j)"')

    def test_layer_init_c(self):
        l = structure.Layer("Air", thickness=100)
        assert_equal(l.name, "Air")
        assert_almost_equal(l.thickness, 100)

    def test_layer_print_c(self):
        l = structure.Layer("Air", thickness=100)
        assert_equal(l.__repr__(), '  "name": "Air",\n  "thickness": 100')

    def test_layer_init_d(self):
        l = structure.Layer("Air", magnetisation_vector=-0.5)
        assert_equal(l.name, "Air")
        assert_almost_equal(l.magnetisation_vector, -0.5)

    def test_layer_print_d(self):
        l = structure.Layer("Air", magnetisation_vector=-0.5)
        assert_equal(l.__repr__(), '  "magnetisation_vector": -0.5,\n  "name": "Air"')

    def test_sample_init_a(self):
        s = structure.Sample("My Sample")
        assert_equal(s.name, "My Sample")

    def test_sample_print_a(self):
        s = structure.Sample("My Sample")
        assert_equal(s.__repr__(), '  "name": "My Sample"')

    def test_sample_init_b(self):
        s = structure.Sample(
            "My Sample",
            description=[
                structure.Layer("Air"),
                structure.Layer("Lipids"),
                structure.Layer("Water"),
            ],
        )
        assert_equal(s.name, "My Sample")
        assert_equal(s.description[0].name, "Air")
        assert_equal(s.description[1].name, "Lipids")
        assert_equal(s.description[2].name, "Water")

    def test_sample_print_b(self):
        s = structure.Sample(
            "My Sample",
            description=[
                structure.Layer("Air"),
                structure.Layer("Lipids"),
                structure.Layer("Water"),
            ],
        )
        assert_equal(
            s.__repr__(),
            '  "description": [\n    {\n      "name": "Air"\n    },\n    {\n      "name": "Lipids"\n    },\n    {\n      "name": "Water"\n    }\n  ],\n  "name": "My Sample"',
        )

    def test_measurement_init_a(self):
        m = structure.Measurement(
            "Angle and energy dispersive", [4.0, 12.0], [0.3, 2.1]
        )
        assert_equal(m.scheme, "Angle and energy dispersive")
        assert_almost_equal(m.wavelength_range[0], 4.0)
        assert_almost_equal(m.wavelength_range[1], 12.0)
        assert_almost_equal(m.angular_range[0], 0.3)
        assert_almost_equal(m.angular_range[1], 2.1)
        assert_equal(m.wavelength_unit, "Aa")
        assert_equal(m.angular_unit, "deg")
        assert_almost_equal(m.omega, 0)

    def test_measurement_print_a(self):
        m = structure.Measurement(
            "Angle and energy dispersive", [4.0, 12.0], [0.3, 2.1]
        )
        assert_equal(
            m.__repr__(),
            '  "angular_range": [\n    0.3,\n    2.1\n  ],\n  "angular_unit": "deg",\n  "omega": 0,\n  "scheme": "Angle and energy dispersive",\n  "wavelength_range": [\n    4.0,\n    12.0\n  ],\n  "wavelength_unit": "Aa"',
        )

    def test_measurement_init_b(self):
        m = structure.Measurement(
            "Angle and energy dispersive",
            [40.0, 120.0],
            [0.3, 2.1],
            wavelength_unit="nm",
        )
        assert_equal(m.scheme, "Angle and energy dispersive")
        assert_almost_equal(m.wavelength_range[0], 40.0)
        assert_almost_equal(m.wavelength_range[1], 120.0)
        assert_almost_equal(m.angular_range[0], 0.3)
        assert_almost_equal(m.angular_range[1], 2.1)
        assert_equal(m.wavelength_unit, "nm")
        assert_equal(m.angular_unit, "deg")
        assert_almost_equal(m.omega, 0)

    def test_measurement_print_b(self):
        m = structure.Measurement(
            "Angle and energy dispersive",
            [40.0, 120.0],
            [0.3, 2.1],
            wavelength_unit="nm",
        )
        assert_equal(
            m.__repr__(),
            '  "angular_range": [\n    0.3,\n    2.1\n  ],\n  "angular_unit": "deg",\n  "omega": 0,\n  "scheme": "Angle and energy dispersive",\n  "wavelength_range": [\n    40.0,\n    120.0\n  ],\n  "wavelength_unit": "nm"',
        )

    def test_measurement_init_c(self):
        m = structure.Measurement(
            "Angle and energy dispersive", [4.0, 12.0], [0.3, 2.1], angular_unit="rad"
        )
        assert_equal(m.scheme, "Angle and energy dispersive")
        assert_almost_equal(m.wavelength_range[0], 4.0)
        assert_almost_equal(m.wavelength_range[1], 12.0)
        assert_almost_equal(m.angular_range[0], 0.3)
        assert_almost_equal(m.angular_range[1], 2.1)
        assert_equal(m.wavelength_unit, "Aa")
        assert_equal(m.angular_unit, "rad")
        assert_almost_equal(m.omega, 0)

    def test_measurement_print_c(self):
        m = structure.Measurement(
            "Angle and energy dispersive", [4.0, 12.0], [0.3, 2.1], angular_unit="rad"
        )
        assert_equal(
            m.__repr__(),
            '  "angular_range": [\n    0.3,\n    2.1\n  ],\n  "angular_unit": "rad",\n  "omega": 0,\n  "scheme": "Angle and energy dispersive",\n  "wavelength_range": [\n    4.0,\n    12.0\n  ],\n  "wavelength_unit": "Aa"',
        )

    def test_measurement_init_c(self):
        m = structure.Measurement(
            "Angle and energy dispersive", [4.0, 12.0], [0.3, 2.1], omega=1.2
        )
        assert_equal(m.scheme, "Angle and energy dispersive")
        assert_almost_equal(m.wavelength_range[0], 4.0)
        assert_almost_equal(m.wavelength_range[1], 12.0)
        assert_almost_equal(m.angular_range[0], 0.3)
        assert_almost_equal(m.angular_range[1], 2.1)
        assert_equal(m.wavelength_unit, "Aa")
        assert_equal(m.angular_unit, "deg")
        assert_almost_equal(m.omega, 1.2)

    def test_measurement_print_c(self):
        m = structure.Measurement(
            "Angle and energy dispersive", [4.0, 12.0], [0.3, 2.1], omega=1.2
        )
        assert_equal(
            m.__repr__(),
            '  "angular_range": [\n    0.3,\n    2.1\n  ],\n  "angular_unit": "deg",\n  "omega": 1.2,\n  "scheme": "Angle and energy dispersive",\n  "wavelength_range": [\n    4.0,\n    12.0\n  ],\n  "wavelength_unit": "Aa"',
        )

    def test_probe_init_a(self):
        p = structure.Probe("neutron")
        assert_equal(p.radiation, "neutron")

    def test_probe_print_a(self):
        p = structure.Probe("neutron")
        assert_equal(p.__repr__(), '  "radiation": "neutron"')

    def test_probe_init_b(self):
        p = structure.Probe("neutron", polarisation=0.97)
        assert_equal(p.radiation, "neutron")
        assert_almost_equal(p.polarisation, 0.97)

    def test_probe_print_b(self):
        p = structure.Probe("neutron", polarisation=0.97)
        assert_equal(p.__repr__(), '  "polarisation": 0.97,\n  "radiation": "neutron"')

    def test_probe_init_c(self):
        p = structure.Probe("neutron", energy=12.5)
        assert_equal(p.radiation, "neutron")
        assert_almost_equal(p.energy, 12.5)

    def test_probe_print_c(self):
        p = structure.Probe("neutron", energy=12.5)
        assert_equal(p.__repr__(), '  "energy": 12.5,\n  "radiation": "neutron"')

    def test_experiment_init(self):
        e = structure.Experiment(
            "ESTIA",
            structure.Probe("neutron"),
            structure.Measurement(
                "Angle and energy dispersive", [4.0, 12.0], [0.3, 2.1]
            ),
            structure.Sample("My Sample"),
        )
        assert_equal(e.instrument, "ESTIA")
        assert_equal(e.probe.radiation, "neutron")
        assert_equal(e.measurement.scheme, "Angle and energy dispersive")
        assert_almost_equal(e.measurement.wavelength_range, [4.0, 12.0])
        assert_almost_equal(e.measurement.angular_range, [0.3, 2.1])
        assert_equal(e.sample.name, "My Sample")

    def test_experiment_print(self):
        e = structure.Experiment(
            "ESTIA",
            structure.Probe("neutron"),
            structure.Measurement(
                "Angle and energy dispersive", [4.0, 12.0], [0.3, 2.1]
            ),
            structure.Sample("My Sample"),
        )
        assert_equal(
            e.__repr__(),
            '  "instrument": "ESTIA",\n  "measurement": {\n    "angular_range": [\n      0.3,\n      2.1\n    ],\n    "angular_unit": "deg",\n    "omega": 0,\n    "scheme": "Angle and energy dispersive",\n    "wavelength_range": [\n      4.0,\n      12.0\n    ],\n    "wavelength_unit": "Aa"\n  },\n  "probe": {\n    "radiation": "neutron"\n  },\n  "sample": {\n    "name": "My Sample"\n  }',
        )
