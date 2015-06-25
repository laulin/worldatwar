import unittest
import os

from ordered_load import ordered_load


class Configuration:
    def __init__(self, filename=None):
        self._contained = dict()

        if filename:
            self.load(filename)

    def load(self, filename):
        with open(filename) as f:
            self._contained = ordered_load(f)


    def get_tech_needed(self, branch, obj):
        """
        This function return a dict containing tech level needed for obj in
        branch. because it is an optionnal field, it can return an empty
        dict.

        branch is like tech, units, defenses
        obj is like m3 or gun factory
        """

        return self._contained[branch][obj].get("tech", dict())

    def get_ressources_needed(self, branch, obj):
        """
        This function return a list containing ressources needed for obj in
        branch.

        branch is like tech, units, defenses
        obj is like m3 or gun factory
        """

        return self._contained[branch][obj]["price"]


if __name__ == "__main__":
    yaml_sample = """tech:
    gun_factory:
        price : [1,2,3]
        tech :
            weaponize : 2
            oil : 3
    """
    yaml_path = "/tmp/conf.yaml"

    class TestConfiguration(unittest.TestCase):
        def setUp(self):
            with open(yaml_path, "w") as f:
                f.write(yaml_sample)

            self.configuration = Configuration(yaml_path)

        def tearDown(self):
            os.remove(yaml_path)


        def test_get_tech_needed(self):
            return_value = self.configuration.get_tech_needed("tech", "gun_factory")
            self.assertEqual({"weaponize":2, "oil":3}, return_value)

        def test_get_ressources_needed(self):
            return_value = self.configuration.get_ressources_needed("tech", "gun_factory")
            self.assertEqual([1,2,3], return_value)

    unittest.main()
