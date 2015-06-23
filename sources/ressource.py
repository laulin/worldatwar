import time
import unittest
import unittest.mock

class Ressource:
    """
    It manages a ressource including auto increasing value
    """

    def __init__(self, value, delta):
        """
        value : the start value
        delta : the value differencial, in value unit per second
        """

        self._value = int(value)
        self._delta = 0
        self._timestamp = int(time.time())

        self.set_delta(delta)

    def update(self):
        """
        Update ressource regarding the time difference
        """

        #@TODO the value mist be an int and computation is wong
        time_diff = int(time.time()) - self._timestamp
        self._value += self._delta * time_diff

        return self._value

    def get_value(self):
        self.update()
        return self._value

    def get_delta(self):
        return self._delta

    def set_delta(self, delta):
        self.update()
        delta = int(delta)
        if delta < 0:
            raise Exception("delta can't be negative")

        self._delta = delta

    def add_value(self, value):
        self.update()
        self._value += int(value)

    def sub_value(self, value):
        self.update()
        if self._value - int(value) < 0:
            raise Exception("Not enough ressources")

        self._value -= int(value)

    def is_available(self, value):
        """
        this function returns true if the value is available
        """
        return value < self._value

class TestRessource(unittest.TestCase):
    @unittest.mock.patch("time.time")
    def test_update(self, mock_time):
        mock_time.return_value = 0
        ressource = Ressource(1000, 10)
        mock_time.return_value = 1
        value = ressource.update()

        self.assertEqual(1010, value)


    @unittest.mock.patch("time.time")
    def test_set_delta(self, mock_time):
        mock_time.return_value = 0
        ressource = Ressource(1000, 1)
        ressource.set_delta(10)
        mock_time.return_value = 1
        value = ressource.update()

        self.assertEqual(1010, value)

    @unittest.mock.patch("time.time")
    def test_add_value(self, mock_time):
        mock_time.return_value = 0
        ressource = Ressource(1000, 1)
        ressource.add_value(100)

        self.assertEqual(1100, ressource.get_value())

    @unittest.mock.patch("time.time")
    def test_sub_value(self, mock_time):
        mock_time.return_value = 0
        ressource = Ressource(1000, 1)
        ressource.sub_value(100)

        self.assertEqual(900, ressource.get_value())

    def test_is_available(self):
        ressource = Ressource(1000, 1)
        self.assertTrue(ressource.is_available(900))
        self.assertFalse(ressource.is_available(1100))

if __name__ == "__main__":
    unittest.main()
