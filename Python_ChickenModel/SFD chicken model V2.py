"""
Python model 'SFD chicken model V2.py'
Translated using PySD
"""

from pathlib import Path
import numpy as np

from pysd.py_backend.statefuls import Integ
from pysd import Component

__pysd_version__ = "3.12.0"

__data = {"scope": None, "time": lambda: 0}

_root = Path(__file__).parent


component = Component()

#######################################################################
#                          CONTROL VARIABLES                          #
#######################################################################

_control_vars = {
    "initial_time": lambda: 0,
    "final_time": lambda: 50,
    "time_step": lambda: 1,
    "saveper": lambda: time_step(),
}


def _init_outer_references(data):
    for key in data:
        __data[key] = data[key]


@component.add(name="Time")
def time():
    """
    Current time of the model.
    """
    return __data["time"]()


@component.add(
    name="FINAL TIME", units="Day", comp_type="Constant", comp_subtype="Normal"
)
def final_time():
    """
    The final time for the simulation.
    """
    return __data["time"].final_time()


@component.add(
    name="INITIAL TIME", units="Day", comp_type="Constant", comp_subtype="Normal"
)
def initial_time():
    """
    The initial time for the simulation.
    """
    return __data["time"].initial_time()


@component.add(
    name="SAVEPER",
    units="Day",
    limits=(0.0, np.nan),
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={"time_step": 1},
)
def saveper():
    """
    The frequency with which output is stored.
    """
    return __data["time"].saveper()


@component.add(
    name="TIME STEP",
    units="Day",
    limits=(0.0, np.nan),
    comp_type="Constant",
    comp_subtype="Normal",
)
def time_step():
    """
    The time step for the simulation.
    """
    return __data["time"].time_step()


#######################################################################
#                           MODEL VARIABLES                           #
#######################################################################


@component.add(
    name="Births",
    units="Chickens/Day",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={"eggs": 1, "incubation_time": 1},
)
def births():
    return eggs() / incubation_time()


@component.add(
    name="Chickens",
    units="Chickens",
    comp_type="Stateful",
    comp_subtype="Integ",
    depends_on={"_integ_chickens": 1},
    other_deps={
        "_integ_chickens": {
            "initial": {"initial_chicken_population": 1},
            "step": {"births": 1, "deaths": 1},
        }
    },
)
def chickens():
    return _integ_chickens()


_integ_chickens = Integ(
    lambda: births() - deaths(), lambda: initial_chicken_population(), "_integ_chickens"
)


@component.add(
    name="Cross roading",
    units="Dmnl",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={"stress": 1},
)
def cross_roading():
    return stress()


@component.add(
    name="Death risk",
    units="1/Day",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={"normal_death_risk": 1, "cross_roading": 1},
)
def death_risk():
    return normal_death_risk() * cross_roading()


@component.add(
    name="Deaths",
    units="Chickens/Day",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={"chickens": 1, "death_risk": 1},
)
def deaths():
    return chickens() * death_risk()


@component.add(
    name="Egg production",
    units="Eggs/Day",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={"chickens": 1, "fertility_effect": 1},
)
def egg_production():
    return chickens() * fertility_effect()


@component.add(
    name="Eggs",
    units="Eggs",
    comp_type="Stateful",
    comp_subtype="Integ",
    depends_on={"_integ_eggs": 1},
    other_deps={
        "_integ_eggs": {
            "initial": {"initial_number_of_eggs": 1},
            "step": {"egg_production": 1, "births": 1},
        }
    },
)
def eggs():
    return _integ_eggs()


_integ_eggs = Integ(
    lambda: egg_production() - births(), lambda: initial_number_of_eggs(), "_integ_eggs"
)


@component.add(
    name="Fertility effect",
    units="Eggs/Chickens/Day",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={"normal_fertility_rate": 1, "stress": 1},
)
def fertility_effect():
    return normal_fertility_rate() / stress()


@component.add(
    name="Incubation time",
    units="Day",
    limits=(0.0, 30.0, 1.0),
    comp_type="Constant",
    comp_subtype="Normal",
)
def incubation_time():
    return 5


@component.add(
    name="Initial chicken population",
    units="Chickens",
    limits=(0.0, 4000.0, 10.0),
    comp_type="Constant",
    comp_subtype="Normal",
)
def initial_chicken_population():
    return 1000


@component.add(
    name="Initial number of eggs",
    units="Eggs",
    limits=(0.0, 2000.0),
    comp_type="Constant",
    comp_subtype="Normal",
)
def initial_number_of_eggs():
    return 1000


@component.add(
    name="Max chicken capacity",
    units="Chickens",
    limits=(1.0, 2000.0, 10.0),
    comp_type="Constant",
    comp_subtype="Normal",
)
def max_chicken_capacity():
    return 1000


@component.add(
    name="Normal death risk",
    units="1/Day",
    limits=(0.0, 1.0, 0.01),
    comp_type="Constant",
    comp_subtype="Normal",
)
def normal_death_risk():
    return 0.2


@component.add(
    name="Normal fertility rate",
    units="Eggs/Chickens/Day",
    limits=(0.0, 1.0, 0.01),
    comp_type="Constant",
    comp_subtype="Normal",
)
def normal_fertility_rate():
    return 0.2


@component.add(
    name="Stress",
    units="Dmnl",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={"chickens": 1, "max_chicken_capacity": 1},
)
def stress():
    return chickens() / max_chicken_capacity()
