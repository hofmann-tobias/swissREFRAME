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

