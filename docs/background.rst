==========
Background
==========

Why, oh, why!
=============

tl;dr: because I needed it.

Now with the actual reason...

Yes, yes, yes, I know. "Yet another IRC Bot"... But why oh why oh why did you
need to make a new one? There are tons of them: `SupyBot
<http://sourceforge.net/projects/supybot/>`_, `Phenny
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
