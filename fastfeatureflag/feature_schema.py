from dataclasses import dataclass


@dataclass
class Feature:
    name: str
    activation: str
    shadow: str | None = None
