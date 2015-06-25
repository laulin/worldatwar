import unittest
import unittest.mock as mock
import heapq
from uuid import uuid4
from collections import namedtuple
import time
from enum import Enum

class ActionType(Enum):
    building_unit = 1
    building_defense = 2
    building_tech = 3
    spying = 4
    attacking = 5

Action = namedtuple("Action", ["id", "start", "stop", "player_id_source", "player_id_dest", "type", "args"])

class ActionTable:
    """
    This class contains all action/events that occurs during the game
    """

    def __init__(self):
        # it keep action_id -> Action
        self._main_table = dict()

        # to do action in the right order, we keep an ordered list using
        # the heapq module. it use a tuple (stop, action_id)
        self._stop_time_index = []

        # each player have to know what happen.
        # Keep player_id -> {action_id}
        self._player_index = dict()

    def add_action(self, duration, player_id_source, player_id_dest, action_type, args):
        """
        this function creates a new action
        the duration unit is ms
        player_id is a string
        action type is an integer @TODO enum
        args depends on action type
        """

        current_time = int(time.time() * 1000)
        action_id = str(uuid4())
        start = current_time
        stop = current_time + duration

        if not player_id_source:
            raise Exception("player id source is mandatory")

        new_action = Action(action_id, start, stop, player_id_source, player_id_dest, action_type, args)

        # updating tables
        self._main_table[action_id] = new_action
        heapq.heappush(self._stop_time_index, (stop, action_id))
        self._player_index.setdefault(player_id_source, set()).add(action_id)

        if player_id_dest:
            self._player_index.setdefault(player_id_source, set()).add(action_id)

    def is_action_timeout(self):
        """
        return True only if one or more action is done
        """
        current_time = int(time.time() * 1000)

        if not self._stop_time_index:
            return False

        # get the last timeout available and check if it timeouts
        if self._stop_time_index[0][0] < current_time:
            return True
        else:
            return False

    def get_player_actions(self, player_id):
        """
        This function return all Action instances of one player
        """

        action_ids = self._player_index.get(player_id, set())

        output = []
        for action_id in action_ids:
            output.append(self._main_table[action_id])

        return output


    def pop_timeouted_action(self):
        """
        return the oldest action that is finished
        """
        if not self.is_action_timeout():
            raise Exception("no action finished")

        # got the action
        timeout, action_id = heapq.heappop(self._stop_time_index)
        action = self._main_table[action_id]

        # and remove from the table
        del self._main_table[action_id]

        self._player_index.get(action.player_id_source, set()).discard(action_id)

        if action.player_id_dest:
            self._player_index.get(action.player_id_dest, set()).discard(action_id)

        return action


if __name__ == "__main__":

    class TestActionTable(unittest.TestCase):
        @mock.patch("__main__.uuid4")
        @mock.patch("__main__.time")
        def test_add_action_no_dest(self, time_mock, mock_uuid4):
            time_mock.time.return_value = 0
            mock_uuid4.return_value = "1234-5678-6666"
            table = ActionTable()
            table.add_action(10, "toto", None, 1, None)
            self.assertEqual({'1234-5678-6666': Action(id='1234-5678-6666', start=0, stop=10, player_id_source='toto', player_id_dest=None, type=1, args=None)}, table._main_table)

        @mock.patch("__main__.uuid4")
        @mock.patch("__main__.time")
        def test_add_action(self, time_mock, mock_uuid4):
            time_mock.time.return_value = 0
            mock_uuid4.return_value = "1234-5678-6666"
            table = ActionTable()
            table.add_action(10, "toto", "titi", 1, None)
            self.assertEqual({'1234-5678-6666': Action(id='1234-5678-6666', start=0, stop=10, player_id_source='toto', player_id_dest='titi', type=1, args=None)}, table._main_table)
        #
        # @mock.patch("__main__.uuid4")
        # @mock.patch("__main__.time")
        # def test_add_action_check_stop_queue(self, time_mock, mock_uuid4):
        #     time_mock.time.return_value = 0
        #     mock_uuid4.side_effect = ["1-1", "2-2", "3-3"]
        #     table = ActionTable()
        #     table.add_action(10, "toto", "titi", 1, None)
        #     table.add_action(20, "toto", "titi", 1, None)
        #     table.add_action(5, "toto", "titi", 1, None)

        @mock.patch("__main__.time")
        def test_is_action_timeout(self, time_mock):
            time_mock.time.return_value = 0
            table = ActionTable()
            table.add_action(10000, "toto", "titi", 1, None)
            time_mock.time.return_value = 100

            self.assertTrue(table.is_action_timeout())

        @mock.patch("__main__.time")
        def test_is_action_timeout_failed(self, time_mock):
            time_mock.time.return_value = 0
            table = ActionTable()
            table.add_action(10000, "toto", "titi", 1, None)
            time_mock.time.return_value = 5

            self.assertFalse(table.is_action_timeout())


        @mock.patch("__main__.time")
        def test_get_player_actions(self, time_mock):
            time_mock.time.return_value = 0
            table = ActionTable()
            table.add_action(10000, "toto", "titi", 1, None)
            table.add_action(1000, "toto", "foo", 1, None)

            output = table.get_player_actions("toto")
            self.assertEqual(2, len(output))

        @mock.patch("__main__.uuid4")
        @mock.patch("__main__.time")
        def test_pop_timeouted_action(self, time_mock, uuid4_mock):
            time_mock.time.return_value = 0
            uuid4_mock.return_value = "xxxx-xxxx-xxxx-xxxx"

            table = ActionTable()
            table.add_action(10000, "toto", "titi", 1, None)
            time_mock.time.return_value = 100

            action = table.pop_timeouted_action()
            self.assertEqual(Action("xxxx-xxxx-xxxx-xxxx", 0, 10000, "toto", "titi", 1, None), action)

    unittest.main()
