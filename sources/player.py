import unittest

from ressources import Ressources

class Player:
    def __init__(self, configuration):
        self._ressources = Ressources(configuration):

        # build a dict with all keys
        # contains all units available
        self._units = dict()
        self._init_units(configuration)

        #contains all defenses available
        self._defenses = dict()
        self._init_defenses(configuration)

        # define tech available
        self._tech = dict()
        self._init_tech()

        # all event from and to the player
        self._events = dict()

    def _init_units(self, configuration):
        for name in configuration["units"].keys():
            self._units[name] = configuration["units"].get("initial_number", 0)

    def _init_defenses(self, configuration):
        for name in configuration["defenses"].keys():
            self._defenses[name] = configuration["defenses"].get("initial_number", 0)

    def _init_tech(self, configuration):
        for name in configuration["tech"].keys():
            self._init_tech[name] = configuration["tech"].get("initial_level", 0)
