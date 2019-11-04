from swissreframe import REFRAME, Coordinate

r = REFRAME()
# or specify path to swisstopoReframeLib.tlb
# r = REFRAME(r'C:\Program Files\swisstopo\ReframeDLL\swisstopoReframeLib.tlb')


# result = r.compute_reframe(600000, 200000, 300, 0, 1, 0, 0)
# print(result)
#
# result = r.compute_gpsref(2600000, 1200000, 0, 3)
# print(result)

# help(swissreframe.REFRAME)
# help(swissreframe.Coordinate)

coord = Coordinate('P1', r)
coord.lv95_bessel1841 = (2636367, 1244116, 431)

print(coord.lv95_lhn95)
