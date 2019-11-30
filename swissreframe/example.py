from swissreframe import Coordinate, initialize_reframe
from jpype import shutdownJVM


r = initialize_reframe()

print(r.planimetric_frames.keys(), r.altimetric_frames.keys(), r.projection_changes.keys())

result1 = r.compute_reframe((600000.1, 200000.1, 200), 'lv03_military', 'lv95', 'ln02', 'lhn95')
print(result1)
result2 = r.compute_gpsref((2600000.1, 1200000.1, 200), 'lv95_to_etrf93_geographic')
print(result2)

coord = Coordinate(type='world', format='geocentric', coordinates=(4325124.39296, 564701.49101, 4638236.37301))
print(coord.lv03_military_ln02)

coord = Coordinate(type='plane', planimetric_frame='lv03_military', altimetric_frame='ln02',
                   coordinates=(600000.1, 200000.1, 200.1))
print(coord.ETRF95_geocentric)

shutdownJVM()
