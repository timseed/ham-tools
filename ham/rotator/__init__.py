from pkgutil import extend_path

__path__ = extend_path(__path__, __name__)
from .spid3 import Serial3
from .spid_serial3 import spid_serial3
