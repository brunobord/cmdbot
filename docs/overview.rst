===============
CmdBot Overview
===============

CmdBot is an IRC Bot written in Python. It consists of a core module that
defines a :class:`Bot` class you can extend to fit your needs. It comes with a
:class:`Brain`, that is to say a simple instance of ``object`` that can contain
any data you want. That's like a *memory* that lives as long as the Bot is
working.

.. warning::

    It's not exactly a data store. When you cut your bot off, its brain is
    vanishing and every thing is gone "forever". There might be a mechanism
    that'd allow you to save the brain state, but it's not yet available.

Install
=======

The Github (dev) version
------------------------

CmdBot is hosted on Github. If you want the latest code, go fetch it here:

https://github.com/brunobord/cmdbot

You can install the program using

.. code-block:: sh

    python setup.py install

The latest releases
-------------------

You can fetch and install the bot library using its `PyPI
<http://pypi.python.org/pypi/cmdbot/1.0.0>`_ version. If you are using pip and/or
virtualenv, just type

.. code-block:: sh

    pip install cmdbot

and you're done.

Usage
=====

the :mod:`cmdbot` module contains a :mod:`core` submodule where the "dumb" Bot
is sitting.

What you need to make any Bot working now is a nice '.ini' file.

.. _ini-file-label:

The INI file
------------

This file stores the basic configuration for you bot.  You can use the sample
bot.ini file that sits in the source code, or edit your own. You just have to
know that only two variables **must** be set in it

.. code-block:: ini

    [general]
    host = name.your.server
    chan = #nameyourchan

The other vars are optional, and usually default values would suit.

The "admin" value
~~~~~~~~~~~~~~~~~

If you want some admin to take this bot over (and you surely need it at some point),
set the value with a space-separated list of nicks... e.g.::

    admins = nick1 nick2 nick3

You may use the "@admin" decorator in your extended classes to process the bot
line **only** if the user that has send the order is in this nick list.

Dumb Bot Usage
--------------

It's as simple as

.. code-block:: sh

    python /path/to/cmdbot/core.py /path/to/your/bot.ini

But... your bot won't be able to do much. Here is a sample "dialog"

.. code-block:: irc

    22:31 -!- cmdbot [~cmdbot@127.0.0.1] has joined #cdc
    22:31 < cmdbot> Hi everyone.
    22:31 < No`> cmdbot: help
    22:31 < cmdbot> No`: you need some help? Here is some...
    22:31 < cmdbot> Available commands: help, ping
    22:32 < No`> cmdbot: ping
    22:32 < cmdbot> No`: pong
    22:32 -!- cmdbot [~cmdbot@127.0.0.1] has quit [EOF From client]

License
=======

This piece of software is published under the terms of the WTFPL  (Do What
The Fuck You Want License), that can be summed as its term "0":

     0. You just DO WHAT THE FUCK YOU WANT TO.

For more information, go to : <http://sam.zoy.org/wtfpl/>
