==============
Advanced Usage
==============

.. _decorators-section:


Decorators
==========

Generally speaking, if you want a sample of what decorators can do, just check
the :file:`samples` directory for examples, especially the
:file:`decoratedbot.py` script.


@direct
-------

Whenever a :meth:`do_<stuff>` method is decorated by ``@direct``, it will only
be executed if someone is directly talking to the Bot:

.. code-block:: python

    @direct
    def do_hello(self, line):
        self.say('hello, you')

.. code-block:: irc

    22:53 -!- cmdbot [-cmdbot@127.0.0.1] has joined #cdc
    22:53 < cmdbot> Hi everyone.
    22:54 < No`> hello
    22:54 < No`> cmdbot: hello
    22:54 < cmdbot> hello, you

The first time, the user didn't talk directly to the bot. The second time, it
was mentioned, so the bot replied "hello, you"


@admin
------

When a :meth:`do_<stuff>` is decorated by ``@admin`` the code will only be
executed if the previous lines has been said by an admin:

.. code-block:: python

    @admin
    def do_hello(self, line):
        self.say('hello, my lord')

.. code-block:: irc

    22:53 -!- cmdbot [-cmdbot@127.0.0.1] has joined #cdc
    22:53 < cmdbot> Hi everyone.
    22:54 < NotAdmin> hello
    22:54 < AdminUser> hello
    22:54 < cmdbot> hello, my lord

.. note::

    You've noticed that it doesn't have to be direct. It's only if the verb it
    the first word of the message.


And what about "no decorator"
-----------------------------

Without decorator, the `do_<stuff>`  method will be called each time a line is
being said by a user. Beware, then, your bot may have a lot of work to do...


And what happens if we mix them?
--------------------------------

There comes the beauty of decorators. You can mix them:

.. code-block:: python

    @admin
    @direct
    def do_hello(self, line):
        self.say('hello, my lord')

The bot will then only say "hello my lord" if some admin directly told it
"hello".

Your own decorator
------------------

Right. You can "prefix" any action with your own decorator, if you want this
action to be called only following a certain condition or a subset of
conditions. Your "Bot's Brain" might help. Here's a simple example, taken from
the :file:`samples/gamebot.py`:

.. code-block:: python

    def in_game(func):
        "Decorator: only process the line game has been started with the player"
        @wraps(func)
        def newfunc(bot, line):
            if bot.brain.knows('games') and line.nick_from in bot.brain.games:
                return func(bot, line)
            else:
                bot.say("Erm. Looks like we didn't start playing.")
        return newfunc

In this snippet, we're defining a decorator that will only process the command
if the "game" has been started with the player.


After that, you can use the decorator like this:

.. code-block:: python

    @in_game
    def do_roll(self, line):
        # ...

Execute a command without a known verb
--------------------------------------

You may sometimes need to execute a function when somebody talks, or when a
special word is said **inside** a line, and not only at its beginning (a.k.a. a
regular "verb").

The ``@no_verb`` decorator is here to help. You can decorate any method
of your Bot class, even a method that doesn't start with a "do\_". e.g:

.. code-block:: python

    @no_verb
    def nothing_special(self, line):
        self.say('I say nothing special, you did not include a known verb')

Do not want help
----------------

It may happen that you'd need to discard help on a particular function. Many
use cases:

* You don't want your users to know that this command exists
* You don't want users to know how to execute a given command (your help line
  would make it too easy for them)
* You want to clean the raw `help` command, in order to have as few items as
  needed

You just need to decorate your function like this:

.. code-block:: python

    @no_help
    def do_nohelp(self, line):
        "I will never be displayed"
        pass

Logging
=======

A simple logging variable can be imported and use inside your bot methods.
By default, the Bot logging level is ``INFO``. You can easily change it like this

.. code-block:: python

    import logging
    logger.setLevel(logging.DEBUG)
    logging.debug("hey, I am debugging")

