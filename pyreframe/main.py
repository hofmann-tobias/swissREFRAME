import os

from comtypes.client import GetModule, CreateObject


class REFRAME:
    def __init__(self, path=None, strict_mode=True):
        self._path_lib = path
        self._strict_mode = strict_mode
        self._lib = None

        self._connect()

    def _connect(self):
        try:
            # Load Reframe COM library
            if not self._path_lib:
                self._path_lib = os.environ["ProgramFiles"] + "\\swisstopo\\ReframeDLL\\swisstopoReframeLib.tlb"
            GetModule(self._path_lib)

            # Create a new Reframe object
            from comtypes.gen.swisstopoReframeLib import Reframe
            self._lib = CreateObject(Reframe)

        except RuntimeError:
            print("COM error")

    def compute_gpsref(self, east_lon: float, north_lat: float, height_z: float, flag: int):
        """
        Call GPSREF (method “ComputeGpsref”) for transformations between Swiss and global (European/World) coordinates
        (and reference ellipsoid change).
        Check following website for further informations: https://shop.swisstopo.admin.ch/de/products/geo_software/DLL_info

        When the transformation is successful, return_code is 1. When return_code is not 1, the transformation
        could not be performed. Check shell output, return_code and/or return_string for more information.

        Return values:
           1: Computation successfully executed: the coordinates passed by reference have been updated with the new
              output values
          -1: Error: coordinates are outside the official Swiss TLM13 perimeter (invalid input coordinates)
          -2: Error: unsupported value for “flag” argument (only “0”, “1”, “2” or “3” are allowed)

        :param east_lon: float or convertible value
        :param north_lat: float or convertible value
        :param height_z: float or convertible value
        :param flag: integer or convertible value
                        0 -> Global geocentric coordinates (CHTRS95/ETRS89/WGS84) and height on GRS80
                             → Swiss plane coordinates LV95 (CH1903+) and height on Bessel 1841
                        1 -> Global geographic coordinates (CHTRS95/ETRS89/WGS84) and height on GRS80
                             → Swiss plane coordinates LV95 (CH1903+) and height on Bessel 1841
                        2 -> Swiss plane coordinates LV95 (CH1903+) and height on Bessel 1841
                             → Global geocentric coordinates (CHTRS95/ETRS89/WGS84) and height on GRS80
                        3 -> Swiss plane coordinates LV95 (CH1903+) and height on Bessel 1841
                             → Global geographic coordinates (CHTRS95/ETRS89/WGS84) and height on GRS80
        :return: When transformation sucessful: [east_lon, north_lat, height_z, return_code, return_string]
                 When transformation not sucessful: None
        """
        parameters_ok = True
        return_values_dict = {
            1: "Computation successfully executed: the coordinates passed by reference have been updated with the new "
               "output values",
            -1: "Error: coordinates are outside the official Swiss TLM13 perimeter (invalid input coordinates)",
            -2: "Error: unsupported value for “flag” argument (only “0”, “1”, “2” or “3” are allowed)"
        }

        try:
            east_lon = float(east_lon)
            north_lat = float(north_lat)
            height_z = float(height_z)
        except ValueError:
            parameters_ok = False
            print('east/longitude, north/latitude and height/z must be float or convertible value')

        try:
            flag = int(flag)
        except ValueError:
            parameters_ok = False
            print('flag must be integer or convertible value')

        if parameters_ok:
            result = list(self._lib.ComputeGpsref(east_lon, north_lat, height_z, flag))
            result.append(return_values_dict[result[3]])

            return result
        else:
            return None

    def compute_reframe(self, east: float, north: float, height: float, planimetric_frame_in: int,
                        planimetric_frame_out: int, altimetric_frame_in: int, altimetric_frame_out: int):
        """
        Call REFRAME (method “ComputeReframe”) for transformations between Swiss reference frames (planimetry and altimetry).
        Check following website for further informations: https://shop.swisstopo.admin.ch/de/products/geo_software/DLL_info

        When the transformation is successful, return_code is 1. When return_code is not 1, the transformation
        could not be performed. Check shell output, return_code and/or return_string for more information.

        Return values:
          1: Computation successfully executed: the coordinates passed by reference have been updated with the new output
            values
         -1: Error: specified point outside of the CHENyx06 triangular network (input coordinates outside boundaries)
             Note: for a planimetric transformation LV03↔LV95, if the input point is outside the CHENyx06 triangular
             network (what means outside the official Swiss TLM perimeter) the transformation is officially defined as
             a translation of +/- 2’000’000 m and +/- 1’000’000 m.
         -2: Error: specified point outside of the HTRANS or CHGeo2004 grid (input coordinates outside boundaries)
         -3: Error: problem occurred when reading a binary file. Check that all the binary files  (datasets definitions)
             are correctly installed and valid (try to recover/recopy the original versions). Reinstall the REFRAME DLL
             if the problem persists.
         -4: Error: unsupported value for “planimetric_frame_in” or “planimetric_frame_out” argument (only “0” or “1”
             are allowed)
         -5: Error: unsupported value for “altimetric_frame_in” or “altimetric_frame_out” argument (only “0”, “1” or
             “2” are allowed)
         -6: Error: input and output reference frames (planimetry and altimetry) are the same, there isn’t any
             transformation to do!
        -10: Error: CHENyx06 dataset inaccessible (from binary file “swisstopo.data.dll”). Check if the file exists
             in the application directory (next to “swisstopoReframeLib.dll”) and that it is accessible
             (enough rights). Reinstall the REFRAME DLL if the problem persists.
        -11: Error: HTRANS dataset inaccessible (from binary file “swisstopo.data.dll”). Check if the file exists in
             the application directory (next to “swisstopoReframeLib.dll”) and that it is accessible (enough rights).
             Reinstall the REFRAME DLL if the problem persists.
        -12: Error: CHGeo2004 dataset is inaccessible (from binary file “swisstopo.data.dll”). Check if the file exists
             in the application directory (next to “swisstopoReframeLib.dll”) and that it is accessible
             (enough rights). Reinstall the REFRAME DLL if the problem persists.


        :param east: float or convertible value
        :param north: float or convertible value
        :param height: float or convertible value
        :param planimetric_frame_in: integer or convertible value
                                        0 -> Swiss plane coordinates LV03 (CH1903)
                                        1 -> Swiss plane coordinates LV95 (CH1903+)
        :param planimetric_frame_out: integer or convertible value
                                        0 -> Swiss plane coordinates LV03 (CH1903)
                                        1 -> Swiss plane coordinates LV95 (CH1903+)
        :param altimetric_frame_in: integer or convertible value
                                        0 -> National levelling network LN02 (levelled heights)
                                        1 -> National height network LHN95 (orthometric heights, CHGeo2004)
                                        2 -> Ellipsoidal heights (on Bessel 1841)
        :param altimetric_frame_out: integer or convertible value
                                        0 -> National levelling network LN02 (levelled heights)
                                        1 -> National height network LHN95 (orthometric heights, CHGeo2004)
                                        2 -> Ellipsoidal heights (on Bessel 1841)
        :return: When transformation sucessful: [east, north, height, return_code, return_string]
                 When transformation not sucessful: None
        """
        parameters_ok = True
        return_values_dict = {
            1: "Computation successfully executed: the coordinates passed by reference have been updated with "
               "the new output values",
            -1: "Error: specified point outside of the CHENyx06 triangular network (input coordinates outside "
                "boundaries) \nNote: for a planimetric transformation LV03↔LV95, if the input point is outside the "
                "CHENyx06 triangular network (what means outside the official Swiss TLM perimeter) the transformation "
                "is officially defined as a translation of +/- 2’000’000 m and +/- 1’000’000 m.",
            -2: "Error: specified point outside of the HTRANS or CHGeo2004 grid (input coordinates outside boundaries)",
            -3: "Error: problem occurred when reading a binary file. Check that all the binary files  (datasets "
                "definitions) are correctly installed and valid (try to recover/recopy the original versions). "
                "Reinstall the REFRAME DLL if the problem persists.",
            -4: "Error: unsupported value for “planimetric_frame_in” or “planimetric_frame_out” argument (only “0” "
                "or “1” are allowed)",
            -5: "Error: unsupported value for “altimetric_frame_in” or “altimetric_frame_out” argument (only “0”, "
                "“1” or “2” are allowed)",
            -6: "Error: input and output reference frames (planimetry and altimetry) are the same, there isn’t any "
                "transformation to do!",
            -10: "Error: CHENyx06 dataset inaccessible (from binary file “swisstopo.data.dll”). Check if the file "
                 "exists in the application directory (next to “swisstopoReframeLib.dll”) and that it is accessible "
                 "(enough rights). Reinstall the REFRAME DLL if the problem persists.",
            -11: "Error: HTRANS dataset inaccessible (from binary file “swisstopo.data.dll”). Check if the file "
                 "exists in the application directory (next to “swisstopoReframeLib.dll”) and that it is accessible "
                 "(enough rights). Reinstall the REFRAME DLL if the problem persists.",
            -12: "Error: CHGeo2004 dataset is inaccessible (from binary file “swisstopo.data.dll”). Check if the "
                 "file exists in the application directory (next to “swisstopoReframeLib.dll”) and that it is "
                 "accessible (enough rights). Reinstall the REFRAME DLL if the problem persists."
        }

        try:
            east = float(east)
            north = float(north)
            height = float(height)
        except ValueError:
            parameters_ok = False
            print('east, north and height must be float or convertible value')

        try:
            planimetric_frame_in = int(planimetric_frame_in)
            planimetric_frame_out = int(planimetric_frame_out)
            altimetric_frame_in = int(altimetric_frame_in)
            altimetric_frame_out = int(altimetric_frame_out)
        except ValueError:
            parameters_ok = False
            print('frame code must be integer or convertible value')

        if parameters_ok:
            result = list(self._lib.ComputeReframe(east, north, height, planimetric_frame_in, planimetric_frame_out,
                                                   altimetric_frame_in, altimetric_frame_out))
            result.append(return_values_dict[result[3]])

            return result
        else:
            return None
