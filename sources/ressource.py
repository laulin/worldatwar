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
        self._delta = int(delta)
        self._timestamp = int(time.time())

    def update(self):
        """
        Update ressource regarding the time difference
        """

        time_diff = int(time.time()) - self._timestamp
        self._value += self._delta * time_diff

        return self._value

    def get_value(self):
        return self._value

    def set_delta(self, delta):
        self._delta = int(delta)

    def add_value(self, value):
        self._value += int(value)

    def sub_value(self, value):
        if self._value - int(value) < 0:
            raise Exception("Not enough ressources")

        self._value -= int(value)

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
        mock_time.return_value = 1
        ressource.set_delta(10)
        value = ressource.update()

        self.assertEqual(1010, value)

    def test_add_value(self):
        ressource = Ressource(1000, 1)
        ressource.add_value(100)

        self.assertEqual(1100, ressource.get_value())


    def test_sub_value(self):
        ressource = Ressource(1000, 1)
        ressource.sub_value(100)

        self.assertEqual(900, ressource.get_value())

if __name__ == "__main__":
    unittest.main()
