"""
CHIRP CSV Generator.

I find manually programming my FT-65 to be

  - error-prone
  - boring
  - not intuitive

So I decided to try and automate this process.

I have by default selected 6 VU mode sats. And this will generate a CSV file called
CHIRP.csv; You should then be able to load that into CHIRP.

Please note. The FT-65 only stores 1 VFO-A, and Multiple VFO-B (which also annoys me), so you will need to manually
set the uplink frequency. Once set however, it will work for ALL the VFO-B settings.


## Example

```python

from ham.mode.sat import VuBirds, SatFM

if __name__ == "__main__":
    my_local = \"""1,DX1PAR*,144.780000,-,0.600000,,100.0,100.0,023,NN,FM,5.00,S,,,,,
2,DX1ARM,144.280000,-,0.600000,,88.5,88.5,023,NN,FM,0.00,S,,,,,
3,DX2LA,144.900000,-,0.600000,,100.0,100.0,023,NN,FM,0.00,S,,,,,
4,DX3F-2m,144.940000,-,0.600000,,88.5,88.5,023,NN,FM,0.00,S,,,,,
5,DX3F-70,434.900000,-,0.600000,,88.5,88.5,023,NN,FM,0.00,S,,,,,
\"""

"""


from ham.mode.sat import VuBirds, SatFM

if __name__ == "__main__":
    my_local = """1,DX1PAR*,144.780000,-,0.600000,,100.0,100.0,023,NN,FM,5.00,S,,,,,
2,DX1ARM,144.280000,-,0.600000,,88.5,88.5,023,NN,FM,0.00,S,,,,,
3,DX2LA,144.900000,-,0.600000,,100.0,100.0,023,NN,FM,0.00,S,,,,,
4,DX3F-2m,144.940000,-,0.600000,,88.5,88.5,023,NN,FM,0.00,S,,,,,
5,DX3F-70,434.900000,-,0.600000,,88.5,88.5,023,NN,FM,0.00,S,,,,,
"""

    sats = [
        SatFM(
            satname="SO50",
            downlink_freq=436.795,
            uplink_freq=145.850,
            ctss_code=67.0,
            activate_code=74.4,
        ),
        SatFM(
            satname="AO90",
            downlink_freq=435.360,
            uplink_freq=145.350,
            ctss_code=67.0,
            activate_code=0,
        ),
        SatFM(
            satname="AO51",
            downlink_freq=436.795,
            uplink_freq=145.850,
            ctss_code=67.0,
            activate_code=97.4,
        ),
        SatFM(
            satname="AO91",
            downlink_freq=437.225,
            uplink_freq=145.350,
            ctss_code=0,
            activate_code=0,
        ),
        SatFM(
            satname="AO92",
            downlink_freq=435.350,
            uplink_freq=145.880,
            ctss_code=67.0,
            activate_code=0,
        ),
        SatFM(
            satname="Diwt2",
            downlink_freq=437.500,
            uplink_freq=145.900,
            ctss_code=67.0,
            activate_code=0,
        ),
    ]

    print("Starting Fm Sat V/U generator for CHIP for FT-65.")
    vub = VuBirds(my_local)
    with open("tim.csv", "wt") as of:
        of.write(vub.process(sats))
