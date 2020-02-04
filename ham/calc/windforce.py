from math import pow


class WindForce(object):
    """
    Some general Wind Calcs for Antenna Loading
    Source:
    http://k7nv.com/notebook/topics/windload.html
    """

    def generic(self, area_sq_ft, wind_in_mph, drag=1.2):
        P = 0.0256 * wind_in_mph * wind_in_mph

        F = P * area_sq_ft * drag

        """
        A = The projected area of the item

        P , Wind pressure (Psf), = .00256 x V^2  (V= wind speed in Mph)

        Cd , Drag coefficient,  = 2.0 for flat plates. For a long cylinder (like most antenna tubes), Cd = 1.2.
        Note the relationship between them is 1.2/2 = .6, not quite 2/3.
        """
        return F

    def eia222f(self, area_sq_ft, wind_in_mph, drag=1.2, height_in_meters=10):
        """
        This is a newer version of the Electronic Industries Assoc. spec.

        Force = A x P x Cd x Kz x Gh
        """
        P = 0.0256 * wind_in_mph * wind_in_mph
        kz = pow((height_in_meters * 3.3 / 33), (2.0 / 7.0))
        gf = pow(0.65 + 0.60 / (height_in_meters * 3.3 / 33), (1.0 / 7.0))
        F = P * area_sq_ft * drag * kz * gf

        return F
