import os

from comtypes.client import GetModule, CreateObject

list_plan_frames = ['lv03', 'lv95']
list_alti_frames = ['ln02', 'lhn95', 'bessel1841']


class REFRAME:
    def __init__(self, path: str = None, strict_mode: bool = True):
        """

        :param str path: path to `swisstopoReframeLib.tlb`, if not installed in default installation directory
        :param bool strict_mode: if True, methods ``compute_gpsref`` and ``compute_reframe`` will only return
        coordinates if the transformation was successful
        """
        self._path_lib = path
        self._strict_mode = strict_mode
        self._lib = None

        self._connect()

    def _connect(self):
        """
        This method loads COM lobrary and create a new Reframe object
        :return: None
        """
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

    def compute_gpsref(self, east_x_lon: float, north_y_lat: float, height_z: float, flag: int):
        """
        Call GPSREF (method ``ComputeGpsref``) for transformations between Swiss and global (European/World)
        coordinates (and reference ellipsoid change).
        Check following website for further informations:
        https://shop.swisstopo.admin.ch/de/products/geo_software/DLL_info

        When the transformation is successful, return_code is 1. When return_code is not 1, the transformation
        could not be performed. Check shell output, return_code and/or return_string for more information.

        Return values:
           1: Computation successfully executed: the coordinates passed by reference have been updated with the
              new output values
          -1: Error: coordinates are outside the official Swiss TLM13 perimeter (invalid input coordinates)
          -2: Error: unsupported value for ``flag`` argument (only ``0``, ``1``, ``2`` or ``3`` are allowed)

        :param float east_x_lon: east or longitude value
        :param float north_y_lat: north or latitude value
        :param float height_z: height (on geoid) or z (on ellipsoid) value
        :param int flag: 
                        0 -> Global geocentric coordinates (CHTRS95/ETRS89/WGS84) and height on GRS80
                             -> Swiss plane coordinates LV95 (CH1903+) and height on Bessel 1841
                        1 -> Global geographic coordinates (CHTRS95/ETRS89/WGS84) and height on GRS80
                             -> Swiss plane coordinates LV95 (CH1903+) and height on Bessel 1841
                        2 -> Swiss plane coordinates LV95 (CH1903+) and height on Bessel 1841
                             -> Global geocentric coordinates (CHTRS95/ETRS89/WGS84) and height on GRS80
                        3 -> Swiss plane coordinates LV95 (CH1903+) and height on Bessel 1841
                             -> Global geographic coordinates (CHTRS95/ETRS89/WGS84) and height on GRS80
        :return: When transformation was sucessful: [east_lon, north_y_lat, height_z, return_code, return_string]
                 When transformation was not sucessful: None
        """
        parameters_ok = True
        return_values_dict = {
            1: "Computation successfully executed: the coordinates passed by reference have been updated with the new "
               "output values",
            -1: "Error: coordinates are outside the official Swiss TLM13 perimeter (invalid input coordinates)",
            -2: "Error: unsupported value for ``flag`` argument (only ``0``, ``1``, ``2`` or ``3`` are allowed)"
        }

        try:
            east_x_lon = float(east_x_lon)
            north_y_lat = float(north_y_lat)
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
            result = list(self._lib.ComputeGpsref(east_x_lon, north_y_lat, height_z, flag))
            result.append(return_values_dict[result[3]])

            return result
        else:
            return None

    def compute_reframe(self, east: float, north: float, height: float, planimetric_frame_in: int,
                        planimetric_frame_out: int, altimetric_frame_in: int, altimetric_frame_out: int):
        """
        Call REFRAME (method ``ComputeReframe``) for transformations between Swiss reference frames
        (planimetry and altimetry).
        Check following website for further informations:
        https://shop.swisstopo.admin.ch/de/products/geo_software/DLL_info

        When the transformation is successful, return_code is 1. When return_code is not 1, the transformation
        could not be performed. Check shell output, return_code and/or return_string for more information.

        Return values:
          1: Computation successfully executed: the coordinates passed by reference have been updated with the
             new output values
         -1: Error: specified point outside of the CHENyx06 triangular network (input coordinates outside
             boundaries)
             Note: for a planimetric transformation LV03↔LV95, if the input point is outside the CHENyx06
             triangular network (what means outside the official Swiss TLM perimeter) the transformation is
             officially defined as a translation of +/- 2'000'000 m and +/- 1'000'000 m.
         -2: Error: specified point outside of the HTRANS or CHGeo2004 grid (input coordinates outside
             boundaries)
         -3: Error: problem occurred when reading a binary file. Check that all the binary files
             (datasets definitions) are correctly installed and valid (try to recover/recopy the original
             versions). Reinstall the REFRAME DLL if the problem persists.
         -4: Error: unsupported value for ``planimetric_frame_in`` or ``planimetric_frame_out`` argument
             (only ``0`` or ``1`` are allowed)
         -5: Error: unsupported value for ``altimetric_frame_in`` or ``altimetric_frame_out`` argument
             (only ``0``, ``1`` or ``2`` are allowed)
         -6: Error: input and output reference frames (planimetry and altimetry) are the same, there isn't any
             transformation to do!
        -10: Error: CHENyx06 dataset inaccessible (from binary file ``swisstopo.data.dll``). Check if the file
             exists in the application directory (next to ``swisstopoReframeLib.dll``) and that it is
             accessible (enough rights). Reinstall the REFRAME DLL if the problem persists.
        -11: Error: HTRANS dataset inaccessible (from binary file ``swisstopo.data.dll``). Check if the file
             exists in the application directory (next to ``swisstopoReframeLib.dll``) and that it is accessible
             (enough rights). Reinstall the REFRAME DLL if the problem persists.
        -12: Error: CHGeo2004 dataset is inaccessible (from binary file ``swisstopo.data.dll``). Check if the
             file exists in the application directory (next to ``swisstopoReframeLib.dll``) and that it is
             accessible (enough rights). Reinstall the REFRAME DLL if the problem persists.


        :param float east: east / Y value
        :param float north: north / X value
        :param float height: height value
        :param int planimetric_frame_in:
                                        0 -> Swiss plane coordinates LV03 (CH1903)
                                        1 -> Swiss plane coordinates LV95 (CH1903+)
        :param int planimetric_frame_out:
                                        0 -> Swiss plane coordinates LV03 (CH1903)
                                        1 -> Swiss plane coordinates LV95 (CH1903+)
        :param int altimetric_frame_in:
                                        0 -> National levelling network LN02 (levelled heights)
                                        1 -> National height network LHN95 (orthometric heights, CHGeo2004)
                                        2 -> Ellipsoidal heights (on Bessel 1841)
        :param int altimetric_frame_out:
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
                "is officially defined as a translation of +/- 2'000'000 m and +/- 1'000'000 m.",
            -2: "Error: specified point outside of the HTRANS or CHGeo2004 grid (input coordinates outside boundaries)",
            -3: "Error: problem occurred when reading a binary file. Check that all the binary files  (datasets "
                "definitions) are correctly installed and valid (try to recover/recopy the original versions). "
                "Reinstall the REFRAME DLL if the problem persists.",
            -4: "Error: unsupported value for ``planimetric_frame_in`` or ``planimetric_frame_out`` argument (only ``0`` "
                "or ``1`` are allowed)",
            -5: "Error: unsupported value for ``altimetric_frame_in`` or ``altimetric_frame_out`` argument (only ``0``, "
                "``1`` or ``2`` are allowed)",
            -6: "Error: input and output reference frames (planimetry and altimetry) are the same, there isn't any "
                "transformation to do!",
            -10: "Error: CHENyx06 dataset inaccessible (from binary file ``swisstopo.data.dll``). Check if the file "
                 "exists in the application directory (next to ``swisstopoReframeLib.dll``) and that it is accessible "
                 "(enough rights). Reinstall the REFRAME DLL if the problem persists.",
            -11: "Error: HTRANS dataset inaccessible (from binary file ``swisstopo.data.dll``). Check if the file "
                 "exists in the application directory (next to ``swisstopoReframeLib.dll``) and that it is accessible "
                 "(enough rights). Reinstall the REFRAME DLL if the problem persists.",
            -12: "Error: CHGeo2004 dataset is inaccessible (from binary file ``swisstopo.data.dll``). Check if the "
                 "file exists in the application directory (next to ``swisstopoReframeLib.dll``) and that it is "
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
            try:
                result.append(return_values_dict[result[3]])
            except:
                print('return_code not found in dict')

            return result
        else:
            return None


class Coordinate:
    def __init__(self, name: str, r: REFRAME, planimetric_frame: str = '', altimetric_frame: str = '',
                 coordinates: tuple = None):
        self.name = name
        self.r = r

        if planimetric_frame != '' and planimetric_frame in list_plan_frames:
            if altimetric_frame != '' and altimetric_frame in list_alti_frames:
                self.plan_frame = list_plan_frames.index(planimetric_frame)
                self.alt_frame = list_alti_frames.index(altimetric_frame)
                self.coord = coordinates
            else:
                print('frame not valid')
        else:
            pass

    def _transform(self, plan_frame_out, alti_frame_out):

        if plan_frame_out in list_plan_frames and alti_frame_out in list_alti_frames:
            return self.r.compute_reframe(self.coord[0], self.coord[1], self.coord[2],
                                          self.plan_frame, list_plan_frames.index(plan_frame_out),
                                          self.alt_frame, list_alti_frames.index(alti_frame_out))
        else:
            print('output frames not vaid')

    def _gpsref_lv952geoz(self):
        coord_lv95 = self.lv95_bessel1841
        return self.r.compute_gpsref(coord_lv95[0], coord_lv95[1], coord_lv95[2], 2)

    @property
    def lv95_lhn95(self):
        return self._transform('lv95', 'lhn95')

    @lv95_lhn95.setter
    def lv95_lhn95(self, coord: tuple):
        self.plan_frame = list_plan_frames.index('lv95')
        self.alt_frame = list_alti_frames.index('lhn95')
        self.coord = coord

    @property
    def lv95_ln02(self):
        return self._transform('lv95', 'ln02')

    @lv95_ln02.setter
    def lv95_ln02(self, coord: tuple):
        self.plan_frame = list_plan_frames.index('lv95')
        self.alt_frame = list_alti_frames.index('ln02')
        self.coord = coord

    @property
    def lv95_bessel1841(self):
        return self._transform('lv95', 'bessel1841')

    @lv95_bessel1841.setter
    def lv95_bessel1841(self, coord: tuple):
        self.plan_frame = list_plan_frames.index('lv95')
        self.alt_frame = list_alti_frames.index('bessel1841')
        self.coord = coord

    @property
    def lv03_ln02(self):
        return self._transform('lv03', 'ln02')

    @lv03_ln02.setter
    def lv03_ln02(self, coord: tuple):
        self.plan_frame = list_plan_frames.index('lv03')
        self.alt_frame = list_alti_frames.index('ln02')
        self.coord = coord

    @property
    def lv03_lhn95(self):
        return self._transform('lv03', 'lhn95')

    @lv03_lhn95.setter
    def lv03_lhn95(self, coord: tuple):
        self.plan_frame = list_plan_frames.index('lv03')
        self.alt_frame = list_alti_frames.index('lhn95')
        self.coord = coord

    @property
    def lv03_bessel1841(self):
        return self._transform('lv03', 'bessel1841')

    @lv03_bessel1841.setter
    def lv03_bessel1841(self, coord: tuple):
        self.plan_frame = list_plan_frames.index('lv03')
        self.alt_frame = list_alti_frames.index('bessel1841')
        self.coord = coord

    @property
    def CHTRF95_geoz(self):
        return self._gpsref_lv952geoz()

    @CHTRF95_geoz.setter
    def CHTRF95_geoz(self, coord):
        self.chtrs95_geoz = coord
