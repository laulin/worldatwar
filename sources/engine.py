import unittest
import unittest.mock as mock
import time
import logging

from authentification import PlayerAuthentification
from player_table import PlayerTable
from action_table import ActionTable
from action_table import ActionType

class Engine:
    def __init__(self, configuration):
        # constructor
        self._configuration = configuration
        self._log = logging.getLogger()

        self._authentification = PlayerAuthentification()
        self._players = PlayerTable(configuration)
        self._actions = ActionTable()


    # authentification
    def create(self, email, password_hashed, nick):
        # create a new player

        player_id = self._authentification.create(email, password_hashed, nick)
        self._players.create(player_id)

    def login(self, email, password_hashed):
        # log a player and return a player_token for thi session
        player_token = self._authentification.login(email, password_hashed)
        return player_token

    def _get_player(self, player_token):
        player_id = self._authentification.player_token_to_player_id(player_token)
        player = self._players.get(player_id)

        return player

    # gets
    def get_ressources(self, player_token):
        #from a player token, it returns him as the next format :
        # [timestamp, (ressource_1_value, ressource_1_delta), (...)]
        player = self._get_player(player_token)

        timestamp = int(time.time() * 1000)
        ressources = player.get_ressources()
        output = [timestamp]
        output.extend(ressources)
        return output

    def get_units(self, player_token):
        # using a player_token, it returns an ordereddict of (unit,number)
        player = self._get_player(player_token)

        return player.get_units()

    def get_defenses(self, player_token):
        # using a player_token, it returns an ordereddict of (defense,number)
        player = self._get_player(player_token)

        return player.get_defenses()

    def get_tech(self, player_token):
        # using a player_token, it returns an ordereddict of (tech,number)
        player = self._get_player(player_token)

        return player.get_tech()


    def _update_actions_building_unit(self, action):
        pass

    def _update_actions_building_defense(self, action):
        pass

    def _update_actions_building_tech(self, action):
        pass

    def _update_actions_spying(self, action):
        pass

    def _update_actions_attacking(self, action):
        pass

    def update_actions(self):
        """
        This function pops all timeouted action and do action
        """
        action_look_up = dict()
        action_look_up[ActionType.building_unit] = self._update_actions_building_unit
        action_look_up[ActionType.building_defense] = self._update_actions_building_defense
        action_look_up[ActionType.building_tech] = self._update_actions_building_tech
        action_look_up[ActionType.spying] = self._update_actions_spying
        action_look_up[ActionType.attacking] = self._update_actions_attacking

        # this function update the action table and report effect to players
        while self._actions.is_action_timeout():
            action = self._actions.pop_timeouted_action()
            callback = action_look_up.get(action.type, None)

            if not callback:
                self._log.warning("type {} is not valid".format(action.type))
                continue

            callback(action)

    def get_actions(self, player_token, filter=None):
        # using a player_token, it returns a list of action; if filter is a tuple,
        # it only keep action with the same type
        self.update_actions()
        player_id = self._authentification.player_token_to_player_id(player_token)
        return self._actions.get_player_actions(player_id)

    def get_tech_needed(self, branch, obj):
        return self._configuration[branch][obj].get("tech", dict())

    def get_missing_tech(self, player, branch, obj):
        needed_tech = self.needed_tech(branch, obj)
        missing_tech = player.check_min_tech(needed_tech)

        return missing_tech

    def get_cost(self, branch, obj):
        return self._configuration[branch][obj].get("tech", dict())

    # actions
    # things have to be payed at the ordering
    def build_unit(self, player_token, unit):
        # add a unit to the factory list
        player_id = self._authentification.player_token_to_player_id(player_token)
        player = self._get_player(player_token)


        missing_tech = self.get_missing_tech(player, "units", unit)
        if missing_tech:
            raise Exception("missing technologie : {}".format(missing_tech))

        if not player.check_min_ressources()



    def build_defense(self, player_token, defense):
        # add a defense to the factory list
        raise NotImplemented()

    def upgrade_tech(self, player_token, tech):
        # add a tech to the search lab list
        raise NotImplemented()

    def spy(self, player_token, other_player_name):
        # try to spy an other player and set the report to the mail box
        raise NotImplemented()

    def attack(self, player_token, other_player_name, units_dict):
        # run an attack from player_token to the other_player_name
        # using units_dict which contains (unit, number).
        # The battle result is in you mail box
        raise NotImplemented()

if __name__ == "__main__":
    class TestEngine(unittest.TestCase):
        def setUp(self):
            self.configuration = {"tech":{"armor":{}}, "units":{"m3":{}, "m4":{}}, "defenses":{"bunker":{}}, "ressources":
                {"steel":{"value" : 1000, "delta" : 10}}}

            self.engine = Engine(self.configuration)

        @mock.patch("__main__.time")
        def test_get_ressources(self, mock_time):
            time.time.return_value = 666
            self.engine.create("toto@titi.com", "xxx", "xxxTOTOxxx")
            player_token = self.engine.login("toto@titi.com", "xxx")
            output = self.engine.get_ressources(player_token)
            self.assertEqual([666000, (1000, 10)], output)


        def _test_get(self, fct, result):
            self.engine.create("toto@titi.com", "xxx", "xxxTOTOxxx")
            player_token = self.engine.login("toto@titi.com", "xxx")
            output = fct(player_token)
            self.assertEqual(result, output)

        def test_get_unit(self):
            self._test_get(self.engine.get_units, {"m3":0, "m4":0})

        def test_get_defenses(self):
            self._test_get(self.engine.get_defenses, {"bunker":0})

        def test_get_tech(self):
            self._test_get(self.engine.get_tech, {"armor":0})

    unittest.main()
