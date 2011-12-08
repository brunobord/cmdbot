============
Your Own Bot
============

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
in its code

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
            if hasattr(self.brain, 'who_said_hello_last'):
                self.say("The one that talked to me last: %s" % self.brain.who_said_hello_last)
            else:
                self.say("Nobody has talked to me...")


Since :class:`BrainyBot` extends the :class:`Bot` class, it already knows how to
"ping" and how to "help" you. If we run it (using an appopriate '.ini' file),
and try to talk to it, here is some result

.. code-block:: irc

    22:53 -!- cmdbot [~cmdbot@127.0.0.1] has joined #cdc
    22:53 < cmdbot> Hi everyone.
    22:54 < No`> cmdbot: hello
    22:54 < cmdbot> No`: hello
    22:54 < No`> cmdbot: who
    22:54 < cmdbot> The one that talked to me last: No`

We've used the :class:`Brain` of our Bot, to tell it to store in-memory who's
talked to him last. And by asking it `who`, it's able to tell it to us.

What's next?
============

Well... now, the sky is the limit. Extended bots can manipulate data, remember
it, treat and process it... And you can still use this bot as a "dumb", if you
want!

A few more examples will probably appear in the :file:`samples` directory. Stay
tuned!
