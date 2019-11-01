# PyREFRAME
Python interface for the official swisstopo's REFRAME DLL

## About REFRAME
https://shop.swisstopo.admin.ch/de/products/geo_software/DLL_info

The REFRAME library allows all transformations of coordinates and heights, which are relevant in Switzerland and available in the REFRAME for GeoSuite software, except UTM projection:
* GPSREF (ETRF93 <-> LV95)
* FINELTRA (LV95 <-> LV03)
* CHGEO2004 (geoid model)
* HTRANS (LHN95 <-> LN02)

## Installation
First, install COM-version of the REFRAME dll's `ReframeLibrary/Binaries/COM_version/Setup/ReframeComDll_x{}.msi`\
Best do not change the installation path!\

Then, install the package:\
``pip install swissreframe``

## Requirements
* comtypes
* Python 3 (tested with 3.7.5)

## Example
`from swissreframe import REFRAME` 

Instance class REFRAME:\
``r = REFRAME()`` 

or specify path to swisstopoReframeLib.tlb:\
``r = REFRAME(r'C:\Program Files\swisstopo\ReframeDLL\swisstopoReframeLib.tlb')``

`result1 = r.compute_reframe(600000, 200000, 300, 0, 1, 0, 0)`\
`print(result1)`\
`result2 = r.compute_gpsref(2600000, 1200000, 0, 3)\`\
`print(result2)`

Returns:\
``[2600000.0, 1200000.0, 300.0, 1, 'Computation successfully executed: the coordinates passed by reference have been updated with the new output values']``

``[7.438632420871814, 46.9510827728495, 49.6221914421767, 1, 'Computation successfully executed: the coordinates passed by reference have been updated with the new output values']``