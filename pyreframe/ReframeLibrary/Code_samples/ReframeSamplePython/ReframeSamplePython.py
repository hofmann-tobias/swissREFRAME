import os

try:
    # Load Reframe COM library
    from comtypes.client import GetModule, CreateObject

    GetModule(os.environ["ProgramFiles"] + "\\swisstopo\\ReframeDLL\\swisstopoReframeLib.tlb")

    # Create a new Reframe object
    from comtypes.gen.swisstopoReframeLib import Reframe

    o = CreateObject(Reframe)

    # Input coordinates: read in a file, got from a textbox, or obtained through another method or library...
    e_lv03 = 601000.0
    n_lv03 = 197500.0
    h_ln02 = 555.0

    # Transform LV03 coordinates to LV95 and LN02 height to Bessel
    result = o.ComputeReframe(e_lv03, n_lv03, h_ln02, 0, 1, 0, 2)

    # Save results to variables
    e_lv95 = result[0]
    n_lv95 = result[1]
    h_bessel = result[2]
    retcode = result[3]

    # Analyze result
    if retcode == 1:  # OK
        print(str(e_lv95) + " / " + str(n_lv95) + " / " + str(h_bessel))
    else:  # Error
        print("Reframe error")  # TODO

    # Transform LV95 coordinates to ETRS89 longitude/latitude and ellipsoidal height on Bessel to GRS80
    result = o.ComputeGpsref(e_lv95, n_lv95, h_bessel, 3)

    # Save results to variables
    lon_etrf93 = result[0]
    lat_etrf93 = result[1]
    h_etrf93 = result[2]
    retcode = result[3]

    # Analyze result
    if retcode == 1:  # OK
        print(str(lon_etrf93) + " / " + str(lat_etrf93) + " / " + str(h_etrf93))
    else:  # Error
        print("Gpsref error")  # TODO

except RuntimeError:
    print("COM error")  # TODO
