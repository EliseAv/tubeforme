#!/usr/bin/env python2.7

import feedparser
import os.path
import re
import urllib2

BASEPATH = os.path.dirname(__file__) + '/'
# feedparser.USER_AGENT = 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.11 (KHTML, like Gecko) Chrome/23.0.1271.91 Safari/537.11'


class VideoFeed:
    def __init__(self, url):
        self.url = url
        self.read_list = ReadList(url)

    def is_new(self, item):
        return self.read_list.is_new(item.id)

    def fetch(self):
        try:
            feed = feedparser.parse(self.url)
            items = feed.entries
            if len(items) == 0:
                raise Exception('Empty feed. Is site down?')
            new_items = filter(self.is_new, items)
            print 'Feed contains %d items, %d are new.' % (len(items), len(new_items))
            # iterate first, then save new read list
            for i in new_items:
                yield i
            self.read_list.save()
        except:
            print 'Unexpected error with', self.url
            print sys.exc_info()[0]


class EquestriaDailyVideoFeed(VideoFeed):
    re_contents = re.compile("<div class='post-body .+<div class='post-footer'>", re.DOTALL | re.IGNORECASE)
    re_youtube = re.compile('\\b(v[=/]|embed/|youtu\.be/)([A-Za-z0-9_-]{11})(?![A-Za-z0-9_-])', re.MULTILINE)

    def __init__(self, label=None):
        uri = 'http://www.equestriadaily.com/feeds/posts/default'
        if label is not None:
            uri += '/-/' + label
        VideoFeed.__init__(self, uri)

    def fetch_pages(self):
        for i in self.fetch():
            try:
                print i.id, i.link
                print 'Fetching ' + i.title
                response = urllib2.urlopen(i.link)
                html = response.read()
                print 'Read %d kibibytes.' % (len(html) / 1024,)
                match = self.re_contents.search(html)
                if match:
                    html = match.group(0)  # strip out header, footer, author, etc
                    yield html
                else:
                    print 'WARNING: No content.'
            except:
                print 'Unexpected error:', sys.exc_info()[0]
            print

    def fetch_video_codes(self):
        for html in self.fetch_pages():
            for match in self.re_youtube.finditer(html):
                video = match.group(2)
                print 'Found video:', video
                yield video


class YoutubeChannelVideoFeed(VideoFeed):
    def __init__(self, channel):
        VideoFeed.__init__(self, 'https://www.youtube.com/feeds/videos.xml?channel_id=' + channel)

    def fetch_video_codes(self):
        for item in self.fetch():
            video = item.id[-11:]  # sometimes it can be this easy :)
            print 'Found video: http://youtu.be/' + video
            yield video


class ReadList:  # this class is not thread-safe at all!
    filename = BASEPATH + 'known.py'
    lists = None

    def __init__(self, key):
        # static initialization
        if ReadList.lists is None:
            try:
                f = open(ReadList.filename)
                ReadList.lists = eval(f.read())
                f.close()
            except:
                ReadList.lists = {}
        # instance initialization
        self.key = key
        self.known = ReadList.lists.get(key, set())
        self.new = set()

    def is_new(self, item):
        self.new.add(item)
        return item not in self.known

    def save(self):
        ReadList.lists[self.key] = self.known = self.new
        self.new = set()
        f = open(ReadList.filename, 'w')
        f.write(repr(ReadList.lists))
        f.close()


def append_to_queue(video_feed):
    codes = video_feed.fetch_video_codes()
    links = map(lambda v: '\nhttp://www.youtube.com/watch?v=' + v, codes)
    f = open(BASEPATH + 'queue.txt', 'a')
    f.writelines(links)
    f.close()


if __name__ == '__main__':
    import sys

    if len(sys.argv) > 1:
        for ytvf in sys.argv[1:]:
            append_to_queue(YoutubeChannelVideoFeed(ytvf))
        sys.exit()
    # append_to_queue(EquestriaDailyVideoFeed()) sigh...
    append_to_queue(EquestriaDailyVideoFeed('Media'))
    append_to_queue(YoutubeChannelVideoFeed('UCAuUUnT6oDeKwE6v1NGQxug'))  # TED
    append_to_queue(YoutubeChannelVideoFeed('UCKRw8GAAtm27q4R3Q0kst_g'))  # RAP News
    append_to_queue(YoutubeChannelVideoFeed('UCyNG6pja1HRuZlMDR9dTI4w'))  # Ultra Fast Pony
    append_to_queue(YoutubeChannelVideoFeed('UCsaypaIo57-x7AfxuPmW2Ow'))  # DasDeer
    append_to_queue(YoutubeChannelVideoFeed('UC3LqW4ijMoENQ2Wv17ZrFJA'))  # PBS Idea Channel
    append_to_queue(YoutubeChannelVideoFeed('UCUL-pmhmDcZDwsA4cX2HO5w'))  # PHD Comics
    append_to_queue(YoutubeChannelVideoFeed('UCEWHPFNilsT0IfQfutVzsag'))  # Porta dos Fundos
    #append_to_queue(YoutubeChannelVideoFeed('UC376n347Ob5Lwzq2WGzF1AA'))  # Jornalismo SBT
    # append_to_queue(YoutubeChannelVideoFeed('democracynow'))
    append_to_queue(YoutubeChannelVideoFeed('UC3XTzVzaHQEd30rQbuvCtTQ'))  # Last Week Tonight
    append_to_queue(YoutubeChannelVideoFeed('UCIQMW4-IH91Ed4VPVbKMsaQ'))  # Ingress
    append_to_queue(YoutubeChannelVideoFeed('UC4ToGRJNQFPFAphVOEgg0ag'))  # IMATOONLINK
    #append_to_queue(YoutubeChannelVideoFeed('UCH-_hzb2ILSCo9ftVSnrCIQ'))  # yc Lewis
    #append_to_queue(YoutubeChannelVideoFeed('UCs4br3aZLU0sOEM-3n0-6xQ'))  # yc Duncan
    #append_to_queue(YoutubeChannelVideoFeed('UCpu8dLHavjMi1a5jgT9ycMA'))  # yc Sjin
    #append_to_queue(YoutubeChannelVideoFeed('UCUxoapwoGN9cKN5SPKGVh7A'))  # yc Kim
    # append_to_queue(YoutubeChannelVideoFeed('BdoubleO100')) mais mine via roo <3
    append_to_queue(YoutubeChannelVideoFeed('UCaYuAirih8a1Etht7KMuDaA'))  # heythatscool
    append_to_queue(YoutubeChannelVideoFeed('UCwf7GkXUML0Whgdt6lvMFTw'))  # Crowne Prince
    append_to_queue(YoutubeChannelVideoFeed('UCuUV_ANYYmZvdcUxbe5nH1Q'))  # OkashiNaArtist Nat
