import json
import time
import tweepy
import argparse

# DOCS https://docs.tweepy.org/en/stable/client.html

# load config and credentials
with open("./config.json") as f:
    config = json.load(f)
with open("./credentials.json") as f:
    credentials = json.load(f)

if __name__ == "__main__":

    parser = argparse.ArgumentParser()
    parser.add_argument(
        "-a", "--account", help="account", required=False, default="barefootdev"
    )
    args = parser.parse_args()
    account = args.account

    print("\nbeginning bot for account:", account)

    API_KEY = credentials[account]["API_KEY"]
    API_SECRET = credentials[account]["API_SECRET"]
    ACCESS_TOKEN = credentials[account]["ACCESS_TOKEN"]
    ACCESS_TOKEN_SECRET = credentials[account]["ACCESS_TOKEN_SECRET"]
    TWITTER_HANDLE = config["accounts"][account]["handle"]
    SEARCH_TERMS = config["accounts"][account]["search_terms"]
    MAX_SEARCH_RESULTS = config["max_search_results"]
    MIN_FOLLOWERS = config["min_followers"]
    MIN_FOLLOWING = config["min_following"]

    tweepy_auth = tweepy.OAuthHandler(API_KEY, API_SECRET)
    tweepy_auth.set_access_token(ACCESS_TOKEN, ACCESS_TOKEN_SECRET)
    client = tweepy.Client(tweepy_auth)
    api = tweepy.API(tweepy_auth)

    while True:
        print("\nbeginning new loop")

        for term in SEARCH_TERMS:
            tweets = api.search_tweets(term, count=MAX_SEARCH_RESULTS)
            print("\nchecking tweets for term:", term)
            for t in tweets:
                # check the language of the tweet
                if t.lang == "en":
                    # ensure this isn't a retweet
                    if t.text[0:2] != "RT":  
                        # accounts with more followers are more valuable to follow
                        if (
                            t.author.followers_count > MIN_FOLLOWERS
                        ):  
                            # accounts with more friends (follows) more likely to follow back
                            if (
                                t.author.friends_count > MIN_FOLLOWING
                            ):  

                                friendship = api.get_friendship(
                                    source_screen_name=TWITTER_HANDLE,
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

            # dont spam the api
            print("\nsleeping before next term")
            time.sleep(60 * 5)

        # dont spam the api
        print("\nsleeping for 2 hours")
