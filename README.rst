=================================
CmdBot, a bot with `cmd` attitude
=================================

Why, oh, why!
=============

tl;dr: because I needed it.

Now with the actual reason...

Yes, yes, yes, I know. "Yet another IRC Bot"... But why oh why oh why did you
need to make a new one? There are tons of them: `SupyBot
<http://sourceforge.net/projects/supybot/>`_ `Phenny
<http://inamidst.com/phenny/>`_, and the super-hyper `Hubot
<https://github.com/github/hubot>`_... Here's the deal, right? There are a lot
of bots, but all of them suck at one thing: remembering. Usually, these bots
only know how to perform small tasks that only require a `ping` and a `pong`
back with the answer. After doing this task, your question and its answer are
gone, and the bot forgets about it.

Here was my challenge: I wanted to hack a bot that could handle a small IRC-
based game, with several players, a subset of rules, dice rolling, keeping
scores during the game, and a winner when the score of a player was reaching the
goal. To do that, your bot needs a brain.

The case of Hubot
-----------------

I've been tempted to build it using Hubot, and its `Hubot-irc adapter
<https://github.com/nandub/hubot-irc/>`_. But I've lost three full evenings
trying to make it work, without success. My `bug report
<https://github.com/nandub/hubot-irc/issues/4>`_ lead to solve it. It might
change in the future, but my node-js skills are close to zero, and my Javascript
is a bit above this level.

I needed to succeed. Building a "dumb" IRC bot is quite easy. There are tons of
examples you can find on the web. You can extend these bots by adding a
plugin system, like Supybot's or phenny's. But that's not good for my use, because
it "only" consists of an ephemereal callback function. I needed a "smarter" bot.

Introducing CmdBot
------------------

Here is my take. It's far from being 100% perfect, but I think it takes the best
of Python's introspection mechanism.

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

Install
=======

CmdBot is hosted on Github. If you want the latest code, go fetch it here::

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
~~~~~~~~~~~~~~~~~

If you want some admin to take this bot over (and you surely need it at some point),
set the value with a space-separated list of nicks... e.g.::

    admins = nick1 nick2 nick3

You may use the "@admin" decorator in your extended classes to process the bot
line **only** if the user that has send the order is in this nick list.


Want to run the bot?
--------------------

It's as simple as::

    python bot.py bot.ini

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

You can see a few example of what a "brainy bot" can do, remember by browsing
the bots available in the "samples" directory.

What's next?
============

Well... now, the sky is the limit. Extended bots can manipulate data, remember
it, treat and process it... And you can still use this bot as a "dumb", if you
want!

