from typing import Union, Tuple, List

import jpype


class REFRAME:
    def __init__(self, path_reframeLib_jar: str = r'jar/reframeLib.jar', path_jvm_dll: str = r''):

        self._path_lib = path_reframeLib_jar
        self._path_jvm = path_jvm_dll
        self._lib = None

        jpype.addClassPath(self._path_lib)

        if self._path_jvm == '':
            jpype.startJVM(convertStrings=False)
        else:
            jpype.startJVM(self._path_jvm, convertStrings=False)

        javaPackage = jpype.JPackage('com.swisstopo.geodesy.reframe_lib')
        jReframe = javaPackage.Reframe
        jPlanimetricFrame = javaPackage.IReframe.PlanimetricFrame
        jAltimetricFrame = javaPackage.IReframe.AltimetricFrame
        jProjectionChange = javaPackage.IReframe.ProjectionChange

        self._lib = jReframe()

        self.planimetric_frames = {'lv95': jPlanimetricFrame.LV95,
                                   'lv03_military': jPlanimetricFrame.LV03_Military,
                                   'lv03_civil': jPlanimetricFrame.LV03_Civil}

        self.altimetric_frames = {'lhn95': jAltimetricFrame.LHN95,
                                  'ln02': jAltimetricFrame.LN02,
                                  'ellipsoid': jAltimetricFrame.Ellipsoid}

        self.projection_changes = {'etrf93_geocentric_to_lv95': jProjectionChange.ETRF93GeocentricToLV95,
                                   'etrf93_gepgraphic_to_lv95': jProjectionChange.ETRF93GeographicToLV95,
                                   'lv95_to_etrf93_geocentric': jProjectionChange.LV95ToETRF93Geocentric,
                                   'lv95_to_etrf93_geographic': jProjectionChange.LV95ToETRF93Geographic}

    def compute_gpsref(self, coordinates: Union[Tuple[Union[float, int]], List[Union[float, int]]],
                       transformation: str) -> tuple:
        try:
            e_x_long, n_y_lati, h_z_h = float(coordinates[0]), float(coordinates[1]), float(coordinates[2])
        except:
            print('east/x/longitude, north/y/latitude and height/z/height must be float or convertible value')
        else:
            assert transformation in self.projection_changes, 'transformation has to be in: {}'.format(
                list(self.projection_changes.keys()))
            try:
                return tuple(
                    self._lib.ComputeGpsref((e_x_long, n_y_lati, h_z_h),
                                            self.projection_changes[transformation]
                                            )
                )
            except jpype.java.lang.Exception as ex:
                print(ex.stacktrace())

    def compute_reframe(self, coordinates: Union[Tuple[Union[float, int]], List[Union[float, int]]],
                        from_planimetric_frame: str, to_planimetric_frame: str,
                        from_altimetric_frame: str, to_altimetric_frame: str) -> tuple:

        try:
            east, north, height = float(coordinates[0]), float(coordinates[1]), float(coordinates[2])
        except:
            print('east, north and height must be float or convertible value')
        else:
            assert from_planimetric_frame in self.planimetric_frames, 'from_planimetric_frame has to be in: {}'.format(
                list(self.altimetric_frames.keys()))
            assert to_planimetric_frame in self.planimetric_frames, 'to_planimetric_frame has to be in: {}'.format(
                list(self.altimetric_frames.keys()))
            assert from_altimetric_frame in self.altimetric_frames, 'from_altimetric_frame has to be in: {}'.format(
                list(self.altimetric_frames.keys()))
            assert to_altimetric_frame in self.altimetric_frames, 'to_altimetric_frame has to be in: {}'.format(
                list(self.altimetric_frames.keys()))
            try:
                return tuple(
                    self._lib.ComputeReframe((east, north, height),
                                             self.planimetric_frames[from_planimetric_frame],
                                             self.planimetric_frames[to_planimetric_frame],
                                             self.altimetric_frames[from_altimetric_frame],
                                             self.altimetric_frames[to_altimetric_frame],
                                             )
                )
            except jpype.java.lang.Exception as ex:
                print(ex.stacktrace())


r = REFRAME()

# input_coord = ['600000', 200000, 200]
#
# output_coord = r.compute_reframe(input_coord, 'lv03_military', 'lv95', 'ln02', 'lhn95')

input_coord = [7.4412597309, 46.9528818401, 249.6153]
output_coord = r.compute_gpsref(input_coord, 'etrf93_gepgraphic_to_lv95')
print(output_coord)
