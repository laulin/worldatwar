import unittest
from collections import OrderedDict
from ressource import Ressource

class Ressources:
    def __init__(self, configuration):
        self._ressources = list()

        for parameters in configuration["ressources"].values():
            self._ressources.append(Ressource(parameters["value"], parameters["delta"]))

    def update(self):
        for ressource in self._ressources:
            ressource.update()

    def get_value(self):
        output = [ressource.get_value() for ressource in self._ressources]
        return output

    def get_delta(self):
        output = [ressource.get_delta() for ressource in self._ressources]
        return output

    def set_delta(self, delta):
        [ressource.set_delta(delta[i]) for i,ressource in enumerate(self._ressources)]

    def add_value(self, value):
        [ressource.add_value(value[i]) for i,ressource in enumerate(self._ressources)]

    def sub_value(self, value):
        check = self.is_available(value)

        if not all(check):
            raise Exception("Not enough ressources")

        [ressource.sub_value(value[i]) for i,ressource in enumerate(self._ressources)]

    def is_available(self, value):
        return [ressource.is_available(value[i]) for i,ressource in enumerate(self._ressources)]

class TestRessources(unittest.TestCase):
    def setUp(self):
        self.configuration = OrderedDict([('ressources', OrderedDict([('steel', OrderedDict([('value', 1000), ('delta', 10)])), ('gasoil', OrderedDict([('value', 100), ('delta', 1)])), ('experience', OrderedDict([('value', 0), ('delta', 0)]))]))])

    def test_init(self):
        ressources = Ressources(self.configuration)

    def test_get_value(self):
        ressources = Ressources(self.configuration)
        values = ressources.get_value()

        self.assertEqual([1000, 100, 0], values)

    #TODO other tests have to be done !


if __name__ == "__main__":
    unittest.main()
