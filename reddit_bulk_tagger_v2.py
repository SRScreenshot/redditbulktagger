#!/usr/bin/env python
from __future__ import print_function

from collections import defaultdict
import json
import sys

import praw as reddit

subreddit_tags = {
        "MensRights": ("MRA", "red"),

        "TheRedPill": ("TRPer", "red"),
        "AlreadyRed": ("Super TRPer", "red"),
        "RedPillWomen": ("RedPillWoman", "red"),

        "antisrs": ("antisrs", "red"),
        "SRSSucks": ("SRSSucker", "red"),
}

COMMENT_LIMIT = 1000
SUBMISSION_LIMIT = 100
KARMA_THRESHOLD = 1

USER_AGENT = "BulkTagger/0.1.4"

def main():
    r = reddit.Reddit(user_agent=USER_AGENT)
    tags = {}

    for subreddit, tag in subreddit_tags.iteritems():
        print("Inspecting subreddit {}".format(subreddit), file=sys.stderr)
        thing_count = 0
        redditors = defaultdict(int)
        sr = r.get_subreddit(subreddit)

        new_comments = sr.get_comments(limit=COMMENT_LIMIT)
        new_submissions = sr.get_new(limit=SUBMISSION_LIMIT)
        hot_submissions = sr.get_hot(limit=SUBMISSION_LIMIT)

        for thing_group in (new_comments, new_submissions, hot_submissions):
            for thing in thing_group:
                thing_count += 1
                if thing_count % 100 == 0:
                    print("Seen {} things ...".format(thing_count), file=sys.stderr)
                if thing.author:
                    redditors[thing.author.name] += thing.ups - thing.downs

        for redditor, karma in redditors.iteritems():
            if karma > KARMA_THRESHOLD:
                tags[redditor] = {"tag": tag[0], "color": tag[1]}

    json.dump(tags, sys.stdout)
    print("Generated {} tags.".format(len(tags.keys())), file=sys.stderr)

if __name__ == "__main__":
    sys.exit(main())
