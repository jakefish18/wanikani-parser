from dataclasses import dataclass


@dataclass
class WKRadical:
    """Dataclass for a WaniKani radical."""
    level: int
    symbol: str
    meaning: str
    mnemonic: str