import unittest
from player import Player

class PlayerTable:
    def __init__(self, configuration):

        # keep the configuration for player creation
        self._configuration = configuration

        self._players = dict()

    def create(self, player_id):
        """
        create a new line for this player_id
        """

        if player_id in self._players:
            raise Exception("player id {} already exist".format(player_id))


        self._players[player_id] = Player(self._configuration)


    def get(self, player_id):
        """
        return a player object using it player id
        """

        return self._players[player_id]

if __name__ == "__main__":
    class TestPlayer(unittest.TestCase):
        def setUp(self):
            self.configuration = {"tech":{"armor":{}}, "units":{"m3":{}}, "defenses":{"bunker":{}}, "ressources":
                {"steel":{"value" : 1000, "delta" : 10}}}

        def test_init(self):
            player_table = PlayerTable(self.configuration)

        def test_create(self):
            player_table = PlayerTable(self.configuration)
            player_table.create("xxx")

        def test_create_fail(self):
            player_table = PlayerTable(self.configuration)
            player_table.create("xxx")
            # already existing player_id
            self.assertRaises(Exception, player_table.create, "xxx")

        def test_get(self):
            player_table = PlayerTable(self.configuration)
            player_table.create("xxx")
            player_table.get("xxx")

    unittest.main()
