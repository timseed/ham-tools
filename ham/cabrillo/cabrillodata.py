from dataclasses import dataclass


@dataclass
class Cabrillio:
    freq: str
    mode: str
    date: str
    time: str
    my_call: str
    rst: str
    exch: str
    their_call: str


    def as_dict(self)->dict:
        return {
        "freq":self.freq,
        "mode":self.mode,
        "date":self.date,
        "time":self.time,
        "my_call":self.my_call,
        "rst":self.rst,
        "exch":self.exch,
        "their_call":self.their_call}

    @staticmethod
    def fields():
        return   [
            "freq",
            "mode",
            "date",
            "time",
            "my_call",
            "rst",
            "exch",
            "their_call",
        ]