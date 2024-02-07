from dataclasses import dataclass


@dataclass
class WaniKaniRadical:
    level: int
    symbol: str
    meaning: str
    mnemonic: str

