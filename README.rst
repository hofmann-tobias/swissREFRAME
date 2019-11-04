swissREFRAME
============
Python interface for the official swisstopo's REFRAME DLL (currently only suited for Windows)

About REFRAME
^^^^^^^^^^^^^
Info about DLL / Source: https://shop.swisstopo.admin.ch/de/products/geo_software/DLL_info

GeoSuite calculation module for planimetric and/or height transformation for application in the Swiss national survey and the cadastral survey. The REFRAME library allows all transformations of coordinates and heights, which are relevant in Switzerland and available in the REFRAME for GeoSuite software, except UTM projection:

* GPSREF (ETRF93 <-> LV95)
* FINELTRA (LV95 <-> LV03)
* CHGEO2004 (geoid model)
* HTRANS (LHN95 <-> LN02)

The REFRAME library may be distributed to third parties and integrated into commercial products, but it must be delivered to the customer free of charge.

``ReframeLibrary/Documentation/developper_manual.pdf`` contains all technical information about REFRAME library.

Installation
^^^^^^^^^^^^
1. | install COM-version of the REFRAME dll's ``ReframeLibrary/Binaries/COM_version/Setup/ReframeComDll_x{}.msi``
   | Best do not change the installation path!


2. install the package:

.. code-block:: sh

    pip install swissreframe

Requirements
^^^^^^^^^^^^

* Windows (tested with Version	10.0.18362 Build 18362)
* comtypes (tested with V1.1.7)
* Python 3 (tested with 3.7.5)



Example
^^^^^^^
.. code-block:: python

    from swissreframe import REFRAME

    r = REFRAME()

This will work, if REFRAME is installed in the default installation path (``C:\Program Files\swisstopo\ReframeDLL\swisstopoReframeLib.tlb``).

You can also specify path to `swisstopoReframeLib.tlb`:

.. code-block:: python

    r = REFRAME(r'C:\swisstopo\ReframeDLL\swisstopoReframeLib.tlb')

Now you can use the methods ``REFRAME.compute_reframe`` and ``REFRAME.compute_gpsref``

.. code-block:: python

    result1 = r.compute_reframe(600000, 200000, 300, 0, 1, 0, 0)
    print(result1)
    result2 = r.compute_gpsref(2600000, 1200000, 0, 3)
    print(result2)

Output:

.. code-block:: python

    [2600000.0, 1200000.0, 300.0, 1, 'Computation successfully executed: the coordinates passed by reference have been updated with the new output values']
    [7.438632420871814, 46.9510827728495, 49.6221914421767, 1, 'Computation successfully executed: the coordinates passed by reference have been updated with the new output values']


Documentation
^^^^^^^^^^^^^
.. code-block::

    Help on class REFRAME in module swissreframe._classes:

    class REFRAME(builtins.object)
     |  REFRAME(path: str = None, strict_mode: bool = True)
     |
     |  Methods defined here:
     |
     |  __init__(self, path: str = None, strict_mode: bool = True)
     |      :param str path: path to `swisstopoReframeLib.tlb`, if not installed in default installation directory
     |      :param bool strict_mode: if True, methods ``compute_gpsref`` and ``compute_reframe`` will only return
     |      coordinates if the transformation was successful
     |
     |  compute_gpsref(self, east_lon: float, north_lat: float, height_z: float, flag: int)
     |      Call GPSREF (method ``ComputeGpsref``) for transformations between Swiss and global (European/World) coordinates
     |      (and reference ellipsoid change).
     |      Check following website for further informations: https://shop.swisstopo.admin.ch/de/products/geo_software/DLL_info
     |
     |      When the transformation is successful, return_code is 1. When return_code is not 1, the transformation
     |      could not be performed. Check shell output, return_code and/or return_string for more information.
     |
     |      Return values:
     |         1: Computation successfully executed: the coordinates passed by reference have been updated with the new
     |            output values
     |        -1: Error: coordinates are outside the official Swiss TLM13 perimeter (invalid input coordinates)
     |        -2: Error: unsupported value for ``flag`` argument (only ``0``, ``1``, ``2`` or ``3`` are allowed)
     |
     |      :param float east_lon: east or longitude value
     |      :param float north_lat: north or latitude value
     |      :param float height_z: height (on geoid) or z (on ellipsoid) value
     |      :param int flag:
     |                      0 -> Global geocentric coordinates (CHTRS95/ETRS89/WGS84) and height on GRS80
     |                           -> Swiss plane coordinates LV95 (CH1903+) and height on Bessel 1841
     |                      1 -> Global geographic coordinates (CHTRS95/ETRS89/WGS84) and height on GRS80
     |                           -> Swiss plane coordinates LV95 (CH1903+) and height on Bessel 1841
     |                      2 -> Swiss plane coordinates LV95 (CH1903+) and height on Bessel 1841
     |                           -> Global geocentric coordinates (CHTRS95/ETRS89/WGS84) and height on GRS80
     |                      3 -> Swiss plane coordinates LV95 (CH1903+) and height on Bessel 1841
     |                           -> Global geographic coordinates (CHTRS95/ETRS89/WGS84) and height on GRS80
     |      :return: When transformation was sucessful: [east_lon, north_lat, height_z, return_code, return_string]
     |               When transformation was not sucessful: None
     |
     |  compute_reframe(self, east: float, north: float, height: float, planimetric_frame_in: int, planimetric_frame_out: int, altimetric_frame_in: int, altimetric_frame_out: int)
     |      Call REFRAME (method ``ComputeReframe``) for transformations between Swiss reference frames (planimetry and altimetry).
     |      Check following website for further informations: https://shop.swisstopo.admin.ch/de/products/geo_software/DLL_info
     |
     |      When the transformation is successful, return_code is 1. When return_code is not 1, the transformation
     |      could not be performed. Check shell output, return_code and/or return_string for more information.
     |
     |      Return values:
     |        1: Computation successfully executed: the coordinates passed by reference have been updated with the new output
     |          values
     |       -1: Error: specified point outside of the CHENyx06 triangular network (input coordinates outside boundaries)
     |           Note: for a planimetric transformation LV03↔LV95, if the input point is outside the CHENyx06 triangular
     |           network (what means outside the official Swiss TLM perimeter) the transformation is officially defined as
     |           a translation of +/- 2'000'000 m and +/- 1'000'000 m.
     |       -2: Error: specified point outside of the HTRANS or CHGeo2004 grid (input coordinates outside boundaries)
     |       -3: Error: problem occurred when reading a binary file. Check that all the binary files  (datasets definitions)
     |           are correctly installed and valid (try to recover/recopy the original versions). Reinstall the REFRAME DLL
     |           if the problem persists.
     |       -4: Error: unsupported value for ``planimetric_frame_in`` or ``planimetric_frame_out`` argument (only ``0`` or ``1``
     |           are allowed)
     |       -5: Error: unsupported value for ``altimetric_frame_in`` or ``altimetric_frame_out`` argument (only ``0``, ``1`` or
     |           ``2`` are allowed)
     |       -6: Error: input and output reference frames (planimetry and altimetry) are the same, there isn't any
     |           transformation to do!
     |      -10: Error: CHENyx06 dataset inaccessible (from binary file ``swisstopo.data.dll``). Check if the file exists
     |           in the application directory (next to ``swisstopoReframeLib.dll``) and that it is accessible
     |           (enough rights). Reinstall the REFRAME DLL if the problem persists.
     |      -11: Error: HTRANS dataset inaccessible (from binary file ``swisstopo.data.dll``). Check if the file exists in
     |           the application directory (next to ``swisstopoReframeLib.dll``) and that it is accessible (enough rights).
     |           Reinstall the REFRAME DLL if the problem persists.
     |      -12: Error: CHGeo2004 dataset is inaccessible (from binary file ``swisstopo.data.dll``). Check if the file exists
     |           in the application directory (next to ``swisstopoReframeLib.dll``) and that it is accessible
     |           (enough rights). Reinstall the REFRAME DLL if the problem persists.
     |
     |
     |      :param float east: east / Y value
     |      :param float north: north / X value
     |      :param float height: height value
     |      :param int planimetric_frame_in:
     |                                      0 -> Swiss plane coordinates LV03 (CH1903)
     |                                      1 -> Swiss plane coordinates LV95 (CH1903+)
     |      :param int planimetric_frame_out:
     |                                      0 -> Swiss plane coordinates LV03 (CH1903)
     |                                      1 -> Swiss plane coordinates LV95 (CH1903+)
     |      :param int altimetric_frame_in:
     |                                      0 -> National levelling network LN02 (levelled heights)
     |                                      1 -> National height network LHN95 (orthometric heights, CHGeo2004)
     |                                      2 -> Ellipsoidal heights (on Bessel 1841)
     |      :param int altimetric_frame_out:
     |                                      0 -> National levelling network LN02 (levelled heights)
     |                                      1 -> National height network LHN95 (orthometric heights, CHGeo2004)
     |                                      2 -> Ellipsoidal heights (on Bessel 1841)
     |      :return: When transformation sucessful: [east, north, height, return_code, return_string]
     |               When transformation not sucessful: None
     |
     |  ----------------------------------------------------------------------
     |  Data descriptors defined here:
     |
     |  __dict__
     |      dictionary for instance variables (if defined)
     |
     |  __weakref__
     |      list of weak references to the object (if defined)