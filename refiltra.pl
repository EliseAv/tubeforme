#!/usr/bin/perl -w

$^I = '~';

while (<>)
{
    # is this a video line?
    if (/\bv=([a-zA-Z0-9_-]{11})(?![a-zA-Z0-9_-])/)
    {
        # look for video file
        @found = glob "*-$1.{flv,mp4,video,webm,3gp}";
        print if $#found;
    }
}
