#!/usr/bin/env python
from __future__ import print_function

from collections import defaultdict
import json
import sys

import praw as reddit

subreddit_tags = {
        "MensRights": "MRA",

        "TheRedPill": "TRPer",
        "AlreadyRed": "Super TRPer",
        "RedPillWomen": "RedPillWoman",

        "antisrs": "antisrs",
        "SRSSucks": "SRSSucker",
}

TAG_COLOR = "red"

COMMENT_LIMIT = 1000
SUBMISSION_LIMIT = 100
KARMA_THRESHOLD = 5

USER_AGENT = "BulkTagger/0.1.4"

def main():
    r = reddit.Reddit(user_agent=USER_AGENT)
    redditors = defaultdict(lambda: defaultdict(int))
    tags = {}

    for subreddit in subreddit_tags.keys():
        print("Inspecting subreddit {}".format(subreddit), file=sys.stderr)
        thing_count = 0
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
                    redditor = thing.author.name
                    redditors[redditor][subreddit] += thing.ups - thing.downs

    for redditor, seen_in_subs in redditors.iteritems():
        matched_tags = [subreddit_tags[sub] for sub, karma in seen_in_subs.items() if karma > KARMA_THRESHOLD]
        if len(matched_tags) == 0:
            continue
        compound_tag = " / ".join(sorted(matched_tags))
        tags[redditor] = {"tag": compound_tag, "color": TAG_COLOR}

    json.dump(tags, sys.stdout, sort_keys=True, indent=4, separators=(',', ': '))
    print("Generated {} tags.".format(len(tags.keys())), file=sys.stderr)

if __name__ == "__main__":
    sys.exit(main())
