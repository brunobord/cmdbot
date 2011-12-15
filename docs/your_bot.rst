==================
Build Your Own Bot
==================

Okay, so this dumb bot can't do much, can it? You want something more exciting?


Want a more clever bot?
=======================

Here's how:

* Create a module / script with a bot that extends the core bot
* add it a few "do_[stuff]" commands
* make it more clever, by using its "brain"

You can see a few example of what a "brainy bot" can do, remember by browsing
the bots available in the "samples" directory.


Detailed example: ``brainybot``
-------------------------------

BrainyBot is a class that resides in the :file:`samples` directory. Let's dive
in its code:

.. code-block:: python

    from cmdbot.core import Bot, direct

    class BrainyBot(Bot):

        @direct
        def do_hello(self, line):
            "Reply hello and save that in brain"
            self.say("%s: hello" % line.nick_from)
            self.brain.who_said_hello_last = line.nick_from

        @direct
        def do_who(self, line):
            "Tell us who talked to you last"
            if self.brain.knows('who_said_hello_last'):
                self.say("The one that talked to me last: %s" % self.brain.who_said_hello_last)
            else:
                self.say("Nobody has talked to me...")


Since :class:`BrainyBot` extends the :class:`Bot` class, it already knows how to
"ping" and how to "help" you. If we run it (using an appopriate '.ini' file),
and try to talk to it, here is some result:

.. code-block:: irc

    22:53 -!- cmdbot [~cmdbot@127.0.0.1] has joined #cdc
    22:53 < cmdbot> Hi everyone.
    22:54 < No`> cmdbot: hello
    22:54 < cmdbot> No`: hello
    22:54 < No`> cmdbot: who
    22:54 < cmdbot> The one that talked to me last: No`

We've used the :class:`Brain` of our Bot, to tell it to store in-memory who's
talked to him last. And by asking it `who`, it's able to tell it to us.

Please note the :meth:`knows` method, that returns `True` if the brain has an
"interesting" value (i.e. not "None", or empty string, list, tuple, etc).
You can just test wether the lookuped key is present in the brain by using the
optional `include_falses` argument:

.. code-block:: python

    >>> bot.brain.knows('stuff')
    False
    >>> bot.brain.stuff = ''
    >>> bot.brain.knows('stuff')
    False
    >>> bot.brain.knows('stuff', include_falses=True)
    True
    >>> bot.brain.stuff = 'hello'
    >>> bot.brain.knows('stuff')
    True


The `do_<trick>`
~~~~~~~~~~~~~~~~

You may have noticed that every new thing your bot knows to do is prefixed by
``do_``. That's the trick. When someone on the channel says something, the bot
analyses it. If the first word of the message is a ``verb`` your bot knows
about, the `do_<verb>` action is processed:

.. note::

    This behaviour is heavily borrowed on the Python :mod:`cmd` module.


The decorators
--------------


@direct
~~~~~~~

Whenever a :meth:`do_<stuff>` method is decorated by ``@direct``, it will only
be executed if someone is directly talking to the Bot:

.. code-block:: python

    @direct
    def do_hello(self, line):
        self.say('hello, you')

.. code-block:: irc

    22:53 -!- cmdbot [~cmdbot@127.0.0.1] has joined #cdc
    22:53 < cmdbot> Hi everyone.
    22:54 < No`> hello
    22:54 < No`> cmdbot: hello
    22:54 < cmdbot> hello, you

The first time, the user didn't talk directly to the bot. The second time, it
was mentioned, so the bot replied "hello, you"


@admin
~~~~~~

When a :meth:`do_<stuff>` is decorated by ``@admin`` the code will only be
executed if the previous lines has been said by an admin:

.. code-block:: python

    @admin
    def do_hello(self, line):
        self.say('hello, my lord')

.. code-block:: irc

    22:53 -!- cmdbot [~cmdbot@127.0.0.1] has joined #cdc
    22:53 < cmdbot> Hi everyone.
    22:54 < NotAdmin> hello
    22:54 < AdminUser> hello
    22:54 < cmdbot> hello, my lord

.. note::

    You've noticed that it doesn't have to be direct. It's only if the verb it
    the first word of the message.


And what about "no decorator"
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Without decorator, the `do_<stuff>`  method will be called each time a line is
being said by a user. Beware, then, your bot may have a lot of work to do...


And what happens if we mix them?
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

There comes the beauty of decorators. You can mix them:

.. code-block:: python

    @admin
    @direct
    def do_hello(self, line):
        self.say('hello, my lord')

The bot will then only say "hello my lord" if some admin directly told it
"hello".

Your own decorator
~~~~~~~~~~~~~~~~~~

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


Bonus: the welcome message
--------------------------

Each bot says something when it /joins the chan. If you want a custom message,
just do something like:

.. code-block:: python

    class FrenchBot(Bot):
        welcome_message = "Bonjour tout le monde !"


More Bonus: command aliases
---------------------------

You may want to define aliases for any command, like this:

.. code-block:: python

    def do_foo(self, line):
        self.say('I do foo or bar')
    do_bar = do_foo

You won't have to worry about decorated methods, and such. Everything will work
exactly the same.

The Configuration you want
==========================

CmdBot is coming with two available configuration modules. The default one is
using the "ini file" described in :ref:`the ini file section <ini-file-label>`.

But you can override this using the :class:`ArgumentConfiguration`. Like this:

.. code-block:: python

    from cmdbot.core import Bot
    from cmdbot.configs import ArgumentConfiguration

    class ArgumentBot(Bot):
        config_class = ArgumentConfiguration

That's it. If you want, you can build your own configuration module. All you have
to do is to build one that has at least the following available properties (if
not mentioned, should be a string):

* host
* chan
* port - should be an int
* nick
* ident
* realname
* admins - should be a tuple, a list or any iterable


What's next?
============

Well... now, the sky is the limit. Extended bots can manipulate data, remember
it, treat and process it... And you can still use this bot as a "dumb" one, if
you want!

You can also make your own decorators, exactly the way :func:`@admin` and
:func:`@direct` work. You may, for example... change the behaviour of a command
if your brain contains a certain bit of data, or if the first letter of the nick
is a "Z"... you see?... no. limit.

A few more examples will probably appear in the :file:`samples` directory. Stay
tuned!
