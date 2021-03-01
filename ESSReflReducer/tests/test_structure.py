"""
Tests for header module
"""

# Copyright (c) Andrew R. McCluskey
# Distributed under the terms of the MIT License
# author: Andrew R. McCluskey

import unittest
from numpy.testing import assert_almost_equal, assert_equal
from datetime import datetime, date
from ESSReflReducer import header, __version__

PERSON = header.Person("Brian", "A N University")
TODAY = datetime.now().strftime("%Y-%m-%d, %H:%M:%S")
TODAY_DATE = date.today()


class TestHeader(unittest.TestCase):
    def test_person_init_a(self):
        p = header.Person("Brian")
        assert_equal(p.name, "Brian")
        assert_equal(p.affiliation, "European Spallation Source")

    def test_person_init_b(self):
        assert_equal(PERSON.name, "Brian")
        assert_equal(PERSON.affiliation, "A N University")

    def test_person_repr(self):
        expect = '  "affiliation": "A N University",\n  "name": "Brian"'
        assert_equal(PERSON.__repr__(), expect)

    def test_creation_init_a(self):
        c = header.Creation(PERSON)
        assert_equal(len(c.owners), 1)
        assert_equal(c.owners[0], PERSON)
        assert_equal(c.time, f"{TODAY}")
        assert_equal(c.system, "dmsc.ess.eu")

    def test_creation_init_b(self):
        c = header.Creation([PERSON, header.Person("Colin")])
        assert_equal(len(c.owners), 2)
        assert_equal(c.owners[0], PERSON)
        assert_equal(c.owners[1].name, "Colin")
        assert_equal(c.owners[1].affiliation, "European Spallation Source")
        assert_equal(c.time, f"{TODAY}")
        assert_equal(c.system, "dmsc.ess.eu")

    def test_creation_init_c(self):
        c = header.Creation(PERSON, time=datetime(2021, 2, 25, 13, 11, 10, 981419))
        assert_equal(len(c.owners), 1)
        assert_equal(c.owners[0], PERSON)
        assert_equal(c.time, "2021-02-25, 13:11:10")

    def test_creation_init_d(self):
        c = header.Creation(PERSON, system="estia.ess.eu")
        assert_equal(len(c.owners), 1)
        assert_equal(c.owners[0], PERSON)
        assert_equal(c.system, "estia.ess.eu")

    def test_creation_print(self):
        c = header.Creation(PERSON, time=datetime(2021, 2, 25, 13, 11, 10, 981419))
        assert_equal(
            c.__repr__(),
            '  "owners": [\n    {\n      "affiliation": "A N University",\n      "name": "Brian"\n    }\n  ],\n  "system": "dmsc.ess.eu",\n  "time": "2021-02-25, 13:11:10"',
        )

    def test_origin_init_a(self):
        o = header.Origin(PERSON, "40208", "An example experiment")
        assert_equal(len(o.owners), 1)
        assert_equal(o.owners[0], PERSON)
        assert_equal(o.experiment_id, "40208")
        assert_equal(o.title, "An example experiment")
        assert_equal(o.facility, "European Spallation Source")
        assert_equal(o.experiment_start, TODAY_DATE)
        assert_equal(o.experiment_end, TODAY_DATE)

    def test_origin_init_b(self):
        o = header.Origin(
            [PERSON, header.Person("Colin")], "40208", "An example experiment"
        )
        assert_equal(len(o.owners), 2)
        assert_equal(o.owners[0], PERSON)
        assert_equal(o.owners[1].name, "Colin")
        assert_equal(o.owners[1].affiliation, "European Spallation Source")
        assert_equal(o.experiment_id, "40208")
        assert_equal(o.title, "An example experiment")
        assert_equal(o.facility, "European Spallation Source")
        assert_equal(o.experiment_start, TODAY_DATE)
        assert_equal(o.experiment_end, TODAY_DATE)

    def test_origin_init_c(self):
        o = header.Origin(
            [PERSON, header.Person("Colin")],
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
        assert_equal(o.experiment_start, TODAY_DATE)
        assert_equal(o.experiment_end, TODAY_DATE)

    def test_origin_init_d(self):
        o = header.Origin(
            [PERSON, header.Person("Colin")],
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
        assert_equal(o.experiment_start, datetime(1992, 7, 14, 6, 11, 20))
        assert_equal(o.experiment_end, TODAY_DATE)

    def test_origin_init_e(self):
        o = header.Origin(
            [PERSON, header.Person("Colin")],
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
        assert_equal(o.experiment_start, TODAY_DATE)
        assert_equal(o.experiment_end, datetime(1994, 11, 29, 2, 50, 42))

    def test_origin_print(self):
        o = header.Origin(PERSON, "40208", "An example experiment")
        assert_equal(
            o.__repr__(),
            '  "experiment_end": "'
            + TODAY[:-10]
            + '",\n  "experiment_id": "40208",\n  "experiment_start": "'
            + TODAY[:-10]
            + '",\n  "facility": "European Spallation Source",\n  "owners": [\n    {\n      "affiliation": "A N University",\n      "name": "Brian"\n    }\n  ],\n  "title": "An example experiment"',
        )

    def test_layer_init_a(self):
        l = header.Layer("Air")
        assert_equal(l.name, "Air")

    def test_layer_print_a(self):
        l = header.Layer("Air")
        assert_equal(l.__repr__(), '  "name": "Air"')

    def test_layer_init_b(self):
        l = header.Layer("Air", sld=2 + 3j)
        assert_equal(l.name, "Air")
        assert_almost_equal(l.sld, 2 + 3j)

    def test_layer_print_b(self):
        l = header.Layer("Air", sld=2 + 3j)
        assert_equal(l.__repr__(), '  "name": "Air",\n  "sld": "(2+3j)"')

    def test_layer_init_c(self):
        l = header.Layer("Air", thickness=100)
        assert_equal(l.name, "Air")
        assert_almost_equal(l.thickness, 100)

    def test_layer_print_c(self):
        l = header.Layer("Air", thickness=100)
        assert_equal(l.__repr__(), '  "name": "Air",\n  "thickness": 100')

    def test_layer_init_d(self):
        l = header.Layer("Air", magnetisation_vector=-0.5)
        assert_equal(l.name, "Air")
        assert_almost_equal(l.magnetisation_vector, -0.5)

    def test_layer_print_d(self):
        l = header.Layer("Air", magnetisation_vector=-0.5)
        assert_equal(l.__repr__(), '  "magnetisation_vector": -0.5,\n  "name": "Air"')

    def test_sample_init_a(self):
        s = header.Sample("My Sample")
        assert_equal(s.name, "My Sample")

    def test_sample_print_a(self):
        s = header.Sample("My Sample")
        assert_equal(s.__repr__(), '  "name": "My Sample"')

    def test_sample_init_b(self):
        s = header.Sample(
            "My Sample",
            description=[
                header.Layer("Air"),
                header.Layer("Lipids"),
                header.Layer("Water"),
            ],
        )
        assert_equal(s.name, "My Sample")
        assert_equal(s.description[0].name, "Air")
        assert_equal(s.description[1].name, "Lipids")
        assert_equal(s.description[2].name, "Water")

    def test_sample_print_b(self):
        s = header.Sample(
            "My Sample",
            description=[
                header.Layer("Air"),
                header.Layer("Lipids"),
                header.Layer("Water"),
            ],
        )
        assert_equal(
            s.__repr__(),
            '  "description": [\n    {\n      "name": "Air"\n    },\n    {\n      "name": "Lipids"\n    },\n    {\n      "name": "Water"\n    }\n  ],\n  "name": "My Sample"',
        )

    def test_measurement_init_a(self):
        m = header.Measurement(
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
        m = header.Measurement(
            "Angle and energy dispersive", [4.0, 12.0], [0.3, 2.1]
        )
        assert_equal(
            m.__repr__(),
            '  "angular_range": [\n    0.3,\n    2.1\n  ],\n  "angular_unit": "deg",\n  "omega": 0,\n  "scheme": "Angle and energy dispersive",\n  "wavelength_range": [\n    4.0,\n    12.0\n  ],\n  "wavelength_unit": "Aa"',
        )

    def test_measurement_init_b(self):
        m = header.Measurement(
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
        m = header.Measurement(
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
        m = header.Measurement(
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
        m = header.Measurement(
            "Angle and energy dispersive", [4.0, 12.0], [0.3, 2.1], angular_unit="rad"
        )
        assert_equal(
            m.__repr__(),
            '  "angular_range": [\n    0.3,\n    2.1\n  ],\n  "angular_unit": "rad",\n  "omega": 0,\n  "scheme": "Angle and energy dispersive",\n  "wavelength_range": [\n    4.0,\n    12.0\n  ],\n  "wavelength_unit": "Aa"',
        )

    def test_measurement_init_c(self):
        m = header.Measurement(
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
        m = header.Measurement(
            "Angle and energy dispersive", [4.0, 12.0], [0.3, 2.1], omega=1.2
        )
        assert_equal(
            m.__repr__(),
            '  "angular_range": [\n    0.3,\n    2.1\n  ],\n  "angular_unit": "deg",\n  "omega": 1.2,\n  "scheme": "Angle and energy dispersive",\n  "wavelength_range": [\n    4.0,\n    12.0\n  ],\n  "wavelength_unit": "Aa"',
        )

    def test_probe_init_a(self):
        p = header.Probe("neutron")
        assert_equal(p.radiation, "neutron")

    def test_probe_print_a(self):
        p = header.Probe("neutron")
        assert_equal(p.__repr__(), '  "radiation": "neutron"')

    def test_probe_init_b(self):
        p = header.Probe("neutron", polarisation=0.97)
        assert_equal(p.radiation, "neutron")
        assert_almost_equal(p.polarisation, 0.97)

    def test_probe_print_b(self):
        p = header.Probe("neutron", polarisation=0.97)
        assert_equal(p.__repr__(), '  "polarisation": 0.97,\n  "radiation": "neutron"')

    def test_experiment_init(self):
        e = header.Experiment(
            "ESTIA",
            header.Probe("neutron"),
            header.Measurement(
                "Angle and energy dispersive", [4.0, 12.0], [0.3, 2.1]
            ),
            header.Sample("My Sample"),
        )
        assert_equal(e.instrument, "ESTIA")
        assert_equal(e.probe.radiation, "neutron")
        assert_equal(e.measurement.scheme, "Angle and energy dispersive")
        assert_almost_equal(e.measurement.wavelength_range, [4.0, 12.0])
        assert_almost_equal(e.measurement.angular_range, [0.3, 2.1])
        assert_equal(e.sample.name, "My Sample")

    def test_experiment_print(self):
        e = header.Experiment(
            "ESTIA",
            header.Probe("neutron"),
            header.Measurement(
                "Angle and energy dispersive", [4.0, 12.0], [0.3, 2.1]
            ),
            header.Sample("My Sample"),
        )
        assert_equal(
            e.__repr__(),
            '  "instrument": "ESTIA",\n  "measurement": {\n    "angular_range": [\n      0.3,\n      2.1\n    ],\n    "angular_unit": "deg",\n    "omega": 0,\n    "scheme": "Angle and energy dispersive",\n    "wavelength_range": [\n      4.0,\n      12.0\n    ],\n    "wavelength_unit": "Aa"\n  },\n  "probe": {\n    "radiation": "neutron"\n  },\n  "sample": {\n    "name": "My Sample"\n  }',
        )

    def test_datasource_init(self):
        o = header.Origin(PERSON, "40208", "An example experiment")
        e = header.Experiment(
            "ESTIA",
            header.Probe("neutron"),
            header.Measurement(
                "Angle and energy dispersive", [4.0, 12.0], [0.3, 2.1]
            ),
            header.Sample("My Sample"),
        )
        links = {
            "related extensive file": "fulldatafile.hdf",
            "instrument reference": "doi:10.1016/j.nima.2016.03.007",
        }
        ds = header.DataSource(o, e, links)
        assert_equal(ds.origin.owners[0].name, "Brian")
        assert_equal(ds.experiment.instrument, "ESTIA")
        assert_equal(ds.links, links)

    def test_datasource_print(self):
        o = header.Origin(PERSON, "40208", "An example experiment")
        e = header.Experiment(
            "ESTIA",
            header.Probe("neutron"),
            header.Measurement(
                "Angle and energy dispersive", [4.0, 12.0], [0.3, 2.1]
            ),
            header.Sample("My Sample"),
        )
        links = {
            "related extensive file": "fulldatafile.hdf",
            "instrument reference": "doi:10.1016/j.nima.2016.03.007",
        }
        ds = header.DataSource(o, e, links)
        assert_equal(
            ds.__repr__(),
            '  "experiment": {\n    "instrument": "ESTIA",\n    "measurement": {\n      "angular_range": [\n        0.3,\n        2.1\n      ],\n      "angular_unit": "deg",\n      "omega": 0,\n      "scheme": "Angle and energy dispersive",\n      "wavelength_range": [\n        4.0,\n        12.0\n      ],\n      "wavelength_unit": "Aa"\n    },\n    "probe": {\n      "radiation": "neutron"\n    },\n    "sample": {\n      "name": "My Sample"\n    }\n  },\n  "links": {\n    "instrument reference": "doi:10.1016/j.nima.2016.03.007",\n    "related extensive file": "fulldatafile.hdf"\n  },\n  "origin": {\n    "experiment_end": "'
            + TODAY[:-10]
            + '",\n    "experiment_id": "40208",\n    "experiment_start": "'
            + TODAY[:-10]
            + '",\n    "facility": "European Spallation Source",\n    "owners": [\n      {\n        "affiliation": "A N University",\n        "name": "Brian"\n      }\n    ],\n    "title": "An example experiment"\n  }',
        )

    def test_file_init_a(self):
        f = header.File("test.dat")
        assert_equal(f.filename.as_posix(), "test.dat")
        assert_equal(f.creation_time.strftime("%Y-%m-%d, %H:"), f"{TODAY[:-5]}")

    def test_file_init_b(self):
        f = header.File("test.dat", creation_time=datetime(1994, 11, 29, 2, 50, 42))
        assert_equal(f.filename.as_posix(), "test.dat")
        assert_equal(f.creation_time, datetime(1994, 11, 29, 2, 50, 42))

    def test_file_print(self):
        f = header.File("test.dat", creation_time=datetime(1994, 11, 29, 2, 50, 42))
        assert_equal(
            f.__repr__(),
            '  "creation_time": "1994-11-29, 02:50:42",\n  "filename": "test.dat"',
        )

    def test_file_dir(self):
        f = header.File("/a/b/test.dat")
        assert_equal(f.dir, '/a/b')

    def test_file_ext(self):
        f = header.File("/a/b/test.dat")
        assert_equal(f.ext, '.dat')

    def test_file_name(self):
        f = header.File("/a/b/test.dat")
        assert_equal(f.name, 'test')

    def test_software_init(self):
        s = header.Software(header.File("/a/b/test.py"))
        assert_equal(s.name, "ESSReflReducer")
        assert_equal(s.version, __version__)
        assert_equal(s.script.filename.as_posix(), "/a/b/test.py")

    def test_software_print(self):
        s = header.Software(header.File("/a/b/test.py", creation_time=datetime(1994, 11, 29, 2, 50, 42)))
        assert_equal(s.__repr__(), '  "name": "ESSReflReducer",\n  "script": {\n    "creation_time": "1994-11-29, 02:50:42",\n    "filename": "/a/b/test.py"\n  },\n  "version": "0.0.1"')

    def test_data_state_init_a(self):
        ds = header.DataState()
        assert_equal(ds.footprint, None)
        assert_equal(ds.intensity, None)
        assert_equal(ds.resolution, None)
        assert_equal(ds.absorption, None)
        assert_equal(ds.background, None)

    def test_data_state_print_a(self):
        ds = header.DataState()
        assert_equal(ds.__repr__(), '  "absorption": null,\n  "background": null,\n  "footprint": null,\n  "intensity": null,\n  "resolution": null')

    def test_data_state_init_b(self):
        ds = header.DataState()
        ds.footprint = 'corrected'
        ds.intensity = 'normalised'
        ds.resolution = 'calculated, based on wavelength resolution and detector spatial resolution'
        ds.absorption = 'uncorrected, not needed'
        ds.background = 'uncorrected'
        assert_equal(ds.footprint, 'corrected')
        assert_equal(ds.intensity, 'normalised')
        assert_equal(ds.resolution, 'calculated, based on wavelength resolution and detector spatial resolution')
        assert_equal(ds.absorption, 'uncorrected, not needed')
        assert_equal(ds.background, 'uncorrected')

    def test_data_state_print_b(self):
        ds = header.DataState()
        ds.footprint = 'corrected'
        ds.intensity = 'normalised'
        ds.resolution = 'calculated, based on wavelength resolution and detector spatial resolution'
        ds.absorption = 'uncorrected, not needed'
        ds.background = 'uncorrected'
        assert_equal(ds.__repr__(), '  "absorption": "uncorrected, not needed",\n  "background": "uncorrected",\n  "footprint": "corrected",\n  "intensity": "normalised",\n  "resolution": "calculated, based on wavelength resolution and detector spatial resolution"')

    def test_data_init(self):
        cols = {"col 1": "qz/Aa-1",
                "col 2": "Rqz",
                "col 3": "sigma Rqz , standard deviation",
                "col 4": "sigma Qz / Aa^-1, standard deviation"}
        d = header.Data(cols)
        assert_equal(d.columns, cols)

    def test_data_print(self):
        cols = {"col 1": "qz/Aa-1",
                "col 2": "Rqz",
                "col 3": "sigma Rqz , standard deviation",
                "col 4": "sigma qz / Aa^-1, standard deviation"}
        d = header.Data(cols)
        assert_equal(d.columns.__repr__(), "{'col 1': 'qz/Aa-1', 'col 2': 'Rqz', 'col 3': 'sigma Rqz , standard deviation', 'col 4': 'sigma qz / Aa^-1, standard deviation'}")

    def test_reduction_init(self):
        s = header.Software(header.File("/a/b/test.py", creation_time=datetime(1994, 11, 29, 2, 50, 42)))
        ds = header.DataState()
        files = [header.File("/a/b/file1.nxs", creation_time=datetime(2001, 11, 29, 2, 23, 42)),
                 header.File("/a/b/file2.nxs", creation_time=datetime(2011, 11, 29, 2, 24, 42)),
                 header.File("/a/b/file3.nxs", creation_time=datetime(2022, 11, 29, 2, 25, 42))]
        r = header.Reduction(s, files, ds)
        assert_equal(r.software.name, 'ESSReflReducer')
        assert_equal(r.input_files[0].filename.as_posix(), "/a/b/file1.nxs")
        assert_equal(r.input_files[1].filename.as_posix(), "/a/b/file2.nxs")
        assert_equal(r.input_files[2].filename.as_posix(), "/a/b/file3.nxs")
        assert_equal(r.data_state.absorption, None)

    def test_reduction_print(self):
        s = header.Software(header.File("/a/b/test.py", creation_time=datetime(1994, 11, 29, 2, 50, 42)))
        ds = header.DataState()
        files = [header.File("/a/b/file1.nxs", creation_time=datetime(2001, 11, 29, 2, 23, 42)),
                 header.File("/a/b/file2.nxs", creation_time=datetime(2011, 11, 29, 2, 24, 42)),
                 header.File("/a/b/file3.nxs", creation_time=datetime(2022, 11, 29, 2, 25, 42))]
        r = header.Reduction(s, files, ds)
        assert_equal(r.__repr__(), '  "data_state": {\n    "absorption": null,\n    "background": null,\n    "footprint": null,\n    "intensity": null,\n    "resolution": null\n  },\n  "input_files": [\n    {\n      "creation_time": "2001-11-29, 02:23:42",\n      "filename": "/a/b/file1.nxs"\n    },\n    {\n      "creation_time": "2011-11-29, 02:24:42",\n      "filename": "/a/b/file2.nxs"\n    },\n    {\n      "creation_time": "2022-11-29, 02:25:42",\n      "filename": "/a/b/file3.nxs"\n    }\n  ],\n  "software": {\n    "name": "ESSReflReducer",\n    "script": {\n      "creation_time": "1994-11-29, 02:50:42",\n      "filename": "/a/b/test.py"\n    },\n    "version": "0.0.1"\n  }')


    def test_orso_init(self):
        c = header.Creation(PERSON)
        oo = header.Origin(PERSON, "40208", "An example experiment")
        e = header.Experiment(
            "ESTIA",
            header.Probe("neutron"),
            header.Measurement(
                "Angle and energy dispersive", [4.0, 12.0], [0.3, 2.1]
            ),
            header.Sample("My Sample"),
        )
        links = {
            "related extensive file": "fulldatafile.hdf",
            "instrument reference": "doi:10.1016/j.nima.2016.03.007",
        }
        ds = header.DataSource(oo, e, links)
        s = header.Software(header.File("/a/b/test.py", creation_time=datetime(1994, 11, 29, 2, 50, 42)))
        dss = header.DataState()
        files = [header.File("/a/b/file1.nxs", creation_time=datetime(2001, 11, 29, 2, 23, 42)),
                 header.File("/a/b/file2.nxs", creation_time=datetime(2011, 11, 29, 2, 24, 42)),
                 header.File("/a/b/file3.nxs", creation_time=datetime(2022, 11, 29, 2, 25, 42))]
        r = header.Reduction(s, files, dss)
        cols = {"col 1": "qz/Aa-1",
                "col 2": "Rqz",
                "col 3": "sigma Rqz , standard deviation",
                "col 4": "sigma Qz / Aa^-1, standard deviation"}
        d = header.Data(cols)
        o = header.ORSO(c, ds, r, d)
        assert_equal(o.creation.owners[0].name, 'Brian')
        assert_equal(o.data_source.experiment.instrument, 'ESTIA')
        assert_equal(o.reduction.software.name, 'ESSReflReducer')
        assert_equal(o.data.columns['col 1'], 'qz/Aa-1')

    def test_orso_print(self):
        c = header.Creation(PERSON)
        c.time = datetime(1994, 11, 29, 2, 50, 42)
        oo = header.Origin(PERSON, "40208", "An example experiment")
        e = header.Experiment(
            "ESTIA",
            header.Probe("neutron"),
            header.Measurement(
                "Angle and energy dispersive", [4.0, 12.0], [0.3, 2.1]
            ),
            header.Sample("My Sample"),
        )
        links = {
            "related extensive file": "fulldatafile.hdf",
            "instrument reference": "doi:10.1016/j.nima.2016.03.007",
        }
        ds = header.DataSource(oo, e, links)
        s = header.Software(header.File("/a/b/test.py", creation_time=datetime(1994, 11, 29, 2, 50, 42)))
        dss = header.DataState()
        files = [header.File("/a/b/file1.nxs", creation_time=datetime(2001, 11, 29, 2, 23, 42)),
                 header.File("/a/b/file2.nxs", creation_time=datetime(2011, 11, 29, 2, 24, 42)),
                 header.File("/a/b/file3.nxs", creation_time=datetime(2022, 11, 29, 2, 25, 42))]
        r = header.Reduction(s, files, dss)
        cols = {"col 1": "qz/Aa-1",
                "col 2": "Rqz",
                "col 3": "sigma Rqz , standard deviation",
                "col 4": "sigma Qz / Aa^-1, standard deviation"}
        d = header.Data(cols)
        o = header.ORSO(c, ds, r, d)
        assert_equal(o.__repr__(), '  "creation": {\n    "owners": [\n      {\n        "affiliation": "A N University",\n        "name": "Brian"\n      }\n    ],\n    "system": "dmsc.ess.eu",\n    "time": "1994-11-29, 02:50:42"\n  },\n  "data": {\n    "columns": {\n      "col 1": "qz/Aa-1",\n      "col 2": "Rqz",\n      "col 3": "sigma Rqz , standard deviation",\n      "col 4": "sigma Qz / Aa^-1, standard deviation"\n    }\n  },\n  "data_source": {\n    "experiment": {\n      "instrument": "ESTIA",\n      "measurement": {\n        "angular_range": [\n          0.3,\n          2.1\n        ],\n        "angular_unit": "deg",\n        "omega": 0,\n        "scheme": "Angle and energy dispersive",\n        "wavelength_range": [\n          4.0,\n          12.0\n        ],\n        "wavelength_unit": "Aa"\n      },\n      "probe": {\n        "radiation": "neutron"\n      },\n      "sample": {\n        "name": "My Sample"\n      }\n    },\n    "links": {\n      "instrument reference": "doi:10.1016/j.nima.2016.03.007",\n      "related extensive file": "fulldatafile.hdf"\n    },\n    "origin": {\n      "experiment_end": "2021-03-01",\n      "experiment_id": "40208",\n      "experiment_start": "2021-03-01",\n      "facility": "European Spallation Source",\n      "owners": [\n        {\n          "affiliation": "A N University",\n          "name": "Brian"\n        }\n      ],\n      "title": "An example experiment"\n    }\n  },\n  "reduction": {\n    "data_state": {\n      "absorption": null,\n      "background": null,\n      "footprint": null,\n      "intensity": null,\n      "resolution": null\n    },\n    "input_files": [\n      {\n        "creation_time": "2001-11-29, 02:23:42",\n        "filename": "/a/b/file1.nxs"\n      },\n      {\n        "creation_time": "2011-11-29, 02:24:42",\n        "filename": "/a/b/file2.nxs"\n      },\n      {\n        "creation_time": "2022-11-29, 02:25:42",\n        "filename": "/a/b/file3.nxs"\n      }\n    ],\n    "software": {\n      "name": "ESSReflReducer",\n      "script": {\n        "creation_time": "1994-11-29, 02:50:42",\n        "filename": "/a/b/test.py"\n      },\n      "version": "0.0.1"\n    }\n  }')
