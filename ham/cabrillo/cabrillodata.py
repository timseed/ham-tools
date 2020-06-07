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

    def as_dict(self) -> dict:
        return {
            "freq": self.freq,
            "mode": self.mode,
            "date": self.date,
            "time": self.time,
            "my_call": self.my_call,
            "rst": self.rst,
            "exch": self.exch,
            "their_call": self.their_call,
        }

    @staticmethod
    def fields():
        return [
            "freq",
            "mode",
            "date",
            "time",
            "my_call",
            "rst",
            "exch",
            "their_call",
        ]

        def as_adif(self) -> str:
            return            f"<freq:{len(self.freq)}> {self.freq} "+\
                f"<mode:{len(self.mode)}> {self.self.mode} " +\
                f"<date:{len(self.date)}> {self.self.date} " +\
                f"<time:{len(self.time)}> {self.self.time} " +\
                f"<my_call:{len(self.my_call)}> self.my_call " +\
                f"<rst:{len( self.rst)}>: { self.rst} " "<exch:{len(self.exch)}>: {self.exch} " +\
                f"<their_call:{len(self.their_call)}:  self.their_call "

