tubeforme
=========

Script that looks for Youtube links in RSS feeds and downloads the videos in new articles.
Works great with VLC Media Player.

Around 2011, I was bored of visiting a blog to get the latest good videos published there.
It felt repetitive to queue stuff and jump to YouTube to watch it.
Years later, it has expanded to all my subscriptions and it's basically become my TV.
It's something use to watch the news, as well as the latest and newest. 99% of it I'll never see again.

No longer maintained
--------------------

As of Firefox 72, released in 2020, which launched
[Picture-in-Picture video](https://support.mozilla.org/en-US/kb/about-picture-picture-firefox),
this project became irrelevant to me. Feel free to take it to a loving home.

Installation
------------

I recommend your installation path (henceforth called `$DESTINATION`) to be your default videos folder.
For OS X users that's `$HOME/Movies`, for Windows users that's `%USERPROFILE%\Videos`.

1. Install [Python 3](http://python.org/download) and [Git](https://git-scm.com/download).
1. Clone this Git repository into `$DESTINATION/tubeforme`
1. Run `pip3 install -r requirements.txt` to install [required Python libraries](requirements.txt).
1. Create the subscriptions file (see below) in `$DESTINATION/subscriptions.yaml`
1. Add to your crontab something like `cd $DESTINATION; python3 -m tubeforme`
1. Your videos will end up in `$DESTINATION/videos`

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

This file's format is [YAML](http://yaml.org/).

Roadmap
-------

1. Use a database already, geez! These text files are embarassing!
1. A GUI of some sort. Preferably one that's easy to install on Windows.
1. Full support for all sites that [youtube-dl](https://github.com/rg3/youtube-dl) supports. They're hundreds!
