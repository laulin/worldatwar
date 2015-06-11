import unittest

class Engine:
    def __init__(self):
        # constructor
        raise NotImplemented()


    # authentification
    def create(self, email, raise NotImplemented()word_hashed, nick):
        # create a new player

        raise NotImplemented()

    def logging(self, email, raise NotImplemented()word_hashed):
        # log a player and return a player_token for thi session
        raise NotImplemented()


    # gets
    def get_ressources(self, player_token):
        #from a player token, it returns him as the next format :
        # [timestamp, (ressource_1_value, ressource_1_delta), (...)]
        raise NotImplemented()

    def get_units(self, player_token):
        # using a player_token, it returns an ordereddict of (unit,number)
        raise NotImplemented()

    def get_defenses(self, player_token):
        # using a player_token, it returns an ordereddict of (defense,number)
        raise NotImplemented()

    def get_techs(self, player_token):
        # using a player_token, it returns an ordereddict of (tech,number)
        raise NotImplemented()

    def get_events(self, player_token, filter=None):
        # using a player_token, it returns a list of event; if filter is a tuple,
        # it only keep event with the same type
        raise NotImplemented()

    # actions
    # things have to be payed at the ordering
    def build_unit(self, player_token, unit):
        # add a unit to the factory list
        raise NotImplemented()

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
