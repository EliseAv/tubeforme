.. coding: utf-8

=========
tubeforme
=========

Around 2008, I was bored of visiting a blog to get the latest good videos published there.
It felt repetitive to queue stuff and jump to YouTube to watch it.
Years later, it has expanded to all my subscriptions and it's basically become my TV.
It's something use to watch the news, as well as the latest and newest. 99% of it I'll never see again.

I originally made it for my own use only, but if more people use it I can make it easier to use.

Installation
------------

I recommend your installation path (henceforth called ``$DESTINATION``) to be your default videos folder.
For OS X users that's ``$HOME/Movies``, for Windows users that's ``%USERPROFILE%\Videos``.

#. Install `Python 3`_ and Git_.
#. Clone this Git repository into ``$DESTINATION/tubeforme``
#. Run ``pip3 install -r requirements.txt`` to install `required Python libraries`_.
#. Create the subscriptions file (see below) in ``$DESTINATION/subscriptions.yaml``
#. Add to your crontab something like ``cd $DESTINATION; python3 -m tubeforme``
#. Your videos will end up in ``$DESTINATION/videos``

Subscriptions file
------------------

Here's an empty subscriptions file::

    blogs: []
    youtube_channels: []

Here's part of my own subscriptions file::

    blogs:
        - http://www.equestriadaily.com/feeds/posts/default/-/Media
    youtube_channels:
        - UCAuUUnT6oDeKwE6v1NGQxug  # TED Talks
        - UCKRw8GAAtm27q4R3Q0kst_g  # Juice Media (Rap News)
        - UCzuqE7-t13O4NIDYJfakrhw  # Democracy Now
        - UC3XTzVzaHQEd30rQbuvCtTQ  # Last Week Tonight
        - UC3LqW4ijMoENQ2Wv17ZrFJA  # PBS Idea Channel

This file's format is YAML_.

Roadmap
-------

#. Use a database already, geez! These text files are embarassing!
#. A GUI of some sort. Preferably one that's easy to install on Windows.
#. Full support for all sites that youtube-dl_ supports. They're hundreds!

.. _Python 3: http://python.org/download
.. _Git: https://git-scm.com/download
.. _required Python libraries: requirements.txt
.. _YAML: http://yaml.org/
.. _youtube-dl: https://github.com/rg3/youtube-dl
