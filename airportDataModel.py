import re
from typing import Tuple
from pydantic import BaseModel, constr

class Comunication(BaseModel):
    twr: list[constr(pattern=r'^\d{3}\.\d{3}$')] | None = None
    gnd: list[constr(pattern=r'^\d{3}\.\d{3}$')] | None = None
    ops: list[constr(pattern=r'^\d{3}\.\d{3}$')] | None = None
    atis: list[constr(pattern=r'^\d{3}\.\d{3}$')] | None = None
    traf: list[constr(pattern=r'^\d{3}\.\d{3}$')] | None = None

class Vor(BaseModel):
    ident: str
    freq: constr(pattern=r'^\d{3}\.\d$')

class Ils(BaseModel):
    rwy: constr(pattern=r'^\d{2}[L|C|R]*$')
    ident: constr(pattern=r'^[A-Z]{3}$')
    freq: constr(pattern=r'^\d{3}\.\d$')

class Rwy(BaseModel):
    head: Tuple[constr(pattern=r'^(\d{2}|\d)(R|L|C)*$'), constr(pattern=r'^(\d{2}|\d)(R|L|C)*$')]
    length: int

class Airport(BaseModel):
    nome: str
    icao: constr(pattern=r'^[A-Z]{4}$')
    comunication: Comunication | None = None
    ils: list[Ils] | None = None
    vor: list[Vor] | None = None
    rwy: list[Rwy]