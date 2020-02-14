from pkgutil import extend_path
from .beacons import Beacons, BeaconFld, Beacon

__path__ = extend_path(__path__, __name__)
from .beacons import Beacon, BeaconFld, Beacons
