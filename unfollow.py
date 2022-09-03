import time
import tweepy
import argparse
import random
from tqdm import tqdm
from utils import get_api, get_config

# relevant docs
# https://docs.tweepy.org/en/stable/api.html#follow-search-and-get-users
# https://docs.tweepy.org/en/stable/api.html#tweepy.API.destroy_friendship

if __name__ == "__main__":

    # randomly a percent of currently followed accounts
    # warning: can be slow! sleeps for 1 min between unfollows to avoid rate limits
    # warning: running this too frequently may breach twitters follow/unfollow rules

    parser = argparse.ArgumentParser(add_help=False)
    parser.add_argument("-h", "--handle", help="handle", required=False)
    args = parser.parse_args()
    handle = args.handle

    api = get_api(handle)
    config = get_config()

    print("\nbeginning unfollow bot for handle:", handle)

    following = []
    for users in tqdm(
        tweepy.Cursor(api.get_friends, screen_name=handle).pages(),
        "getting current following list",
    ):
        following.extend([u.screen_name for u in users])
        time.sleep(10)  # api rate limit

    print("found {} accounts following".format(len(following)))

    dont_unfollow = config["accounts"][handle]["dont_unfollow"]
    following = [
        f
        for f in tqdm(
            following,
            "skipping {} accounts in the dont_unfollow list".format(len(dont_unfollow)),
        )
        if f not in dont_unfollow
    ]

    # unfollow random accounts
    # dont unfollow too many too quickly or you will violate the terms of the API
    unfollow_count = min(int(len(following) * 0.1), config["max_unfollow_count"])
    print(
        "unfollowing {}% ({}) accounts".format(
            config["unfollow_percent"], unfollow_count
        )
    )
    for i in tqdm(range(unfollow_count)):
        # pop a random account from the following list
        screen_name = following.pop(random.randint(0, len(following) - 1))
        api.destroy_friendship(screen_name=screen_name)
        time.sleep(60)  # api rate limit
