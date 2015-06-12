import unittest

class Warehouse:
    def __init__(self, contained_type, configuration):
        self._contained = dict()
        self._init_values(contained_type, configuration)

    def _init_values(self, contained_type, configuration):
        for name in configuration[contained_type].keys():
            self._contained[name] = int(configuration[contained_type][name].get("initial_number", 0))

    def check_min(self, request):
        # from the request parameters, which is a dict (name:quantity), it
        # check if this quantity is available in self._contained. Return a dict of
        # missing things
        output = dict()
        for name,quantity in request.items():
            if name not in self._contained:
                raise Exception("'{}' doesn't exist".format(name))

            if quantity < 0:
                raise ValueError("'{}'' is negative".format(name))

            if self._contained[name] < quantity:
                output[name] = quantity - self._contained[name]

        return output

    def get(self):
        return dict(self._contained)

    def add(self, request):
        # add request value to contained; request keys must be
        # already available in contained

        for name, quantity in request.items():
            if name not in self._contained:
                raise Exception("'{}' doesn't exist".format(name))

            if quantity < 0:
                raise ValueError("'{}'' is negative".format(name))

            self._contained[name] += quantity


    def sub(self, request):
        # sub request value to contained; request keys must be
        # already available in contained

        min_quantity = self.check_min(request)
        if min_quantity:
            formatted_needs = " ".join(["{}:+{}".format(k,v) for k,v in min_quantity.items()])
            raise Exception("sub need min_quantity for {}".format(formatted_needs))

        for name, quantity in request.items():
            if name not in self._contained:
                raise Exception("'{}' doesn't exist".format(name))

            if quantity < 0:
                raise ValueError("'{}'' is negative".format(name))

            self._contained[name] -= quantity

class TestWarehouse(unittest.TestCase):
    def setUp(self):
        self.conf = {"unit":{"toto":{"initial_number":2}}}

    def test_init(self):
        warehouse = Warehouse("unit", self.conf)

    def test_get(self):
        warehouse = Warehouse("unit", self.conf)
        self.assertEqual(warehouse.get(), {"toto":2})


    # check_min function test
    def test_check_min_success(self):
        warehouse = Warehouse("unit", self.conf)
        return_value = warehouse.check_min({"toto":2})

        self.assertEqual({}, return_value)

    def test_check_min_failed(self):
        warehouse = Warehouse("unit", self.conf)
        return_value = warehouse.check_min({"toto":3})

        self.assertEqual({"toto":1}, return_value)

    def test_check_min_bad_key(self):
        warehouse = Warehouse("unit", self.conf)
        self.assertRaises(Exception, warehouse.check_min, {"titi":3})

    def test_check_min_negative(self):
        warehouse = Warehouse("unit", self.conf)
        self.assertRaises(ValueError, warehouse.check_min, {"toto":-1})


    # add function test
    def test_add_success(self):
        warehouse = Warehouse("unit", self.conf)
        warehouse.add({"toto":1})

        self.assertEqual({"toto":3}, warehouse.get())

    def test_add_bad_key(self):
        warehouse = Warehouse("unit", self.conf)
        self.assertRaises(Exception, warehouse.add, {"titi":3})

    def test_add_negative(self):
        warehouse = Warehouse("unit", self.conf)
        self.assertRaises(ValueError, warehouse.add, {"toto":-1})

    # sub function test
    def test_sub_success(self):
        warehouse = Warehouse("unit", self.conf)
        warehouse.sub({"toto":1})

        self.assertEqual({"toto":1}, warehouse.get())

    def test_sub_bad_key(self):
        warehouse = Warehouse("unit", self.conf)
        self.assertRaises(Exception, warehouse.sub, {"titi":3})

    def test_sub_negative(self):
        warehouse = Warehouse("unit", self.conf)
        self.assertRaises(ValueError, warehouse.sub, {"toto":-1})


if __name__ == "__main__":
    unittest.main()
