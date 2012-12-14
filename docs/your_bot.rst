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
            self.reply("hello", nick=line.nick_from)
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

'Say' or 'Reply'?
=================

Two basic actions are available to interact with the channel. The :meth:`say`
method simply "says" your message.

The :meth:`reply` method is a bit more elaborated, it's able to precisely reply
to a user, as you can see in the above example. Example usage:

.. code-block:: python

    @direct
    def do_hello(self, line):
        self.reply('my message', line=line)  # will reply to the line emitted by the user
        self.reply('my message', nick='mynick')  # will reply to 'mynick'


The `do_trick`
~~~~~~~~~~~~~~

You may have noticed that every new thing your bot knows to do is prefixed by
``do_``. That's the trick. When someone on the channel says something, the bot
analyses it. If the first word of the message is a ``verb`` your bot knows
about, the `do_<verb>` action is processed:

.. note::

    This behaviour is heavily borrowed on the Python :mod:`cmd` module.


The decorators
--------------

For more information about the available decorators, go to the :ref:`decorators-section`
section.


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

If you need special characters in your command, you cannot alias commands this
way. Instead, you'll have to add a property, like this:

.. code-block:: python

    def do_coffee(self, line):
        self.say(u'I can make coffee or café')
    do_foo.aliases = (u'café', u'cafés', 'cafe')

The aliases can be a list or a tuple. You'll have to define them using strings,
not necessarily using unicode.

The ``/me`` support
-------------------

Instead of using the :func:`self.say` method, you may alternatively use the
:func:`self.me` method, with will emulate when you are using the well-known
``/me`` IRC command.

.. code-block:: python

    def do_foo(self, line):
        self.say("I am a bot")
        self.me("is a bot")

will result as:

.. code-block:: irc

    <cmdbot>: I am a bot
    * cmdbot is a bot

The Configuration you want
==========================

Configure via the command-line arguments
----------------------------------------

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

Environment variables
---------------------

Alternatively, you may want to configure the bot via your environment variables.
For example:

.. code-block:: python

    from cmdbot.core import Bot
    from cmdbot.configs import EnvironmentConfiguration

    class MyEnvironmentBot(Bot):
        config_class = EnvironmentConfiguration

This bot will dig its configuration values out of the following environment
variables:

* ``CMDBOT_HOST``: mandatory IRC server host value
* ``CMDBOT_CHAN``: mandatory channel the bot must join.
* ``CMDBOT_PORT``: optional port value. Will default to '6667'.
* ``CMDBOT_NICK``: optional nick value. Default is 'cmdbot'
* ``CMDBOT_IDENT``: optional ident value. Default is 'cmdbot'
* ``CMDBOT_REALNAME``: optional real name value. Default is 'Cmd bot'
* ``CMDBOT_ADMINS``: a comma-separated list of the bot administrator.

Default admin list is empty.

What's next?
============

Well... now, the sky is the limit. Extended bots can manipulate data, remember
it, treat and process it... And you can still use this bot as a "dumb" one, if
you want!

You can also make your own decorators, exactly the way :func:`@admin` and
:func:`@direct` work. You may, for example... change the behaviour of a command
if your brain contains a certain bit of data, or if the first letter of the nick
is a "Z"... you see?... no. limit.

A few examples are available in the :file:`samples` directory. Good cmdbot-ing!
