from typing import Union, Tuple, List

import jpype


class Box:
    pass


global_variables = Box()
global_variables.r = None


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


class Coordinate:

    def __init__(self, **kwargs):

        if len(kwargs) != 0:
            if 'type' in kwargs:
                if kwargs['type'] == 'plane':
                    if 'planimetric_frame' in kwargs and 'altimetric_frame' in kwargs:
                        self._type = 'plane'
                        if kwargs['planimetric_frame'] == 'lv95' and kwargs['altimetric_frame'] == 'ln02':
                            self.lv95_ln02 = kwargs['coordinates']
                        elif kwargs['planimetric_frame'] == 'lv95' and kwargs['altimetric_frame'] == 'lhn95':
                            self.lv95_lhn95 = kwargs['coordinates']
                        elif kwargs['planimetric_frame'] == 'lv95' and kwargs['altimetric_frame'] == 'bessel1841':
                            self.lv95_bessel1841 = kwargs['coordinates']
                        elif kwargs['planimetric_frame'] == 'lv03' and kwargs['altimetric_frame'] == 'ln02':
                            self.lv03_ln02 = kwargs['coordinates']
                        elif kwargs['planimetric_frame'] == 'lv03' and kwargs['altimetric_frame'] == 'lhn95':
                            self.lv03_lhn95 = kwargs['coordinates']
                        elif kwargs['planimetric_frame'] == 'lv03' and kwargs['altimetric_frame'] == 'bessel1841':
                            self.lv03_bessel1841 = kwargs['coordinates']
                        else:

                            if kwargs['planimetric_frame'] not in list_plan_frames:
                                raise ValueError(
                                    'Unknown planimetric frame {}. '
                                    'Choice a planimetric frame from following list: {} '.format(
                                        kwargs['planimetric_frame'], list_plan_frames))
                            if kwargs['altimetric_frame'] not in list_plan_frames:
                                raise ValueError(
                                    'Unknown altimetric frame {}. '
                                    'Choice a altimetric frame from following list: {} '.format(
                                        kwargs['altimetric_frame'], list_alti_frames))

                    else:
                        raise KeyError('You have to specify planimetric and altimetric frame!')

                elif kwargs['type'] == 'world':
                    if 'format' in kwargs:
                        self._type = 'world'
                        if kwargs['format'] == 'geocentric':
                            self.CHTRF95_geozentric = kwargs['coordinates']
                        elif kwargs['format'] == 'geographic':
                            self.CHTRF95_geographic = kwargs['coordinates']
                        else:
                            raise ValueError('Unknown coordinate format {}.'
                                             'Choice coordinate format from following list: {}'.format(kwargs['format'],
                                                                                                       list_world_formats))
                    else:
                        raise KeyError('You have to specify coordinate format! Choice from following list: {}'.format(
                            list_world_formats))
                else:
                    raise ValueError('type has to be "world" or "plane"')

    def _reframe(self, plan_frame_out, alti_frame_out):

        if plan_frame_out in list_plan_frames and alti_frame_out in list_alti_frames:
            return global_variables.r.compute_reframe(self._coord[0], self._coord[1], self._coord[2],
                                                      self._plan_frame, list_plan_frames.index(plan_frame_out),
                                                      self._alt_frame, list_alti_frames.index(alti_frame_out))
        else:
            print('output frames not vaid')

    def _gpsref(self, type_out, world_format):

        if type_out == 'world':
            coord_lv95_bessel1841 = self.lv95_bessel1841
            if world_format == 'geocentric':
                return global_variables.r.compute_gpsref(coord_lv95_bessel1841[0], coord_lv95_bessel1841[1],
                                                         coord_lv95_bessel1841[2], 2)
            elif world_format == 'geographic':
                coord_world = global_variables.r.compute_gpsref(coord_lv95_bessel1841[0], coord_lv95_bessel1841[1],
                                                                coord_lv95_bessel1841[2], 3)
                return coord_world

        if type_out == 'plane':
            if world_format == 'geocentric':
                coord_geozentric = self.CHTRF95_geozentric
                return global_variables.r.compute_gpsref(coord_geozentric[0], coord_geozentric[1],
                                                         coord_geozentric[2], 0)
            elif world_format in list_world_formats:
                if world_format == 'geographic':
                    coord_geographic = self.CHTRF95_geographic
                    return global_variables.r.compute_gpsref(coord_geographic[0], coord_geographic[1],
                                                             coord_geographic[2], 1)

    def _return_coordinates(self, input):
        return input

    @property
    def lv95_lhn95(self):
        if self._type == 'plane':
            output = self._reframe('lv95', 'lhn95')
        elif self._type == 'world':
            coord_lv95_bessel1841 = self._gpsref('plane', self._world_format)[0, 2]
            print(coord_lv95_bessel1841)
        return self._return_coordinates(output)

    @lv95_lhn95.setter
    def lv95_lhn95(self, coord: tuple):
        self._plan_frame = list_plan_frames.index('lv95')
        self._alt_frame = list_alti_frames.index('lhn95')
        self._coord = coord

    @property
    def lv95_ln02(self):
        if self._type == 'plane':
            output = self._reframe('lv95', 'ln02')
        elif self._type == 'world':
            output = None
        return self._return_coordinates(output)

    @lv95_ln02.setter
    def lv95_ln02(self, coord: tuple):
        self._plan_frame = list_plan_frames.index('lv95')
        self._alt_frame = list_alti_frames.index('ln02')
        self._coord = coord

    @property
    def lv95_bessel1841(self):
        if self._type == 'plane':
            output = self._reframe('lv95', 'bessel1841')
        elif self._type == 'world':
            output = None
        return self._return_coordinates(output)

    @lv95_bessel1841.setter
    def lv95_bessel1841(self, coord: tuple):
        self._plan_frame = list_plan_frames.index('lv95')
        self._alt_frame = list_alti_frames.index('bessel1841')
        self._coord = coord

    @property
    def lv03_ln02(self):
        if self._type == 'plane':
            output = self._reframe('lv03', 'ln02')
        elif self._type == 'world':
            output = None
        return self._return_coordinates(output)

    @lv03_ln02.setter
    def lv03_ln02(self, coord: tuple):
        self._plan_frame = list_plan_frames.index('lv03')
        self._alt_frame = list_alti_frames.index('ln02')
        self._coord = coord

    @property
    def lv03_lhn95(self):
        if self._type == 'plane':
            output = self._reframe('lv03', 'lhn95')
        elif self._type == 'world':
            output = None
        return self._return_coordinates(output)

    @lv03_lhn95.setter
    def lv03_lhn95(self, coord: tuple):
        self._plan_frame = list_plan_frames.index('lv03')
        self._alt_frame = list_alti_frames.index('lhn95')
        self._coord = coord

    @property
    def lv03_bessel1841(self):
        if self._type == 'plane':
            output = self._reframe('lv03', 'bessel1841')
        elif self._type == 'world':
            output = None
        return self._return_coordinates(output)

    @lv03_bessel1841.setter
    def lv03_bessel1841(self, coord: tuple):
        self._plan_frame = list_plan_frames.index('lv03')
        self._alt_frame = list_alti_frames.index('bessel1841')
        self._coord = coord

    @property
    def CHTRF95_geozentric(self):
        return self._gpsref('world', 'geocentric')

    @CHTRF95_geozentric.setter
    def CHTRF95_geozentric(self, coord):
        self._world_format = 'geocentric'
        self._coord = coord

    @property
    def CHTRF95_geographic(self):
        return self._gpsref('world', 'geographic')

    @CHTRF95_geographic.setter
    def CHTRF95_geographic(self, coord):
        self._world_format = 'geographic'
        self._coord = coord
