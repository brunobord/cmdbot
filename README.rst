=================================
CmdBot, a bot with `cmd` attitude
=================================


Introducing CmdBot
==================

CmdBot is an IRC Bot written in Python. It consists of a core module that
defines a `Bot` class you can extend to fit your needs. It comes with a
`Brain`, that is to say a simple instance of ``object`` that can contain
any data you want. That's like a *memory* that lives as long as the Bot is
working.

It's far from being 100% perfect, but I think it takes the best of Python's
introspection mechanism.

By the way, why the name "CmdBot"? Because its function loading system has been
inspired by the `Python's cmd module <http://docs.python.org/library/cmd.html>`_,
that uses class member introspection to catch the designated functions and
execute them.

License
=======

This piece of software is published under the terms of the WTFPL  (Do What
The Fuck You Want License), that can be summed as its term "0":

     0. You just DO WHAT THE FUCK YOU WANT TO.

For more information, go to : <http://sam.zoy.org/wtfpl/>

The extensive documentation
===========================

An extensive documentation can be found at <http://readthedocs.org/docs/cmdbot/>

Install
=======

CmdBot is hosted on Github. If you want the latest code, go fetch it here:

https://github.com/brunobord/cmdbot

You can install the program using::

    python setup.py install


A cute "ini" file
-----------------

The mandatory step: building an ini file. You can use the sample bot.ini file
that sits in the source code, or edit your own. You just have to know that only
two variables **must** be set in it::

    [general]
    host = name.your.server
    chan = #nameyourchan

The other vars are optional, and usually default values would suit.

The "admin" value
#################

If you want some admin to take this bot over (and you surely need it at some point),
set the value with a space-separated list of nicks... e.g.::

    admins = nick1 nick2 nick3

You may use the "@admin" decorator in your extended classes to process the bot
line **only** if the user that has send the order is in this nick list.


Want to run the bot?
--------------------

It's as simple as::

    python cmdbot/core.py bot.ini

But... your bot won't be able to do much. Here is a sample "dialog"::

    22:31 -!- cmdbot [~cmdbot@127.0.0.1] has joined #cdc
    22:31 < cmdbot> Hi everyone.
    22:31 < No`> cmdbot: help
    22:31 < cmdbot> No`: you need some help? Here is some...
    22:31 < cmdbot> Available commands: help, ping
    22:32 < No`> cmdbot: ping
    22:32 < cmdbot> No`: pong
    22:32 -!- cmdbot [~cmdbot@127.0.0.1] has quit [EOF From client]

Want a more clever bot?
=======================

Here's how:

* Create a module / script with a bot that extends the core bot
* add it a few "do_[stuff]" commands
* make it more clever, by using its "brain"

You can see a few example of what a "brainy bot" can do in the `samples`
directory.

What's next?
============

Well... now, the sky is the limit. Extended bots can manipulate data, remember
it, treat and process it... And you can still use this bot as a "dumb", if you
want!
