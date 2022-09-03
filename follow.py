import time
import argparse
from utils import get_api, get_config


if __name__ == "__main__":

    # follow accounts that have recently tweeted certain keywords (see config.json)
    # and are not already followed
    # and have follower/following numbers of a configurable threshold

    parser = argparse.ArgumentParser(add_help=False)
    parser.add_argument("-h", "--handle", help="handle", required=False)
    args = parser.parse_args()
    handle = args.handle

    print("\nbeginning bot for handle:", handle)
    api = get_api(handle)
    config = get_config()
    search_terms = config["accounts"][handle]["search_terms"]

    while True:
        print("\nbeginning new loop:", handle)

        for term in search_terms:
            tweets = api.search_tweets(term, count=config["max_search_results"])
            print("\nchecking tweets for term:", term)
            for t in tweets:
                # check the language of the tweet
                if t.lang == "en":
                    # ensure this isn't a retweet
                    if t.text[0:2] != "RT":
                        # accounts with more followers are more valuable to follow
                        if t.author.followers_count > config["min_followers"]:
                            # accounts with more friends (follows) more likely to follow back
                            if t.author.friends_count > config["min_following"]:

                                friendship = api.get_friendship(
                                    source_screen_name=handle,
                                    target_screen_name=t.user.screen_name,
                                )[0]
                                # check that neither account follows the other
                                if (
                                    not friendship.following
                                    and not friendship.followed_by
                                ):
                                    # print the user and tweet for sanity checks
                                    print("\nfollowing new user: ", t.user.screen_name)
                                    print("tweet: ", t.text)
                                    api.create_friendship(
                                        screen_name=t.user.screen_name
                                    )
                        else:
                            print("")

            # dont spam the api
            print("\nsleeping before next search")
            time.sleep(60 * 5)

        # dont spam the api
        print("\nsleeping for 2 hours")
