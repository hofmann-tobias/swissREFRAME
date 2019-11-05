from swissreframe import REFRAME, Coordinate
import swissreframe

swissreframe.global_variables.r = REFRAME()

# or specify path to swisstopoReframeLib.tlb
# r = REFRAME(r'C:\Program Files\swisstopo\ReframeDLL\swisstopoReframeLib.tlb')


# result = r.compute_reframe(600000, 200000, 300, 0, 1, 0, 0)
# print(result)
#
# result = r.compute_gpsref(2600000, 1200000, 0, 3)
# print(result)

# help(swissreframe.REFRAME)
# help(swissreframe.Coordinate)

# _coord = Coordinate('P1')
# _coord.lv95_bessel1841 = (2636367, 1244116, 431)
#
# print(_coord.lv95_lhn95)


# coord = Coordinate('P1', type='plane', planimetric_frame='lv03', altimetric_frame='ln02',
#                    coordinates=(600000, 200000, 200))
# print(coord.lv03_ln02)
# print(coord.CHTRF95_geozentric)
# print(coord.lv03_bessel1841)

# coord = Coordinate(type='world', format='geocentric', coordinates=(4453807.37317, 581504.71712, 4513538.02108))
# print(coord._coord)
# print(coord.CHTRF95_geozentric)


coord = Coordinate(type='world', format='geographic', coordinates=(7.4386599242, 45.3319370681, 253.4735))
print(coord.lv95_lhn95)