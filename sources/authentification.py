import unittest
import unittest.mock as mock
from collections import namedtuple
from uuid import uuid4

Player = namedtuple("Player", ["player_id", "email", "password_hashed", "nick"])

class PlayerAuthentification:
    def __init__(self):

        # key is a player id, value is a Player instance
        self._players = dict()

        # email to player_id index
        self._emails = dict()

        # nick to player_id
        self._nicks = dict()

        # player_to_are used to prevent player id theft
        self._player_tokens = dict()

    def create(self, email, password_hashed, nick):
        """
        This function creates a new players
        """

        if email in self._emails:
            raise Exception("email already registered")

        if nick in self._nicks:
            raise Exception("nickname already used")

        new_player = Player(str(uuid4()), email, password_hashed, nick)
        self._players[new_player.player_id] = new_player
        self._emails[new_player.email] = new_player.player_id
        self._nicks[new_player.nick] = new_player.player_id

        return new_player.player_id

    def login(self, email, password_hashed):
        """
        This function login the player and return player_token if every thing is ok
        """

        if email not in self._emails:
            raise Exception("you must be registered")

        player_id = self._emails[email]

        player = self._players[player_id]

        if player.password_hashed != password_hashed:
            raise Exception("bad password !")

        player_token = uuid4()
        self._player_tokens[player_token] = player_id

        return player_token

    def nick_to_player_id(self, nick):
        if nick not in self._nicks:
            raise Exception("nick '{}' doesn't exist".format(nick))

        return self._nicks[nick]

    def player_token_to_player_id(self, player_token):
        return self._player_tokens[player_token]

if __name__ == "__main__":

    class TestPlayerAuthentifiction(unittest.TestCase):

        def test_create_success(self):
            player_authentifiation = PlayerAuthentification()
            toto_id = player_authentifiation.create("toto@foo.bar", "ABCDEF01234", "xxx_toto_xxx")
            self.assertNotEqual(toto_id, None)

        def test_create_failed_already_exist_email(self):
            player_authentifiation = PlayerAuthentification()
            player_authentifiation.create("toto@foo.bar", "ABCDEF01234", "xxx_toto_xxx")
            self.assertRaises(Exception, player_authentifiation.create, ("toto@foo.bar", "ABCDEF01233", "yyy_toto_yyy"))

        def test_create_failed_already_exist_nick(self):
            player_authentifiation = PlayerAuthentification()
            player_authentifiation.create("toto@foo.bar", "ABCDEF01234", "xxx_toto_xxx")
            self.assertRaises(Exception, player_authentifiation.create, ("toto@foo.com", "ABCDEF01233", "xxx_toto_xxx"))

        def test_login_success(self):
            player_authentifiation = PlayerAuthentification()
            creation_id = player_authentifiation.create("toto@foo.bar", "ABCDEF01234", "xxx_toto_xxx")
            player_token = player_authentifiation.login("toto@foo.bar", "ABCDEF01234")
            login_id = player_authentifiation.player_token_to_player_id(player_token)
            self.assertEqual(creation_id, login_id)

        def test_login_fail_bad_email(self):
            player_authentifiation = PlayerAuthentification()
            creation_id = player_authentifiation.create("toto@foo.bar", "ABCDEF01234", "xxx_toto_xxx")
            self.assertRaises(Exception, player_authentifiation.login, ("toto@foo.bare", "ABCDEF01234"))

        def test_login_fail_bad_password(self):
            player_authentifiation = PlayerAuthentification()
            creation_id = player_authentifiation.create("toto@foo.bar", "ABCDEF01234", "xxx_toto_xxx")
            self.assertRaises(Exception, player_authentifiation.login, ("toto@foo.bar", "ABCDEF01233"))

        def test_nick_to_player_id_success(self):
            player_authentifiation = PlayerAuthentification()
            creation_id = player_authentifiation.create("toto@foo.bar", "ABCDEF01234", "xxx_toto_xxx")
            request_id = player_authentifiation.nick_to_player_id("xxx_toto_xxx")
            self.assertEqual(creation_id, request_id)

        def test_nick_to_player_id_fail(self):
            player_authentifiation = PlayerAuthentification()
            creation_id = player_authentifiation.create("toto@foo.bar", "ABCDEF01234", "xxx_toto_xxx")
            self.assertRaises(Exception, player_authentifiation.nick_to_player_id, ("yyy_toto_xxx"))


    if __name__ == "__main__":
        unittest.main()
