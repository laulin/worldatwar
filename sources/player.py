import unittest

from ressources import Ressources
from warehouse import Warehouse

class Player:
    # This class contains all player data.
    # it is just a wrapper around warehouse class.
    def __init__(self, configuration):
        self._ressources = Ressources(configuration)

        # build a dict with all keys
        # contains all units available
        self._units = Warehouse("units", configuration)

        #contains all defenses available
        self._defenses = Warehouse("defenses", configuration)

        # define tech available
        self._tech = Warehouse("tech", configuration)

        # mail box
        # @TODO
        self._mail_box = []

    def check_min_ressources(self, values):
        # from a list a ressource values, return True if ressources are available
        self._ressources.is_available(values)

    def check_min_units(self, units):
        # check a min quantity of units
        return self._units.check_min(units)

    def check_min_tech(self, tech):
        # check a min tech level
        return  self._tech.check_min(tech)

    def get_ressources(self):
        return zip(self._ressources.get_value(), self._ressources.get_delta())

    def get_units(self):
        return self._units.get()

    def get_defenses(self):
        return self._defenses.get()

    def get_tech(self):
        return self._tech.get()

    def add_units(self, units):
        self._units.add(units)

    def add_defenses(self, defenses):
        self._defenses.add(defenses)

    def inc_tech(self, tech_name):
        self._tech.add({tech_name:1})

    def sub_units(self, units):
        self._units.sub(units)

    def sub_defenses(self, defenses):
        self._defenses.sub(defenses)

class TestPlayer(unittest.TestCase):
    def setUp(self):
        self.configuration = {"tech":{"armor":{}}, "units":{"m3":{}}, "defenses":{"bunker":{}}, "ressources":
            {"steel":{"value" : 1000, "delta" : 10}}}

    def test_init(self):
        player = Player(self.configuration)

if __name__ == "__main__":
    unittest.main()
