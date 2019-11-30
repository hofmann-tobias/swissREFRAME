from typing import Union, Tuple, List

import jpype
import os


class Box:
    pass


global_variables = Box()
global_variables.r = None


def _get_path(relative_path):
    base_path = os.path.dirname(os.path.abspath(__file__))
    return os.path.join(base_path, relative_path)


def initialize_reframe(path_reframeLib_jar: str = r'jar/reframeLib.jar', path_jvm_dll: str = r''):
    r = REFRAME(path_reframeLib_jar, path_jvm_dll)
    global_variables.r = r
    return r


class REFRAME:
    def __init__(self, path_reframeLib_jar: str = r'jar/reframeLib.jar', path_jvm_dll: str = r''):

        self._path_lib = path_reframeLib_jar
        self._path_jvm = path_jvm_dll
        self._lib = None

        jpype.addClassPath(_get_path(self._path_lib))

        if self._path_jvm == '' and not jpype.isJVMStarted():
            jpype.startJVM(jpype.getDefaultJVMPath(), "-ea", convertStrings=False)
        elif not jpype.isJVMStarted():
            jpype.startJVM(self._path_jvm, "-ea", convertStrings=False)

        javaPackage = jpype.JPackage('com.swisstopo.geodesy.reframe_lib')
        jReframe = jpype.JClass('com.swisstopo.geodesy.reframe_lib.Reframe')
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

    def compute_gpsref(self, coordinates: Union[Tuple[Union[float, int], Union[float, int], Union[float, int]],
                                                List[Union[float, int]]],
                       transformation: str) -> tuple:

        try:
            e_x_long, n_y_lati, h_z_h = float(coordinates[0]), float(coordinates[1]), float(coordinates[2])
        except ValueError:
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

    def compute_reframe(self, coordinates: Union[Tuple[Union[float, int], Union[float, int], Union[float, int]],
                                                 List[Union[float, int]]],
                        from_planimetric_frame: str, to_planimetric_frame: str,
                        from_altimetric_frame: str, to_altimetric_frame: str) -> tuple:

        try:
            east, north, height = float(coordinates[0]), float(coordinates[1]), float(coordinates[2])
        except ValueError:
            print('east, north and height must be float or convertible value')
        else:
            assert from_planimetric_frame in self.planimetric_frames, 'from_planimetric_frame has to be in: {}'.format(
                list(self.planimetric_frames.keys()))
            assert to_planimetric_frame in self.planimetric_frames, 'to_planimetric_frame has to be in: {}'.format(
                list(self.planimetric_frames.keys()))
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
                                             ),

                )
            except jpype.java.lang.Exception as ex:
                print(ex.stacktrace())


class Coordinate:

    def __init__(self, **kwargs):

        if not isinstance(global_variables.r, REFRAME):
            raise ReferenceError('`global_variables.r` is not an instance of swissreframe.REFRAME.\n'
                                 'Execute `global_variables.r = REFRAME()` before create Coordinate instance!')

        elif 'type' in kwargs and 'coordinates' in kwargs:
            self.planimetric_frames = list(global_variables.r.planimetric_frames.keys())
            self.altimetric_frames = list(global_variables.r.altimetric_frames.keys())
            self.world_formats = ['geocentric', 'geographic']

            if kwargs['type'] == 'plane':
                if 'planimetric_frame' in kwargs and 'altimetric_frame' in kwargs:
                    if kwargs['planimetric_frame'] == 'lv95' and kwargs['altimetric_frame'] == 'ln02':
                        self.lv95_ln02 = kwargs['coordinates']
                    elif kwargs['planimetric_frame'] == 'lv95' and kwargs['altimetric_frame'] == 'lhn95':
                        self.lv95_lhn95 = kwargs['coordinates']
                    elif kwargs['planimetric_frame'] == 'lv95' and kwargs['altimetric_frame'] == 'ellipsoid':
                        self.lv95_ellipsoid = kwargs['coordinates']
                    elif kwargs['planimetric_frame'] == 'lv03_military' and kwargs['altimetric_frame'] == 'ln02':
                        self.lv03_military_ln02 = kwargs['coordinates']
                    elif kwargs['planimetric_frame'] == 'lv03_military' and kwargs['altimetric_frame'] == 'lhn95':
                        self.lv03_military_lhn95 = kwargs['coordinates']
                    elif kwargs['planimetric_frame'] == 'lv03_military' and kwargs[
                        'altimetric_frame'] == 'ellipsoid':
                        self.lv03_military_ellipsoid = kwargs['coordinates']
                    else:
                        if kwargs['planimetric_frame'] not in self.planimetric_frames:
                            raise ValueError(
                                'Unknown planimetric frame {}. '
                                'Choice a planimetric frame from following list: {} '.format(
                                    kwargs['planimetric_frame'], self.planimetric_frames))
                        if kwargs['altimetric_frame'] not in self.altimetric_frames:
                            raise ValueError(
                                'Unknown altimetric frame {}. '
                                'Choice a altimetric frame from following list: {} '.format(
                                    kwargs['altimetric_frame'], self.altimetric_frames))
                else:
                    raise KeyError('You have to specify planimetric and altimetric frame!')
            elif kwargs['type'] == 'world':
                if 'format' in kwargs:
                    if kwargs['format'] == 'geocentric':
                        self.ETRF95_geocentric = kwargs['coordinates']
                    elif kwargs['format'] == 'geographic':
                        self.ETRF95_geographic = kwargs['coordinates']
                    else:
                        raise ValueError('Unknown coordinate format {}.'
                                         'Choice coordinate format from following list: {}'.format(kwargs['format'],
                                                                                                   self.world_formats))
                else:
                    raise KeyError('You have to specify coordinate format! Choice from following list: {}'.format(
                        self.world_formats))
            else:
                raise ValueError('``type`` has to be `world` or `plane`')
        else:
            raise AttributeError('Parameters `type`, `coordinates` and either `world_format` or `altimetric_frame` '
                                 'and `planimetric_frame` has to be specified!')

    def __str__(self):
        return '<Coordinate{}>'.format(self._coordinates)

    def __repr__(self):
        return self.__str__()

    def _transform(self, to_type: str, **kwargs):
        if to_type == 'plane' and self._type == 'plane':
            assert 'to_planimetric_frame' in kwargs and 'to_altimetric_frame' in kwargs
            return global_variables.r.compute_reframe(self._coordinates,
                                                      from_planimetric_frame=self._plan_frame,
                                                      to_planimetric_frame=kwargs['to_planimetric_frame'],
                                                      from_altimetric_frame=self._alt_frame,
                                                      to_altimetric_frame=kwargs['to_altimetric_frame']
                                                      )
        elif to_type == 'world' and self._type == 'plane':
            coord_lv95_ellipsoid = self.lv95_ellipsoid
            assert 'to_world_format' in kwargs
            assert coord_lv95_ellipsoid is not None, 'Intermediate transformation lv95/bessel failed'
            if kwargs['to_world_format'] == 'geocentric':
                return global_variables.r.compute_gpsref(coord_lv95_ellipsoid, 'lv95_to_etrf93_geocentric')
            elif kwargs['to_world_format'] == 'geographic':
                return global_variables.r.compute_gpsref(coord_lv95_ellipsoid, 'lv95_to_etrf93_geographic')

        elif to_type == 'plane' and self._type == 'world':
            if self._world_format == 'geocentric':
                coord_lv95_ellipsoid = global_variables.r.compute_gpsref(self._coordinates, 'etrf93_geocentric_to_lv95')
            elif self._world_format == 'geographic':
                coord_lv95_ellipsoid = global_variables.r.compute_gpsref(self._coordinates, 'etrf93_geographic_to_lv95')
            assert 'to_planimetric_frame' in kwargs and 'to_altimetric_frame' in kwargs
            return global_variables.r.compute_reframe(coord_lv95_ellipsoid,
                                                      from_planimetric_frame='lv95',
                                                      to_planimetric_frame=kwargs['to_planimetric_frame'],
                                                      from_altimetric_frame='ellipsoid',
                                                      to_altimetric_frame=kwargs['to_altimetric_frame']
                                                      )
        elif to_type == 'world' and self._type == 'world':
            coord_lv95_ellipsoid = self.lv95_ellipsoid
            assert 'to_world_format' in kwargs
            if kwargs['to_world_format'] == 'geocentric':
                return global_variables.r.compute_gpsref(coord_lv95_ellipsoid, 'lv95_to_etrf93_geocentric')
            elif kwargs['to_world_format'] == 'geographic':
                return global_variables.r.compute_gpsref(coord_lv95_ellipsoid, 'lv95_to_etrf93_geographic')

        else:
            raise NotImplementedError('Unexpected arguments on method Coordinate._transform')

    @property
    def lv95_lhn95(self):
        if self._type == 'plane' and self._plan_frame == 'lv95' and self._alt_frame == 'lhn95':
            return self._coordinates
        else:
            return self._transform(to_type='plane', to_planimetric_frame='lv95', to_altimetric_frame='lhn95')

    @lv95_lhn95.setter
    def lv95_lhn95(self, coordinates: tuple):
        self._type = 'plane'
        self._plan_frame = 'lv95'
        self._alt_frame = 'lhn95'
        self._coordinates = coordinates

    @property
    def lv95_ln02(self):
        if self._type == 'plane' and self._plan_frame == 'lv95' and self._alt_frame == 'ln02':
            return self._coordinates
        else:
            return self._transform(to_type='plane', to_planimetric_frame='lv95', to_altimetric_frame='ln02')

    @lv95_ln02.setter
    def lv95_ln02(self, coordinates: tuple):
        self._type = 'plane'
        self._plan_frame = 'lv95'
        self._alt_frame = 'ln02'
        self._coordinates = coordinates

    @property
    def lv95_ellipsoid(self):
        if self._type == 'plane' and self._plan_frame == 'lv95' and self._alt_frame == 'ellipsoid':
            return self._coordinates
        else:
            return self._transform(to_type='plane', to_planimetric_frame='lv95', to_altimetric_frame='ellipsoid')

    @lv95_ellipsoid.setter
    def lv95_ellipsoid(self, coordinates: tuple):
        self._type = 'plane'
        self._plan_frame = 'lv95'
        self._alt_frame = 'ellipsoid'
        self._coordinates = coordinates

    @property
    def lv03_military_ln02(self):
        if self._type == 'plane' and self._plan_frame == 'lv03_military' and self._alt_frame == 'ln02':
            return self._coordinates
        else:
            return self._transform(to_type='plane', to_planimetric_frame='lv03_military', to_altimetric_frame='ln02')

    @lv03_military_ln02.setter
    def lv03_military_ln02(self, coordinates: tuple):
        self._type = 'plane'
        self._plan_frame = 'lv03_military'
        self._alt_frame = 'ln02'
        self._coordinates = coordinates

    @property
    def lv03_military_lhn95(self):
        if self._type == 'plane' and self._plan_frame == 'lv03_military' and self._alt_frame == 'lhn95':
            return self._coordinates
        else:
            return self._transform(to_type='plane', to_planimetric_frame='lv03_military', to_altimetric_frame='lhn95')

    @lv03_military_lhn95.setter
    def lv03_military_lhn95(self, coordinates: tuple):
        self._type = 'plane'
        self._plan_frame = 'lv03_military'
        self._alt_frame = 'lhn95'
        self._coordinates = coordinates

    @property
    def lv03_military_ellipsoid(self):
        if self._type == 'plane' and self._plan_frame == 'lv03_military' and self._alt_frame == 'ellipsoid':
            return self._coordinates
        else:
            return self._transform(to_type='plane', to_planimetric_frame='lv03_military',
                                   to_altimetric_frame='ellipsoid')

    @lv03_military_ellipsoid.setter
    def lv03_military_ellipsoid(self, coordinates: tuple):
        self._type = 'plane'
        self._plan_frame = 'lv03_military'
        self._alt_frame = 'ellipsoid'
        self._coordinates = coordinates

    @property
    def ETRF95_geocentric(self):
        if self._type == 'world' and self._world_format == 'geocentric':
            return self._coordinates
        else:
            return self._transform(to_type='world', to_world_format='geocentric')

    @ETRF95_geocentric.setter
    def ETRF95_geocentric(self, coordinates):
        self._type = 'world'
        self._world_format = 'geocentric'
        self._coordinates = coordinates

    @property
    def ETRF95_geographic(self):
        if self._type == 'world' and self._world_format == 'geographic':
            return self._coordinates
        else:
            return self._transform(to_type='world', to_world_format='geographic')

    @ETRF95_geographic.setter
    def ETRF95_geographic(self, coordinates):
        self._type = 'world'
        self._world_format = 'geographic'
        self._coordinates = coordinates
