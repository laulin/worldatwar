Introduction
============

This repo is a game engine for web browser. Because it is just an engine, it
don't care about interface (web, cli, ...)

Final API
=========

It is was a player will see, and what he can do. This is as simple as possible,
further FAPI could have more feature (messages, ...)

logging :
    - create a player unsing a mail, a password and a nickname
    - logging with him mail and password
    - disconnect with him player token (got with logging)

in-game :
    get :
        - get ressources
        - get units available
        - get defenses available
        - get tech levels
        - get actions (attacking/defending, building)
        - get messages list
        - get one message

    set :
        - build unit/defense
        - upgrade tech
        - spy a player (and get the report)
        - attack a player
        - write one message

    check if the values are correct. It allows the user to see if one value is
    unconsistency:
        - build unit/defense
        - upgrade tech
        - spy a player (and get the report)
        - attack a player
