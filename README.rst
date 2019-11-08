This is a prototype!


swissREFRAME
============
Python interface for the official swisstopo's REFRAME jar library

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
Just install the package:

.. code-block:: sh

    pip install swissreframe

Requirements
^^^^^^^^^^^^
* Java x64/x86 (swissREFRAME starts a JVM to execute REFRAME jar library, tested with 8.0_231)
* Python 3 (tested with 3.7.5)
* JPype1 (tested with 0.7.0)



Example / Usage
^^^^^^^
.. code-block:: python

    from swissreframe import REFRAME, Coordinate, global_variables

    global_variables.r = REFRAME()

This should work. But you can also specify path to ``reframeLib.jar``:

.. code-block:: python

    global_variables.r = REFRAME(path_reframeLib_jar = r'D:\jar\reframeLib.jar')

and also path to ``jvm.dll``:

.. code-block:: python

    global_variables.r = REFRAME(path_reframeLib_jar = r'C:\Program Files\Java\jre1.8.0_231\bin\server\jvm.dll')


Now you can use the methods ``REFRAME.compute_reframe`` and ``REFRAME.compute_gpsref``

.. code-block:: python

    result1 = global_variables.r.compute_reframe((600000.1, 200000.1, 200), 'lv03_military', 'lv95', 'ln02', 'lhn95')
    print(result1)
    result2 = r.compute_gpsref((2600000.1, 1200000.1, 200), 'lv95_to_etrf93_geographic')
    print(result2)

Output:

.. code-block:: python

    (2600000.182999904, 1200000.1660008044, 199.92481259693554)
    (7.438633764230579, 46.95108371391055, 249.62218793481588)
    
Or you can use class Coordinate and its methods:

.. code-block:: python

    coord = Coordinate(type='plane', planimetric_frame='lv03_military', altimetric_frame='ln02',
                       coordinates=(600000.1, 200000.1, 200.1))
    print(coord.ETRFF95_geozentric)

Output:

.. code-block:: python

    (4325124.392962725, 564701.4910050733, 4638236.373010437)


Documentation
^^^^^^^^^^^^^
Coming soon
